#include "itkImageFileWriter.h"
#include "itkStatisticsImageFilter.hxx"

//Histogram Matching
#include "itkHistogramMatchingImageFilter.h"

//Substract Image Filter
#include "itkSubtractImageFilter.h"

//Threshold Image Filter
#include "itkThresholdImageFilter.h"

//Sigmoid Image Enhancement
#include "itkSigmoidParametersOptimizationImageCalculator.h"
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

//#ifdef _WIN32
//#define STATISTICALTEMPLATESFOLDER "\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates"
//#define PATH_SEPARATOR "\\"
//#define PATH_SEPARATOR_CHAR '\\'
//#define DEL_CMD "del /Q "
//#define MOVE_CMD "move "
//#else
//#define STATISTICALTEMPLATESFOLDER "/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates"
//#define PATH_SEPARATOR "/"
//#define PATH_SEPARATOR_CHAR '/'
//#define DEL_CMD "rm -f "
//#define MOVE_CMD "mv "
//#endif

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

//#ifdef _WIN32
//    char* HOME_DIR=getenv("HOMEPATH");
//#else
//    char* HOME_DIR=getenv("HOME");
//#endif

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
//      cleanVoxels->SetLower(static_cast<InputImageType::PixelType>(0.0));
//      cleanVoxels->SetUpper(static_cast<InputImageType::PixelType>(1.0));
//      cleanVoxels->SetOutsideValue(static_cast<InputImageType::PixelType>(0.0));
  }else if (dtiMap=="RelativeAnisotropy") {
//      cleanVoxels->SetLower(static_cast<InputImageType::PixelType>(0.0));
//      cleanVoxels->SetUpper(static_cast<InputImageType::PixelType>(1.0));
//      cleanVoxels->SetOutsideValue(static_cast<InputImageType::PixelType>(0.0));
  }else if (dtiMap=="ParallelDiffusivity") {
//      cleanVoxels->SetLower(static_cast<InputImageType::PixelType>(0.0));
//      cleanVoxels->SetUpper(static_cast<InputImageType::PixelType>(1.0));
//      cleanVoxels->SetOutsideValue(static_cast<InputImageType::PixelType>(0.0));
  }else if (dtiMap=="VolumeRatio") {
//      cleanVoxels->SetLower(static_cast<InputImageType::PixelType>(0.0));
//      cleanVoxels->SetUpper(static_cast<InputImageType::PixelType>(1.0));
//      cleanVoxels->SetOutsideValue(static_cast<InputImageType::PixelType>(0.0));
  }
  cleanVoxels->Update();

  //Find Sigmoid optimum parameters
  typedef itk::SigmoidParametersOptimizationImageCalculator<InputImageType> OptimumSigmoidParametersType;
  typename OptimumSigmoidParametersType::Pointer optSigmoid = OptimumSigmoidParametersType::New();
  optSigmoid->SetInput(cleanVoxels->GetOutput());
  //TODO VER SE TODOS OS MAPAS PODEM SER APLICADOS OS MESMO PARAMETROS PARA SIGMOID
  optSigmoid->SetMaximumAlpha(1.0);
  optSigmoid->SetMinimumAlpha(0.0);
//  optSigmoid->SetMaximumBeta();
//  optSigmoid->SetMinimumBeta();
  optSigmoid->Update();
  std::cout<<"Optimum [Alpha,Beta] = [ "<<optSigmoid->GetOptimumAlpha()<<" , "<<optSigmoid->GetOptimumBeta()<<" ]"<<std::endl;

  //Sigmoid lesion enhancement step
    typedef itk::SigmoidImageFilter<InputImageType,InputImageType> SigmoidType;
  typename SigmoidType::Pointer sigmoid = SigmoidType::New();
  sigmoid->SetInput(cleanVoxels->GetOutput());
    sigmoid->SetOutputMinimum(0);
    sigmoid->SetOutputMaximum(1);
    sigmoid->SetAlpha(optSigmoid->GetOptimumAlpha());
    sigmoid->SetBeta(optSigmoid->GetOptimumBeta());

  //Lesion segmentation by clustering approach
  if (clusterMethod == "KMeans") {
      //K-Means Segmentation Approach
      typedef itk::ScalarImageKmeansImageFilter< InputImageType > KMeansFilterType;
      typename KMeansFilterType::Pointer kmeansFilter = KMeansFilterType::New();
      kmeansFilter->SetInput( sigmoid->GetOutput() );
      const unsigned int numberOfInitialClasses = numClass;

      typedef itk::StatisticsImageFilter<InputImageType> StatisticsType;
      typename StatisticsType::Pointer statImage = StatisticsType::New();
      statImage->SetInput(sigmoid->GetOutput());
      statImage->Update();
      double classStep=statImage->GetSigma()/static_cast<InputPixelType>(numberOfInitialClasses);
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








    //Markov Random Field label refinement
      typedef itk::FixedArray<OutputPixelType,1>  ArrayPixelType;
      typedef itk::Image< ArrayPixelType, 3 > ArrayImageType;
      typedef itk::ComposeImageFilter<InputImageType, ArrayImageType> ScalarToArrayFilterType;

      typename ScalarToArrayFilterType::Pointer scalarToArrayFilter = ScalarToArrayFilterType::New();
      scalarToArrayFilter->SetInput( sigmoid->GetOutput() );

      typedef itk::MRFImageFilter< ArrayImageType, OutputImageType > MRFFilterType;

      MRFFilterType::Pointer mrfFilter = MRFFilterType::New();

      mrfFilter->SetInput( scalarToArrayFilter->GetOutput() );
      mrfFilter->SetNumberOfClasses( numberOfClasses );
      mrfFilter->SetMaximumNumberOfIterations( numberOfIterations );
      mrfFilter->SetErrorTolerance( 1e-7 );
      mrfFilter->SetSmoothingFactor( smoothingFactor );

      typedef itk::ImageClassifierBase<ArrayImageType,OutputImageType >   SupervisedClassifierType;
      SupervisedClassifierType::Pointer classifier = SupervisedClassifierType::New();

      typedef itk::Statistics::MinimumDecisionRule DecisionRuleType;
      DecisionRuleType::Pointer  classifierDecisionRule = DecisionRuleType::New();

      classifier->SetDecisionRule( classifierDecisionRule.GetPointer() );

      typedef itk::Statistics::DistanceToCentroidMembershipFunction< ArrayPixelType > MembershipFunctionType;
      typedef MembershipFunctionType::Pointer MembershipFunctionPointer;

      double meanDistance = 0;
      MembershipFunctionType::CentroidType centroid(1);
      for( unsigned int i=1; i <= numberOfClasses; i++ )
        {
        MembershipFunctionPointer membershipFunction = MembershipFunctionType::New();
//        centroid[0] = atof( argv[i+numberOfArgumentsBeforeMeans] );
//        centroid[0] = initMeans[i];
        centroid[0]=classStep*i;
        membershipFunction->SetCentroid( centroid );
        classifier->AddMembershipFunction( membershipFunction );
        meanDistance += static_cast< double > (centroid[0]);
        }
      if (numberOfClasses > 0)
        {
        meanDistance /= numberOfClasses;
        }
      else
        {
        std::cerr << "ERROR: numberOfClasses is 0" << std::endl;
        return EXIT_FAILURE;
        }
      mrfFilter->SetSmoothingFactor( smoothingFactor );
      mrfFilter->SetNeighborhoodRadius( 1 );

      std::vector< double > weights;
      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0); // This is the central pixel
      weights.push_back(1.5);
      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0);

      weights.push_back(1.5);
      weights.push_back(2.0);
      weights.push_back(1.5);
      weights.push_back(2.0);
      weights.push_back(0.0); // This is the central pixel
      weights.push_back(2.0);
      weights.push_back(1.5);
      weights.push_back(2.0);
      weights.push_back(1.5);

      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0); // This is the central pixel
      weights.push_back(1.5);
      weights.push_back(1.0);
      weights.push_back(1.5);
      weights.push_back(1.0);

      double totalWeight = 0;
      for(std::vector< double >::const_iterator wcIt = weights.begin(); wcIt != weights.end(); ++wcIt )
        {
        totalWeight += *wcIt;
        }
      for(std::vector< double >::iterator wIt = weights.begin(); wIt != weights.end(); ++wIt )
        {
        *wIt = static_cast< double > ( (*wIt) * meanDistance / (2 * totalWeight));
        }

      mrfFilter->SetMRFNeighborhoodWeight( weights );
        mrfFilter->SetClassifier( classifier );

        std::cout << "Number of Iterations : ";
        std::cout << mrfFilter->GetNumberOfIterations() << std::endl;
        std::cout << "Stop condition: " << std::endl;
        std::cout << "  (1) Maximum number of iterations " << std::endl;
        std::cout << "  (2) Error tolerance:  "  << std::endl;
        std::cout << mrfFilter->GetStopCondition() << std::endl;










     typename WriterType::Pointer writer = WriterType::New();
      writer->SetFileName( outputVolume.c_str() );
      writer->SetInput( kmeansFilter->GetOutput() );
      writer->SetUseCompression(1);
      writer->Update();
  }else if (clusterMethod == "FuzzyCMean") {

  }

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
