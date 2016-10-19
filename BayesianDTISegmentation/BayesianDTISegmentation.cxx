#include "itkImageFileWriter.h"
#include "itkImage.h"
#include "itkImageRegionConstIterator.h"
#include "itkImageRegionIterator.h"

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

//Segmentation Methods
#include "itkBayesianClassifierInitializationImageFilter.h"
#include "itkBayesianClassifierImageFilter.h"

#include "itkPluginUtilities.h"

#include "BayesianDTISegmentationCLP.h"

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

    typedef float                          InputPixelType;
    typedef unsigned char                  OutputPixelType;
    typedef float                          PriorType;
    typedef float                          PosteriorType;
    const unsigned int                     Dimension=3;

    typedef itk::Image<InputPixelType,  Dimension>              InputImageType;
    typedef itk::VectorImage< InputPixelType, Dimension >       VectorInputImageType;

    typedef itk::ImageFileReader<InputImageType>                ReaderType;
    typedef itk::ImageFileReader<VectorInputImageType>          PriorsReaderType;

    typename ReaderType::Pointer inputReader = ReaderType::New();
    inputReader->SetFileName( inputVolume.c_str() );
    inputReader->Update();

    typename ReaderType::Pointer referenceReader = ReaderType::New();
    referenceReader->SetFileName( referenceVolume.c_str() );
    referenceReader->Update();

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
    if (mapType=="FractionalAnisotropy") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(1.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (mapType=="MeanDiffusivity") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(-1.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (mapType=="RelativeAnisotropy") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(1.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (mapType=="ParallelDiffusivity") {
        cleanVoxels->SetLower(static_cast<InputPixelType>(-1.0));
        cleanVoxels->SetUpper(static_cast<InputPixelType>(0.0));
        cleanVoxels->SetOutsideValue(static_cast<InputPixelType>(0.0));
    }else if (mapType=="VolumeRatio") {
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
    typedef itk::LogisticContrastEnhancementImageFilter<InputImageType, InputImageType> OptimumSigmoidParametersType;
    typename OptimumSigmoidParametersType::Pointer optSigmoid = OptimumSigmoidParametersType::New();
    optSigmoid->SetInput(mask->GetOutput());
    if (thrMethod == "MaxEntropy") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::MAXENTROPY);
    }else if (thrMethod == "Otsu") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::OTSU);
    }else if (thrMethod == "Renyi") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::RENYI);
    }else if (thrMethod == "Moments") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::MOMENTS);
    }else if (thrMethod == "IsoData") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::ISODATA);
    }else if (thrMethod == "Yen") {
        optSigmoid->SetThresholdMethod(OptimumSigmoidParametersType::YEN);
    }
    optSigmoid->Update();
    std::cout<<"Optimum [Alpha,Beta] = [ "<<optSigmoid->GetAlpha()<<" , "<<optSigmoid->GetBeta()<<" ]"<<std::endl;

    //Sigmoid lesion enhancement step
    typedef itk::SigmoidImageFilter<InputImageType,InputImageType> SigmoidType;
    typename SigmoidType::Pointer sigmoid = SigmoidType::New();
    sigmoid->SetInput(rescaler->GetOutput());
    sigmoid->SetOutputMinimum(0.0);
    sigmoid->SetOutputMaximum(1.0);
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

    //Bayesian Segmentation Approach
    typedef itk::BayesianClassifierInitializationImageFilter< InputImageType >         BayesianInitializerType;
    typename BayesianInitializerType::Pointer bayesianInitializer = BayesianInitializerType::New();

    bayesianInitializer->SetInput( maskWM->GetOutput() );
    bayesianInitializer->SetNumberOfClasses( 2 ); // Always set to 2 classes: Lesion and non-Lesions probability
    bayesianInitializer->Update();

    typedef itk::BayesianClassifierImageFilter< VectorInputImageType,OutputPixelType, PosteriorType,PriorType >   ClassifierFilterType;
    typename ClassifierFilterType::Pointer bayesClassifier = ClassifierFilterType::New();

    bayesClassifier->SetInput( bayesianInitializer->GetOutput() );

    string priorsTemplate = "";
    if (priorsImage == "Multiple Sclerosis Lesions") {
        if (mapResolution == "1mm") {
            priorsTemplate="USP-ICBM-MSLesionPriors-46-1mm.nii.gz";
        }else {
            priorsTemplate="USP-ICBM-MSLesionPriors-46-2mm.nii.gz";
        }
        //    Read the MS lesion priors probability image
        stringstream priors_path;
        priors_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<priorsTemplate;
        typename PriorsReaderType::Pointer priorsReader = PriorsReaderType::New();
        priorsReader->SetFileName(priors_path.str().c_str());
        priorsReader->Update();

        bayesClassifier->SetPriors(priorsReader->GetOutput());
    }


    // Write the output file
    typedef itk::ImageFileWriter<ClassifierFilterType::OutputImageType> WriterType;
    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputLabel.c_str() );
    writer->SetInput( bayesClassifier->GetOutput() );
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
