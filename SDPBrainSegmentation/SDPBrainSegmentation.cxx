//ITK
#include "itkImageFileWriter.h"
#include "itkVectorImage.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkCastImageFilter.h"
#include "itkImageRegionConstIterator.h"
#include "itkImageRegionIterator.h"

#include "itkPluginUtilities.h"

#include "SDPBrainSegmentationCLP.h"

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



using namespace  std;

// Use an anonymous namespace to keep class types and function names
// from colliding when module is used as shared object module.  Every
// thing should be in an anonymous namespace except for the module
// entry point, e.g. main()
//
namespace
{

template <class T>
bool StatisticalZScoreThreshold(std::vector<T> voxelStack, float voxelIntensity, float zThreshold){
    T mean = 0;
    T STD = 0;
    for (unsigned int i = 0; i < voxelStack.size(); ++i) {
        mean += voxelStack[i];
    }
    mean = mean/voxelStack.size();

    for (unsigned int i = 0; i < voxelStack.size(); ++i) {
        STD += (voxelStack[i] - mean)*(voxelStack[i] - mean);
    }
    STD = std::sqrt(STD/voxelStack.size());

    //Do the Z-Score evaluation
    double z= 0;
    double x = voxelIntensity;
    if (STD == static_cast<T>(0)) {
        return false;
    }else{
        z = (x - mean)/STD;
        if (z <= (-1)*zThreshold) {
            std::cout<<"Z: "<<z<<std::endl;
            return true;
        }else{
            return false;
        }
    }
}

template <class T>
int DoIt( int argc, char * argv[], T )
{

#ifdef _WIN32
    char* HOME_DIR=getenv("HOMEPATH");
#else
    char* HOME_DIR=getenv("HOME");
#endif

    PARSE_ARGS;    
    const unsigned int                                    Dimension=3;
    typedef    T                                          InputPixelType;
    typedef    unsigned char                              OutputPixelType;
    //        typedef    T                              OutputPixelType;

    typedef itk::Image<InputPixelType,  Dimension>        InputImageType;
    typedef itk::VectorImage<InputPixelType, Dimension>   StatisticalImageType;
    typedef itk::Image<OutputPixelType, Dimension>        OutputImageType;

    typedef itk::ImageFileReader<InputImageType>          ReaderType;
    typedef itk::ImageFileReader<StatisticalImageType>    StatisticalReaderType;

    typename ReaderType::Pointer inputReader = ReaderType::New();
    inputReader->SetFileName( inputVolume.c_str() );
    inputReader->Update();

    typename StatisticalReaderType::Pointer statReader = StatisticalReaderType::New();

    string statTemplate = "";
    if ((mapType == "FractionalAnisotropy") & (mapResolution == "1mm")) {
        statTemplate="USP-ICBM-20-N16-statFA-1mm.nii.gz";
    }else if ((mapType == "MeanDiffusivity") & (mapResolution == "1mm")) {
        statTemplate="USP-ICBM-20-N16-statMD-1mm.nii.gz";
    }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "1mm")) {
        statTemplate="USP-ICBM-20-N16-statRA-1mm.nii.gz";
    }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "1mm")) {
        statTemplate="USP-ICBM-20-N16-statPerD-1mm.nii.gz";
    }else if ((mapType == "ParallelDiffusivity") & (mapResolution == "1mm")) {
        statTemplate="USP-ICBM-20-N16-statParD-1mm.nii.gz";
    }else if ((mapType == "FractionalAnisotropy") & (mapResolution == "2mm")) {
        statTemplate="USP-ICBM-20-N16-statFA-2mm.nii.gz";
    }else if ((mapType == "MeanDiffusivity") & (mapResolution == "2mm")) {
        statTemplate="USP-ICBM-20-N16-statMD-2mm.nii.gz";
    }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "2mm")) {
        statTemplate="USP-ICBM-20-N16-statRA-2mm.nii.gz";
    }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "2mm")) {
        statTemplate="USP-ICBM-20-N16-statPerD-2mm.nii.gz";
    }else if ((mapType == "ParallelDiffusivity") & (mapResolution == "2mm")) {
        statTemplate="USP-ICBM-20-N16-statParD-2mm.nii.gz";
    }

    //    Read the DTI Statistical Template
    stringstream TEMPLATE_path;
    TEMPLATE_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<statTemplate;
    statReader->SetFileName(TEMPLATE_path.str().c_str());
    statReader->Update();


    //    Start brain statistical segmentation
    //    Create the Probability Image
    typename InputImageType::Pointer probabilityVolume = InputImageType::New();
    probabilityVolume->CopyInformation( inputReader->GetOutput() );
    probabilityVolume->SetBufferedRegion( inputReader->GetOutput()->GetBufferedRegion() );
    probabilityVolume->SetRequestedRegion( inputReader->GetOutput()->GetRequestedRegion() );
    probabilityVolume->Allocate();

    //     Set iterators
    typedef itk::ImageRegionConstIterator<StatisticalImageType>    ConstRegionIteratorType;
    typedef itk::ImageRegionIterator<InputImageType>               RegionIteratorType;
    ConstRegionIteratorType     statIt(statReader->GetOutput(), statReader->GetOutput()->GetRequestedRegion());
    RegionIteratorType          probIt(probabilityVolume, probabilityVolume->GetRequestedRegion());
    RegionIteratorType          inputIt(inputReader->GetOutput(), inputReader->GetOutput()->GetRequestedRegion());

    unsigned int numberOfComponents = statReader->GetOutput()->GetNumberOfComponentsPerPixel();

    std::cout<<"DTI statistical template loaded...NumberOfComponents: "<<statReader->GetOutput()->GetNumberOfComponentsPerPixel()<<std::endl;

    statIt.GoToBegin();
    probIt.GoToBegin();
    inputIt.GoToBegin();
    while (!statIt.IsAtEnd()) {
        //        Jump voxel with null values
        if (inputIt.Get()!=0) {
            std::vector<InputPixelType> voxelStack;
            for (int numComp = 0; numComp < numberOfComponents; ++numComp) {
                voxelStack.push_back(statIt.Get()[numComp]);
            }

            if (statMethod == "Z-Score") {
                if (StatisticalZScoreThreshold(voxelStack, static_cast<float>(inputIt.Get()), zThreshold)) {
                    probIt.Set(1);
                }
                ++statIt;
                ++probIt;
                ++inputIt;
            }
        }else{
            ++statIt;
            ++probIt;
            ++inputIt;
        }

    }

    //    Cast the probability volume to Label type
    typedef itk::CastImageFilter<InputImageType, OutputImageType> CastType;
    typename CastType::Pointer caster = CastType::New();
    caster->SetInput(probabilityVolume);


    typedef itk::ImageFileWriter<OutputImageType> WriterType;
    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputLabel.c_str() );
    writer->SetInput( caster->GetOutput() );
    writer->SetUseCompression(1);
    writer->Update();

    return EXIT_SUCCESS;
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
