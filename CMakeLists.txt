cmake_minimum_required(VERSION 2.8.9)

project(MSLesionTrackExtension)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/MSLesionTrack")
set(EXTENSION_CATEGORY "Segmentation.MS Lesion Track")
set(EXTENSION_CONTRIBUTORS "Antonio Carlos da S. Senra Filho, CSIM Laboratory (University of Sao Paulo, Department of Computing and Mathematics)")
set(EXTENSION_DESCRIPTION "This extension aims to provide image processing tools in order to segment and detect MS lesions and the surrounding NAWM in the patient disease progression.")
set(EXTENSION_ICONURL "https://www.slicer.org/slicerWiki/index.php/File:MSLesionTrackExtension-logo.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/MSLesionTrack/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(BrainTissuesMask)
add_subdirectory(BrainExtractionTool)
add_subdirectory(DTILesionTrack)
add_subdirectory(LSDPBrainSegmentation)
add_subdirectory(BayesianDTISegmentation)
add_subdirectory(MRFDTISegmentation)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
