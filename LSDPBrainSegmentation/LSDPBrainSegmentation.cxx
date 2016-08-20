//ITK
#include "itkImageFileWriter.h"
#include "itkVectorImage.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkCastImageFilter.h"
#include "itkNeighborhoodIterator.h"

#include "itkPluginUtilities.h"

#include "LSDPBrainSegmentationCLP.h"

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
bool LocalDecision(float tScore, float tThr, string mapType){
    if (mapType == "FractionalAnisotropy") {
        return (tScore <= (-1)*tThr);
    }
    if (mapType == "MeanDiffusivity") {
        return (tScore >= tThr);
    }
    if (mapType == "RelativeAnisotropy") {
        return (tScore <= (-1)*tThr);
    }
    if (mapType == "PerpendicularDiffusivity") {
        return (tScore >= tThr);
    }
    if (mapType == "VolumeRatio") {
        return (tScore >= tThr);
    }
    return false;
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

    typedef itk::Image<InputPixelType,  Dimension>          InputImageType;
    typedef itk::Image<OutputPixelType, Dimension>          OutputImageType;

    typedef itk::ImageFileReader<InputImageType>             ReaderType;
    typedef itk::ImageFileReader<OutputImageType>            LabelReaderType;

    typename ReaderType::Pointer inputReader = ReaderType::New();
    inputReader->SetFileName( inputVolume.c_str() );
    inputReader->Update();

    typename LabelReaderType::Pointer inputLabelReader = LabelReaderType::New();
    inputLabelReader->SetFileName( inputLabel.c_str() );
    inputLabelReader->Update();

    typename ReaderType::Pointer meanStatReader = ReaderType::New();
    typename ReaderType::Pointer stdStatReader = ReaderType::New();

    string meanStatTemplate = "";
    string stdStatTemplate = "";
    if ((mapType == "FractionalAnisotropy") & (mapResolution == "1mm")) {
        meanStatTemplate="USP-ICBM-FAmean-131-1mm.nii.gz";
        stdStatTemplate="USP-ICBM-FAstd-131-1mm.nii.gz";
    }else if ((mapType == "MeanDiffusivity") & (mapResolution == "1mm")) {
        meanStatTemplate="USP-ICBM-MDmean-131-1mm.nii.gz";
        stdStatTemplate="USP-ICBM-MDstd-131-1mm.nii.gz";
    }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "1mm")) {
        meanStatTemplate="USP-ICBM-RAmean-131-1mm.nii.gz";
        stdStatTemplate="USP-ICBM-RAstd-131-1mm.nii.gz";
    }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "1mm")) {
        meanStatTemplate="USP-ICBM-PerpDiffmean-131-1mm.nii.gz";
        stdStatTemplate="USP-ICBM-PerpDiffstd-131-1mm.nii.gz";
    }else if ((mapType == "VolumeRatio") & (mapResolution == "1mm")) {
        meanStatTemplate="USP-ICBM-VRmean-131-1mm.nii.gz";
        stdStatTemplate="USP-ICBM-VRstd-131-1mm.nii.gz";
    }else if ((mapType == "FractionalAnisotropy") & (mapResolution == "2mm")) {
        meanStatTemplate="USP-ICBM-FAmean-131-2mm.nii.gz";
        stdStatTemplate="USP-ICBM-FAstd-131-2mm.nii.gz";
    }else if ((mapType == "MeanDiffusivity") & (mapResolution == "2mm")) {
        meanStatTemplate="USP-ICBM-MDmean-131-2mm.nii.gz";
        stdStatTemplate="USP-ICBM-MDstd-131-2mm.nii.gz";
    }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "2mm")) {
        meanStatTemplate="USP-ICBM-RAmean-131-2mm.nii.gz";
        stdStatTemplate="USP-ICBM-RAstd-131-2mm.nii.gz";
    }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "2mm")) {
        meanStatTemplate="USP-ICBM-PerpDiffmean-131-2mm.nii.gz";
        stdStatTemplate="USP-ICBM-PerpDiffstd-131-2mm.nii.gz";
    }else if ((mapType == "VolumeRatio") & (mapResolution == "2mm")) {
        meanStatTemplate="USP-ICBM-VRmean-131-2mm.nii.gz";
        stdStatTemplate="USP-ICBM-VRstd-131-2mm.nii.gz";
    }

    //    Read the DTI Statistical Template
    stringstream meanTEMPLATE_path, stdTEMPLATE_path;
    meanTEMPLATE_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<meanStatTemplate;
    stdTEMPLATE_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<stdStatTemplate;
    meanStatReader->SetFileName(meanTEMPLATE_path.str().c_str());
    stdStatReader->SetFileName(stdTEMPLATE_path.str().c_str());
    meanStatReader->Update();
    stdStatReader->Update();


    //    Start brain statistical segmentation
    //    Create the Probability Image
    typename InputImageType::Pointer probabilityVolume = InputImageType::New();
    probabilityVolume->CopyInformation( inputReader->GetOutput() );
    probabilityVolume->SetBufferedRegion( inputReader->GetOutput()->GetBufferedRegion() );
    probabilityVolume->SetRequestedRegion( inputReader->GetOutput()->GetRequestedRegion() );
    probabilityVolume->Allocate();

    //     Set iterators
    typedef itk::NeighborhoodIterator<OutputImageType>              NeighborOutputIteratorType;
    typedef itk::NeighborhoodIterator<InputImageType>               NeighborInputIteratorType;
    typename NeighborInputIteratorType::RadiusType radius;
    radius.Fill(1);
    NeighborOutputIteratorType       labelIt(radius, inputLabelReader->GetOutput(), inputLabelReader->GetOutput()->GetRequestedRegion());
    NeighborInputIteratorType        meanStatIt(radius, meanStatReader->GetOutput(), meanStatReader->GetOutput()->GetRequestedRegion());
    NeighborInputIteratorType        stdStatIt(radius, stdStatReader->GetOutput(), stdStatReader->GetOutput()->GetRequestedRegion());
    NeighborInputIteratorType        probIt(radius, probabilityVolume, probabilityVolume->GetRequestedRegion());
    NeighborInputIteratorType        inputIt(radius, inputReader->GetOutput(), inputReader->GetOutput()->GetRequestedRegion());

    int iteration = 5;
    while (iteration>0) {
        meanStatIt.GoToBegin();
        stdStatIt.GoToBegin();
        probIt.GoToBegin();
        inputIt.GoToBegin();
        labelIt.GoToBegin();
        float tScore=0.0;
        while (!labelIt.IsAtEnd()) {
            //Jump voxels with zero values
            if (labelIt.GetCenterPixel()!=static_cast<OutputImageType::PixelType>(0)) {
                //Check all 3D neighborhood for diffusivity abnormalities
                for(unsigned int i = 0; i < 27; i++)
                {
                    if (labelIt.GetPixel(i)==static_cast<OutputImageType::PixelType>(0)) {
                        tScore=((inputIt.GetPixel(i)-meanStatIt.GetPixel(i))/stdStatIt.GetPixel(i));
                        //Calculate the threshold based on the type of diffusivity map
                        if (LocalDecision(tScore,tThreshold, mapType)) {
                            probIt.SetPixel(i, 1);
                        }
                    }else{
                        //Adding the previous FLAIR lesion label into the final label image
                        probIt.SetPixel(i, 2);
                    }
                }
                ++meanStatIt;
                ++stdStatIt;
                ++probIt;
                ++inputIt;
                ++labelIt;
            }else{
                ++meanStatIt;
                ++stdStatIt;
                ++probIt;
                ++inputIt;
                ++labelIt;
            }
        }
        iteration--;
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
