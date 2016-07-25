#include "itkImageFileWriter.h"
#include "itkImage.h"
#include "itkImageRegionConstIterator.h"
#include "itkImageRegionIterator.h"

//Segmentation Methods
#include "itkBayesianClassifierInitializationImageFilter.h"
#include "itkBayesianClassifierImageFilter.h"

#include "itkPluginUtilities.h"

#include "BayesianDTISegmentationCLP.h"

#ifdef _WIN32
#define STATISTICALTEMPLATESFOLDER "\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates"
#define PATH_SEPARATOR "\\"
#define PATH_SEPARATOR_CHAR '\\'
#define DEL_CMD "del /Q "
#define MOVE_CMD "move "
#else
#define STATISTICALTEMPLATESFOLDER "/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates"
#define PATH_SEPARATOR "/"
#define PATH_SEPARATOR_CHAR '/'
#define DEL_CMD "rm -f "
#define MOVE_CMD "mv "
#endif

using namespace std;

// Use an anonymous namespace to keep class types and function names
// from colliding when module is used as shared object module.  Every
// thing should be in an anonymous namespace except for the module
// entry point, e.g. main()
//
namespace
{

template <class T>
int DoIt( int argc, char * argv[], T )
{

#ifdef _WIN32
    char* HOME_DIR=getenv("HOMEPATH");
#else
    char* HOME_DIR=getenv("HOME");
#endif

    PARSE_ARGS;

    typedef float                          InputPixelType;
    typedef unsigned char                  OutputPixelType;
    typedef float                          PriorType;
    typedef float                          PosteriorType;
    const unsigned int                     Dimension=3;

    typedef itk::Image<InputPixelType,  Dimension>              InputImageType;
    typedef itk::VectorImage< InputPixelType, Dimension >       VectorInputImageType;

    typedef itk::ImageFileReader<InputImageType>                ReaderType;
    typedef itk::ImageFileReader<VectorInputImageType>          PriorsReaderType;

    typename ReaderType::Pointer reader = ReaderType::New();
    reader->SetFileName( inputVolume.c_str() );
    reader->Update();

    //Bayesian Segmentation Approach
    typedef itk::BayesianClassifierInitializationImageFilter< InputImageType >         BayesianInitializerType;
    typename BayesianInitializerType::Pointer bayesianInitializer = BayesianInitializerType::New();

    bayesianInitializer->SetInput( reader->GetOutput() );
    //        bayesianInitializer->SetNumberOfClasses( numClass );// Background, WM, GM and CSF
    bayesianInitializer->SetNumberOfClasses( 3 );
    bayesianInitializer->Update();

    typedef itk::BayesianClassifierImageFilter< VectorInputImageType,OutputPixelType, PosteriorType,PriorType >   ClassifierFilterType;
    typename ClassifierFilterType::Pointer bayesClassifier = ClassifierFilterType::New();

    bayesClassifier->SetInput( bayesianInitializer->GetOutput() );

    if (priorsImage == "Multiple Sclerosis DTI Lesions") {
        string priorsTemplate = "";
        if ((mapType == "FractionalAnisotropy") & (mapResolution == "1mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-FA-1mm.nii.gz";
        }else if ((mapType == "MeanDiffusivity") & (mapResolution == "1mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-MD-1mm.nii.gz";
        }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "1mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-RA-1mm.nii.gz";
        }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "1mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-PerD-1mm.nii.gz";
        }else if ((mapType == "ParallelDiffusivity") & (mapResolution == "1mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-ParD-1mm.nii.gz";
        }else if ((mapType == "FractionalAnisotropy") & (mapResolution == "2mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-FA-2mm.nii.gz";
        }else if ((mapType == "MeanDiffusivity") & (mapResolution == "2mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-MD-2mm.nii.gz";
        }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "2mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-RA-2mm.nii.gz";
        }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "2mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-PerD-2mm.nii.gz";
        }else if ((mapType == "ParallelDiffusivity") & (mapResolution == "2mm")) {
            priorsTemplate="USP-ICBM-MS-BayesPriors-ParD-2mm.nii.gz";
        }

        //    Read the DTI Statistical Template
        stringstream TEMPLATE_path;
        TEMPLATE_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<priorsTemplate;
        typename PriorsReaderType::Pointer priorsReader = PriorsReaderType::New();
        priorsReader->SetFileName(TEMPLATE_path.str().c_str());
        priorsReader->Update();

        //Setting the priors probability in the Bayesian framework
        bayesClassifier->SetPriors(priorsReader->GetOutput());

        // Write the output file
        typedef itk::ImageFileWriter<ClassifierFilterType::OutputImageType> WriterType;
        typename WriterType::Pointer writer = WriterType::New();
        writer->SetFileName( outputLabel.c_str() );
        writer->SetInput( bayesClassifier->GetOutput() );
        writer->SetUseCompression(1);
        writer->Update();

        return EXIT_SUCCESS;
    }

    // Write the output file
    typedef itk::ImageFileWriter<ClassifierFilterType::OutputImageType> WriterType;
    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputLabel.c_str() );
    writer->SetInput( bayesClassifier->GetOutput() );
    writer->SetUseCompression(1);
    writer->Update();

    return EXIT_SUCCESS;
    //    }

}

} // end of anonymous namespace

int main( int argc, char * argv[] )
{
    PARSE_ARGS;

    itk::ImageIOBase::IOPixelType     pixelType;
    itk::ImageIOBase::IOComponentType componentType;

    try
    {
        itk::GetImageType(inputVolume, pixelType, componentType);

        // This filter handles all types on input, but only produces
        // signed types
        switch( componentType )
        {
        case itk::ImageIOBase::UCHAR:
            return DoIt( argc, argv, static_cast<unsigned char>(0) );
            break;
        case itk::ImageIOBase::CHAR:
            return DoIt( argc, argv, static_cast<char>(0) );
            break;
        case itk::ImageIOBase::USHORT:
            return DoIt( argc, argv, static_cast<unsigned short>(0) );
            break;
        case itk::ImageIOBase::SHORT:
            return DoIt( argc, argv, static_cast<short>(0) );
            break;
        case itk::ImageIOBase::UINT:
            return DoIt( argc, argv, static_cast<unsigned int>(0) );
            break;
        case itk::ImageIOBase::INT:
            return DoIt( argc, argv, static_cast<int>(0) );
            break;
        case itk::ImageIOBase::ULONG:
            return DoIt( argc, argv, static_cast<unsigned long>(0) );
            break;
        case itk::ImageIOBase::LONG:
            return DoIt( argc, argv, static_cast<long>(0) );
            break;
        case itk::ImageIOBase::FLOAT:
            return DoIt( argc, argv, static_cast<float>(0) );
            break;
        case itk::ImageIOBase::DOUBLE:
            return DoIt( argc, argv, static_cast<double>(0) );
            break;
        case itk::ImageIOBase::UNKNOWNCOMPONENTTYPE:
        default:
            std::cout << "unknown component type" << std::endl;
            break;
        }
    }

    catch( itk::ExceptionObject & excep )
    {
        std::cerr << argv[0] << ": exception caught !" << std::endl;
        std::cerr << excep << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
