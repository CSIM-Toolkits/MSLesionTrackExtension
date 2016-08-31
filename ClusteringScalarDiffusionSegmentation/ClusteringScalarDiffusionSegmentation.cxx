#include "itkImageFileWriter.h"

//Histogram Matching
#include "itkHistogramMatchingImageFilter.h"

//Substract Image Filter
#include "itkSubtractImageFilter.h"

//Sigmoid Image Enhancement
#include "itkSigmoidImageFilter.h"

//Clustering Methods
#include "itkScalarImageKmeansImageFilter.h"

#include "itkPluginUtilities.h"

#include "ClusteringScalarDiffusionSegmentationCLP.h"

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

  typedef    T                              InputPixelType;
  typedef    unsigned char                  OutputPixelType;

  typedef itk::Image<InputPixelType,  3>    InputImageType;
  typedef itk::Image<OutputPixelType, 3>    OutputImageType;

  typedef itk::ImageFileReader<InputImageType>  ReaderType;
  typedef itk::ImageFileWriter<OutputImageType> WriterType;


  typename ReaderType::Pointer reader = ReaderType::New();
  reader->SetFileName( inputVolume.c_str() );

  string meanStatTemplate = "";
  if ((mapType == "FractionalAnisotropy") & (mapResolution == "1mm")) {
      meanStatTemplate="USP-ICBM-FAmean-131-1mm.nii.gz";
  }else if ((mapType == "MeanDiffusivity") & (mapResolution == "1mm")) {
      meanStatTemplate="USP-ICBM-MDmean-131-1mm.nii.gz";
  }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "1mm")) {
      meanStatTemplate="USP-ICBM-RAmean-131-1mm.nii.gz";
  }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "1mm")) {
      meanStatTemplate="USP-ICBM-PerpDiffmean-131-1mm.nii.gz";
  }else if ((mapType == "VolumeRatio") & (mapResolution == "1mm")) {
      meanStatTemplate="USP-ICBM-VRmean-131-1mm.nii.gz";
  }else if ((mapType == "FractionalAnisotropy") & (mapResolution == "2mm")) {
      meanStatTemplate="USP-ICBM-FAmean-131-2mm.nii.gz";
  }else if ((mapType == "MeanDiffusivity") & (mapResolution == "2mm")) {
      meanStatTemplate="USP-ICBM-MDmean-131-2mm.nii.gz";
  }else if ((mapType == "RelativeAnisotropy") & (mapResolution == "2mm")) {
      meanStatTemplate="USP-ICBM-RAmean-131-2mm.nii.gz";
  }else if ((mapType == "PerpendicularDiffusivity") & (mapResolution == "2mm")) {
      meanStatTemplate="USP-ICBM-PerpDiffmean-131-2mm.nii.gz";
  }else if ((mapType == "VolumeRatio") & (mapResolution == "2mm")) {
      meanStatTemplate="USP-ICBM-VRmean-131-2mm.nii.gz";
  }

  //    Read the DTI Template
  typename ReaderType::Pointer templateReader = ReaderType::New();
  stringstream meanTEMPLATE_path;
  meanTEMPLATE_path<<HOME_DIR<<STATISTICALTEMPLATESFOLDER<<PATH_SEPARATOR<<meanStatTemplate;
  templateReader->SetFileName(meanTEMPLATE_path.str().c_str());
//  templateReader->Update();

  //Histogram matching step
    typedef itk::HistogramMatchingImageFilter<InputImageType, InputImageType> HistogramMatchType;
  typename HistogramMatchType::Pointer histogramMatch = HistogramMatchType::New();
  histogramMatch->SetSourceImage(reader->GetOutput());
  histogramMatch->SetReferenceImage(templateReader->GetOutput());
  histogramMatch->SetNumberOfHistogramLevels(128);
  histogramMatch->SetNumberOfMatchPoints(10000);

  //Image subtraction with the DTI atlas
    typedef itk::SubtractImageFilter<InputImageType,InputImageType, InputImageType> SubtractType;
  typename SubtractType::Pointer subtract = SubtractType::New();
  subtract->SetInput1(templateReader->GetOutput());
  subtract->SetInput2(histogramMatch->GetOutput());

  //Sigmoid lesion enhancement step
    typedef itk::SigmoidImageFilter<InputImageType,InputImageType> SigmoidType;
  typename SigmoidType::Pointer sigmoid = SigmoidType::New();
  sigmoid->SetInput(subtract->GetOutput());
    sigmoid->SetOutputMinimum(0);
    sigmoid->SetOutputMaximum(1);
    //TODO Work on alpha and beta optimization!!!
    sigmoid->SetAlpha(alpha);
    sigmoid->SetBeta(beta);

  //Lesion segmentation by clustering approach
  if (clusterMethod == "KMeans") {
      //K-Means Segmentation Approach
      typedef itk::ScalarImageKmeansImageFilter< InputImageType > KMeansFilterType;
      typename KMeansFilterType::Pointer kmeansFilter = KMeansFilterType::New();
      kmeansFilter->SetInput( sigmoid->GetOutput() );
      const unsigned int numberOfInitialClasses = numClass;

      for( unsigned k=0; k < numberOfInitialClasses; k++ )
      {
          kmeansFilter->AddClassWithInitialMean(initMeans[k]);
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
  }else if (clusterMethod == "FuzzyCMean") {

  }

  //TODO Deixar esta parte final para o DTILesionTrack (Python)
  //White matter masking to reduce false positive ratio

  //Morphological closing to clean small signals

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
