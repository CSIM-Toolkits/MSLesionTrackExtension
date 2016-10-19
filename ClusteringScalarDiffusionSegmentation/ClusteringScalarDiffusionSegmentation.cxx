#include "itkImageFileWriter.h"
#include "itkStatisticsImageFilter.hxx"

// Utils
#include "itkRescaleIntensityImageFilter.h"
#include "itkAbsImageFilter.h"
#include "itkMaskImageFilter.h"

//Histogram Matching
#include "itkHistogramMatchingImageFilter.h"

//Substract Image Filter
#include "itkSubtractImageFilter.h"

//Threshold Image Filter
#include "itkThresholdImageFilter.h"

//Sigmoid Image Enhancement
#include "itkLogisticContrastEnhancementImageFilter.h"
#include "itkSigmoidImageFilter.h"

//Clustering Methods
#include "itkScalarImageKmeansImageFilter.h"

//MRF Refinement
#include "itkMRFImageFilter.h"
#include "itkDistanceToCentroidMembershipFunction.h"
#include "itkMinimumDecisionRule.h"
#include "itkComposeImageFilter.h"

#include "itkPluginUtilities.h"

#include "ClusteringScalarDiffusionSegmentationCLP.h"

#ifdef _WIN32
#define STATISTICALTEMPLATESFOLDER "\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates"
#define FIBERBUNDLESTEMPLATESFOLDER "\\MSLesionTrack-Data\\WMTracts-Templates"
#define WHITEMATTERTEMPLATESFOLDER "\\MSLesionTrack-Data\\Structural-Templates"
#define PATH_SEPARATOR "\\"
#define PATH_SEPARATOR_CHAR '\\'
#define DEL_CMD "del /Q "
#define MOVE_CMD "move "
#else
#define STATISTICALTEMPLATESFOLDER "/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates"
#define FIBERBUNDLESTEMPLATESFOLDER "/MSLesionTrack-Data/WMTracts-Templates"
#define WHITEMATTERTEMPLATESFOLDER "/MSLesionTrack-Data/Structural-Templates"
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

    typedef    T                              InputPixelType;
    typedef    unsigned char                  OutputPixelType;

    typedef itk::Image<InputPixelType,  3>    InputImageType;
    typedef itk::Image<OutputPixelType, 3>    OutputImageType;

    typedef itk::ImageFileReader<InputImageType>  ReaderType;
    typedef itk::ImageFileWriter<OutputImageType> WriterType;


    typename ReaderType::Pointer inputReader = ReaderType::New();
    inputReader->SetFileName( inputVolume.c_str() );

    typename ReaderType::Pointer referenceReader = ReaderType::New();
    referenceReader->SetFileName( referenceVolume.c_str() );

    typename ReaderType::Pointer maskReader = ReaderType::New();
    typename ReaderType::Pointer wmReader = ReaderType::New();

    //Histogram matching step
    typedef itk::HistogramMatchingImageFilter<InputImageType, InputImageType> HistogramMatchType;
    typename HistogramMatchType::Pointer histogramMatch = HistogramMatchType::New();
    histogramMatch->SetSourceImage(inputReader->GetOutput());
    histogramMatch->SetReferenceImage(referenceReader->GetOutput());
    histogramMatch->SetNumberOfHistogramLevels(128);
    histogramMatch->SetNumberOfMatchPoints(10000);

    //Image subtraction with the DTI atlas
    typedef itk::SubtractImageFilter<InputImageType,InputImageType, InputImageType> SubtractType;
    typename SubtractType::Pointer subtract = SubtractType::New();
    subtract->SetInput1(referenceReader->GetOutput());
    subtract->SetInput2(histogramMatch->GetOutput());

    //Cleaning unrelated differences from the difference image
    typedef itk::ThresholdImageFilter<InputImageType>         ThresholderType;
    typename ThresholderType::Pointer cleanVoxels = ThresholderType::New();
    cleanVoxels->SetInput(subtract->GetOutput());
    if (dtiMap=="FractionalAnisotropy") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(1.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (dtiMap=="MeanDiffusivity") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(-1.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (dtiMap=="RelativeAnisotropy") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(1.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (dtiMap=="PerpendicularDiffusivity") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(-1.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (dtiMap=="VolumeRatio") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(-1.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }
    cleanVoxels->Update();

    //Return absolute pixel values image
    typedef itk::AbsImageFilter<InputImageType, InputImageType> AbsoluteImageType;
    typename AbsoluteImageType::Pointer abs = AbsoluteImageType::New();
    abs->SetInput(cleanVoxels->GetOutput());

    //Rescale pixel intensity to [0,1] range
    typedef itk::RescaleIntensityImageFilter<InputImageType, InputImageType> RescalerType;
    typename RescalerType::Pointer rescaler = RescalerType::New();
    rescaler->SetOutputMinimum(0.0);
    rescaler->SetOutputMaximum(1.0);
    rescaler->SetInput(abs->GetOutput());

    //Mask white matter core fiber bundles
    //Read mask image file
    stringstream maskFile_path;
    if (mapResolution == "1mm") {
        maskFile_path<<HOME_DIR<<FIBERBUNDLESTEMPLATESFOLDER<<PATH_SEPARATOR<<"JHU-ICBM-labels-1mm-mask.nii.gz";
    }else{
        maskFile_path<<HOME_DIR<<FIBERBUNDLESTEMPLATESFOLDER<<PATH_SEPARATOR<<"JHU-ICBM-labels-2mm-mask.nii.gz";
    }
    maskReader->SetFileName(maskFile_path.str().c_str());
    maskReader->Update();

    //Apply fiber bundles mask
    typedef itk::MaskImageFilter<InputImageType, InputImageType>    MaskFilterType;
    typename MaskFilterType::Pointer mask = MaskFilterType::New();
    mask->SetInput(rescaler->GetOutput());
    mask->SetMaskImage(maskReader->GetOutput());

    //Find Sigmoid optimum parameters
    typedef itk::LogisticContrastEnhancementImageFilter<InputImageType, InputImageType> LogisticParametersType;
    typename LogisticParametersType::Pointer optSigmoid = LogisticParametersType::New();
    optSigmoid->SetInput(mask->GetOutput());
    if (thrMethod == "MaxEntropy") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::MAXENTROPY);
    }else if (thrMethod == "Otsu") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::OTSU);
    }else if (thrMethod == "Renyi") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::RENYI);
    }else if (thrMethod == "Moments") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::MOMENTS);
    }else if (thrMethod == "IsoData") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::ISODATA);
    }else if (thrMethod == "Yen") {
        optSigmoid->SetThresholdMethod(LogisticParametersType::YEN);
    }
    optSigmoid->Update();
    std::cout<<"Optimum [Alpha,Beta] = [ "<<optSigmoid->GetAlpha()<<" , "<<optSigmoid->GetBeta()<<" ]"<<std::endl;

    //Sigmoid lesion enhancement step
    typedef itk::SigmoidImageFilter<InputImageType,InputImageType> SigmoidType;
    typename SigmoidType::Pointer sigmoid = SigmoidType::New();
    sigmoid->SetInput(rescaler->GetOutput());
    sigmoid->SetOutputMinimum(0);
    sigmoid->SetOutputMaximum(1);
    sigmoid->SetAlpha(optSigmoid->GetAlpha());
    sigmoid->SetBeta(optSigmoid->GetBeta());

    //Mask the whole white matter
    stringstream wmFile_path;
    if (mapResolution == "1mm") {
        wmFile_path<<HOME_DIR<<WHITEMATTERTEMPLATESFOLDER<<PATH_SEPARATOR<<"MNI152_T1_1mm_brain_wm.nii.gz";
    }else{
        wmFile_path<<HOME_DIR<<WHITEMATTERTEMPLATESFOLDER<<PATH_SEPARATOR<<"MNI152_T1_2mm_brain_wm.nii.gz";
    }
    wmReader->SetFileName(wmFile_path.str().c_str());
    wmReader->Update();

    //Apply whole white matter mask
    typedef itk::MaskImageFilter<InputImageType, InputImageType>    MaskFilterType;
    typename MaskFilterType::Pointer maskWM = MaskFilterType::New();
    maskWM->SetInput(sigmoid->GetOutput());
    maskWM->SetMaskImage(wmReader->GetOutput());

    //Lesion segmentation by clustering approach
    //K-Means Segmentation Approach
    typedef itk::ScalarImageKmeansImageFilter< InputImageType > KMeansFilterType;
    typename KMeansFilterType::Pointer kmeansFilter = KMeansFilterType::New();
    kmeansFilter->SetInput( maskWM->GetOutput() );
    const unsigned int numberOfInitialClasses = numClass;

    typedef itk::StatisticsImageFilter<InputImageType> StatisticsType;
    typename StatisticsType::Pointer statImage = StatisticsType::New();
    statImage->SetInput(sigmoid->GetOutput());
    statImage->Update();
    double classStep=(2.0*statImage->GetSigma())/static_cast<InputPixelType>(numberOfInitialClasses);
    //        double classStep=(statImage->GetMaximum()-statImage->GetMinimum())/static_cast<InputPixelType>(numberOfInitialClasses);
    for( unsigned k=1; k <= numberOfInitialClasses; k++ )
    {
        kmeansFilter->AddClassWithInitialMean(classStep*k);
        std::cout<<"initClassGuess["<<k<<"]="<<classStep*k<<std::endl;
    }

    kmeansFilter->Update();

    typename KMeansFilterType::ParametersType estimatedMeans = kmeansFilter->GetFinalMeans();
    const unsigned int numberOfClasses = estimatedMeans.Size();
    for ( unsigned int i = 0; i < numberOfClasses; ++i )
    {
        std::cout << "cluster[" << i << "] ";
        std::cout << "    estimated mean : " << estimatedMeans[i] << std::endl;
    }


    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputVolume.c_str() );
    writer->SetInput( kmeansFilter->GetOutput() );
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
