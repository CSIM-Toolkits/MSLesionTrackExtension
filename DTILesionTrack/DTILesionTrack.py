import os
import sys
import platform
import unittest

from os.path import expanduser

import vtk, qt, ctk, slicer
from SimpleITK.SimpleITK import MaskNegated
from slicer.ScriptedLoadableModule import *
import logging


#
# DTILesionTrack
#

class DTILesionTrack(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "DTI Lesion Track"  # TODO make this more human readable by adding spaces
        self.parent.categories = ["Segmentation.MS Lesion Track"]
        self.parent.dependencies = []
        self.parent.contributors = [
            "Antonio Carlos da S. Senra Filho (University of Sao Paulo), Luiz Otavio Murta Junior (University of Sao Paulo)"]  # replace with "Firstname Lastname (Organization)"
        self.parent.helpText = """
    This module aims to segment abnormals voxels from diffusion maps provided from DTI images,
     such as the fractional anisotropy (FA), mean diffusivity (MD) and others. This tool is optimized
      to analyse the lesion patterns observed in Multiple Sclerosis disease.
    """
        self.parent.acknowledgementText = """
    This work was partially funded by CNPq grant 201871/2015-7/SWE and CAPES.
"""  # replace with organization, grant and thanks.


#
# DTILesionTrackWidget
#

class DTILesionTrackWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # Instantiate and connect widgets ...

        #
        # Input Parameters Area
        #
        parametersInputCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersInputCollapsibleButton.text = "Input Parameters"
        self.layout.addWidget(parametersInputCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersInputFormLayout = qt.QFormLayout(parametersInputCollapsibleButton)

        #
        # input FLAIR volume selector
        #
        self.inputFLAIRSelector = slicer.qMRMLNodeComboBox()
        self.inputFLAIRSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputFLAIRSelector.selectNodeUponCreation = False
        self.inputFLAIRSelector.addEnabled = False
        self.inputFLAIRSelector.removeEnabled = False
        self.inputFLAIRSelector.noneEnabled = False
        self.inputFLAIRSelector.showHidden = False
        self.inputFLAIRSelector.showChildNodeTypes = False
        self.inputFLAIRSelector.setMRMLScene(slicer.mrmlScene)
        self.inputFLAIRSelector.setToolTip("T2-FLAIR image.")
        parametersInputFormLayout.addRow("T2-FLAIR Volume ", self.inputFLAIRSelector)

        #
        # input T1 volume selector
        #
        self.inputT1Selector = slicer.qMRMLNodeComboBox()
        self.inputT1Selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputT1Selector.selectNodeUponCreation = True
        self.inputT1Selector.addEnabled = False
        self.inputT1Selector.removeEnabled = False
        self.inputT1Selector.noneEnabled = False
        self.inputT1Selector.showHidden = False
        self.inputT1Selector.showChildNodeTypes = False
        self.inputT1Selector.setMRMLScene(slicer.mrmlScene)
        self.inputT1Selector.setToolTip("T1 image.")
        parametersInputFormLayout.addRow("T1 Volume ", self.inputT1Selector)

        #
        # input FA volume selector
        #
        self.inputFASelector = slicer.qMRMLNodeComboBox()
        self.inputFASelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputFASelector.selectNodeUponCreation = True
        self.inputFASelector.addEnabled = False
        self.inputFASelector.removeEnabled = False
        self.inputFASelector.noneEnabled = False
        self.inputFASelector.showHidden = False
        self.inputFASelector.showChildNodeTypes = False
        self.inputFASelector.setMRMLScene(slicer.mrmlScene)
        self.inputFASelector.setToolTip("DTI Fractional Anisotropy (FA) map.")
        parametersInputFormLayout.addRow("DTI-FA Volume ", self.inputFASelector)

        #
        # input MD volume selector
        #
        self.inputMDSelector = slicer.qMRMLNodeComboBox()
        self.inputMDSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputMDSelector.selectNodeUponCreation = True
        self.inputMDSelector.addEnabled = False
        self.inputMDSelector.removeEnabled = False
        self.inputMDSelector.noneEnabled = True
        self.inputMDSelector.showHidden = False
        self.inputMDSelector.showChildNodeTypes = False
        self.inputMDSelector.setMRMLScene(slicer.mrmlScene)
        self.inputMDSelector.setToolTip("DTI Mean Diffusivity (MD) map.")
        parametersInputFormLayout.addRow("DTI-MD Volume ", self.inputMDSelector)

        #
        # input RA volume selector
        #
        self.inputRASelector = slicer.qMRMLNodeComboBox()
        self.inputRASelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputRASelector.selectNodeUponCreation = True
        self.inputRASelector.addEnabled = False
        self.inputRASelector.removeEnabled = False
        self.inputRASelector.noneEnabled = True
        self.inputRASelector.showHidden = False
        self.inputRASelector.showChildNodeTypes = False
        self.inputRASelector.setMRMLScene(slicer.mrmlScene)
        self.inputRASelector.setToolTip("DTI Relative Anisotropy (RA) map.")
        parametersInputFormLayout.addRow("DTI-RA Volume ", self.inputRASelector)

        #
        # input Perpendicular Diffusivity volume selector
        #
        self.inputPerDSelector = slicer.qMRMLNodeComboBox()
        self.inputPerDSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputPerDSelector.selectNodeUponCreation = True
        self.inputPerDSelector.addEnabled = False
        self.inputPerDSelector.removeEnabled = False
        self.inputPerDSelector.noneEnabled = True
        self.inputPerDSelector.showHidden = False
        self.inputPerDSelector.showChildNodeTypes = False
        self.inputPerDSelector.setMRMLScene(slicer.mrmlScene)
        self.inputPerDSelector.setToolTip("DTI Perpendicular Diffusivity map.")
        parametersInputFormLayout.addRow("DTI-Perpendicular Diff. Volume ", self.inputPerDSelector)

        #
        # input Volume Ratio volume selector
        #
        self.inputVRSelector = slicer.qMRMLNodeComboBox()
        self.inputVRSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputVRSelector.selectNodeUponCreation = True
        self.inputVRSelector.addEnabled = False
        self.inputVRSelector.removeEnabled = False
        self.inputVRSelector.noneEnabled = True
        self.inputVRSelector.showHidden = False
        self.inputVRSelector.showChildNodeTypes = False
        self.inputVRSelector.setMRMLScene(slicer.mrmlScene)
        self.inputVRSelector.setToolTip("DTI Volume Ratio map.")
        parametersInputFormLayout.addRow("DTI-VR Volume ", self.inputVRSelector)

        #
        # Output Parameters Area
        #
        parametersOutputCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersOutputCollapsibleButton.text = "Output Parameters"
        self.layout.addWidget(parametersOutputCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersOutputFormLayout = qt.QFormLayout(parametersOutputCollapsibleButton)

        #
        # output label selector
        #
        self.outputSelector = slicer.qMRMLNodeComboBox()
        self.outputSelector.nodeTypes = ["vtkMRMLLabelMapVolumeNode"]
        self.outputSelector.selectNodeUponCreation = True
        self.outputSelector.addEnabled = True
        self.outputSelector.removeEnabled = True
        self.outputSelector.noneEnabled = False
        self.outputSelector.showHidden = False
        self.outputSelector.showChildNodeTypes = False
        self.outputSelector.setMRMLScene(slicer.mrmlScene)
        self.outputSelector.setToolTip(
            "Output a global label mask which inform the lesions segmented in the white matter.")
        parametersOutputFormLayout.addRow("Lesion Label ", self.outputSelector)

        #
        # Output Lesion Mask Area
        #
        # self.setOutputLesionMaskBooleanWidget = ctk.ctkComboBox()
        # self.setOutputLesionMaskBooleanWidget.addItem("Global")
        # self.setOutputLesionMaskBooleanWidget.addItem("Separable")
        # self.setOutputLesionMaskBooleanWidget.setToolTip(
        #     "Choose if you want to separate the lesions by different label masks or display as a global lesion label mask.")
        # parametersOutputFormLayout.addRow("Output Lesion Mask ", self.setOutputLesionMaskBooleanWidget)

        #
        # Brain extraction on T1 and FLAIR
        #
        self.setApplyBrainExtractedBooleanWidget = ctk.ctkCheckBox()
        self.setApplyBrainExtractedBooleanWidget.setChecked(False)
        self.setApplyBrainExtractedBooleanWidget.setToolTip(
            "Apply previous brain extraction step before move on the registration process. If the input T1 and FLAIR images are already brain extracted, you can leave this step blank.")
        parametersOutputFormLayout.addRow("Apply brain extraction on T1 and FLAIR", self.setApplyBrainExtractedBooleanWidget)

        #
        # Advanced Parameters Area
        #
        parametersAdvancedCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersAdvancedCollapsibleButton.text = "Advanced Parameters"
        self.layout.addWidget(parametersAdvancedCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersAdvancedFormLayout = qt.QFormLayout(parametersAdvancedCollapsibleButton)

        #
        # White Matter Tracks Area
        #
        # self.setWhiteMatterTracksBooleanWidget = ctk.ctkComboBox()
        # self.setWhiteMatterTracksBooleanWidget.addItem("All white matter tracks")
        # self.setWhiteMatterTracksBooleanWidget.addItem("Main white matter tracks")
        # self.setWhiteMatterTracksBooleanWidget.setToolTip(
        #     "Choose how many white matter tracks do you want to be analysed in the post-processing step. Option: All tracks = Use all the atlas labels marked in the Mori, et al. ICBM-DTI-81 atlas (DOI:10.1016/j.neuroimage.2007.02.049); Main tracks = Use only the 6 main white matter tracks ()")
        # parametersAdvancedFormLayout.addRow("White Matter Tracks Evaluation ", self.setWhiteMatterTracksBooleanWidget)

        #
        # DTI Template Area
        #
        self.setDTITemplateWidget = ctk.ctkComboBox()
        self.setDTITemplateWidget.addItem("JHU-81")
        self.setDTITemplateWidget.addItem("USP-20")
        self.setDTITemplateWidget.addItem("USP-131")
        self.setDTITemplateWidget.setToolTip(
            "Choose the DTI template where the input images will be registered. Options: ICBM-DTI-81 (1.5T from John Hopkins University), ICBM-DTI-20 (3.0T 16 averages from University of Sao Paulo) or ICBM-DTI-131 (3.0T from University of Sao Paulo)")
        parametersAdvancedFormLayout.addRow("DTI Template ", self.setDTITemplateWidget)

        #
        # Template Resolution Area
        #
        self.setTemplateResolutionBooleanWidget = ctk.ctkComboBox()
        self.setTemplateResolutionBooleanWidget.addItem("1mm")
        self.setTemplateResolutionBooleanWidget.addItem("2mm")
        self.setTemplateResolutionBooleanWidget.setToolTip(
            "Choose the spatial resolution which will be used to whole DTI segmentation pipeline. Options: 1mm or 2mm")
        parametersAdvancedFormLayout.addRow("Template Spatial Resolution ", self.setTemplateResolutionBooleanWidget)

        #
        # Interpolation Method Area
        #
        self.setInterpolationMethodBooleanWidget = ctk.ctkComboBox()
        self.setInterpolationMethodBooleanWidget.addItem("Linear")
        self.setInterpolationMethodBooleanWidget.addItem("BSpline")
        self.setInterpolationMethodBooleanWidget.addItem("NearestNeighbor")
        self.setInterpolationMethodBooleanWidget.setToolTip(
            "Choose the interpolation method used to register the input images into the standard space. Options: Linear, Tri-linear and Spline")
        parametersAdvancedFormLayout.addRow("Interpolation ", self.setInterpolationMethodBooleanWidget)

        #
        # BSpline Grid Size Area
        #
        # self.setBSplineGridSizeWidget = ctk.ctkMessageBox()
        # self.setBSplineGridSizeWidget.setToolTip(" Options: Linear, Tri-linear and Spline")
        # parametersAdvancedFormLayout.addRow("Template Spatial Resolution ", self.setBSplineGridSizeWidget)

        #
        # Fast Registration Strategy
        #
        self.setFastRegistrationBooleanWidget = ctk.ctkCheckBox()
        self.setFastRegistrationBooleanWidget.setChecked(True)
        self.setFastRegistrationBooleanWidget.setToolTip(
            "Calculate all the registration process in the 2mm resolution and, when its finishes, the image is interpolated to 1mm.")
        parametersOutputFormLayout.addRow("Use Fast Registration Strategy",
                                          self.setFastRegistrationBooleanWidget)

        # #
        # # Estimates Patient Lesion Load Area
        # #
        # self.setLesionLoadBooleanWidget = ctk.ctkCheckBox()
        # self.setLesionLoadBooleanWidget.setChecked(True)
        # self.setLesionLoadBooleanWidget.setToolTip("Output the lesion load metric estimated from the output label.")
        # parametersAdvancedFormLayout.addRow("Estimates Patient Lesion Load ", self.setLesionLoadBooleanWidget)

        #
        # Statistical Analysis Area
        #
        self.setSegmentationApproachWidget = ctk.ctkComboBox()
        self.setSegmentationApproachWidget.addItem("LSDP")
        self.setSegmentationApproachWidget.addItem("SpatialClustering")
        self.setSegmentationApproachWidget.addItem("Bayesian")
        self.setSegmentationApproachWidget.setToolTip(
            "Choose the DTI template where the input images will be registered. Options: Local Statistical Diffusibility Properties (LSDP), Spatial Clustering Outlier, Bayesian ...")
        parametersAdvancedFormLayout.addRow("Segmentation Approach ", self.setSegmentationApproachWidget)

        #
        # Apply Button
        #
        self.applyButton = qt.QPushButton("Apply")
        self.applyButton.toolTip = "Run the algorithm."
        self.applyButton.enabled = False
        parametersOutputFormLayout.addRow(self.applyButton)

        # connections
        self.applyButton.connect('clicked(bool)', self.onApplyButton)
        self.inputFASelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
        self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

        # Add vertical spacer
        self.layout.addStretch(1)

        # Refresh Apply button state
        self.onSelect()

    def cleanup(self):
        pass

    def onSelect(self):
        self.applyButton.enabled = self.inputFASelector.currentNode() and self.outputSelector.currentNode()

    def onApplyButton(self):
        logic = DTILesionTrackLogic()
        logic.run(self.inputFLAIRSelector.currentNode()
                  , self.inputT1Selector.currentNode()
                  , self.inputFASelector.currentNode()
                  , self.inputMDSelector.currentNode()
                  , self.inputRASelector.currentNode()
                  , self.inputPerDSelector.currentNode()
                  , self.inputVRSelector.currentNode()
                  , self.outputSelector.currentNode()
                  , self.setApplyBrainExtractedBooleanWidget
                  , self.setInterpolationMethodBooleanWidget
                  , self.setTemplateResolutionBooleanWidget.currentText
                  , self.setDTITemplateWidget.currentText
                  , self.setFastRegistrationBooleanWidget
                  , self.setSegmentationApproachWidget.currentText
                  )


#
# DTILesionTrackLogic
#

class DTILesionTrackLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def hasImageData(self, volumeNode):
        """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
        if not volumeNode:
            logging.debug('hasImageData failed: no volume node')
            return False
        if volumeNode.GetImageData() is None:
            logging.debug('hasImageData failed: no image data in volume node')
            return False
        return True

    def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
        """Validates if the output is not the same as input
    """
        if not inputVolumeNode:
            logging.debug('isValidInputOutputData failed: no input volume node defined')
            return False
        if not outputVolumeNode:
            logging.debug('isValidInputOutputData failed: no output volume node defined')
            return False
        if inputVolumeNode.GetID() == outputVolumeNode.GetID():
            logging.debug(
                'isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
            return False
        return True

    def run(self, inputFLAIRVolume, inputT1Volume, inputFAVolume, inputMDVolume, inputRAVolume, inputPerDVolume,
            inputVRVolume, outputLabelVolume, applyBET, interpolationMethod,
            templateDTIResolution, templateDTI, segmentationApproach, useFastRegistration):
        """
    Run the actual algorithm
    """
        logging.info('Processing started')
        slicer.util.showStatusMessage("Processing started")
        mapsCount=1

        #################################################################################################################
        #                   Start the pre-processing step: Brain extraction (optional) and Registration                 #
        #################################################################################################################

        # Check if the input images are already brain extracted. If not, apply a brain extraction on both.
        if applyBET.isChecked():
            slicer.util.showStatusMessage("Pre-processing: Extraction brain from T1 and FLAIR images...")
            #
            # T1 brain extraction
            #
            betParams = {}
            betParams["inputVolume"] = inputT1Volume.GetID()
            betParams["outputVolume"] = inputT1Volume.GetID()

            slicer.cli.run(slicer.modules.brainextractiontool, None, betParams, wait_for_completion=True)

            #
            # FLAIR brain extraction
            #
            betParams = {}
            betParams["inputVolume"] = inputFLAIRVolume.GetID()
            betParams["outputVolume"] = inputFLAIRVolume.GetID()

            slicer.cli.run(slicer.modules.brainextractiontool, None, betParams, wait_for_completion=True)

        # Perform fast registration strategy? (Do always the registration over 2mm and interpolate to 1mm after warped)
        # TODO PRECISA TERMINAR ESTA IDEIA!!!!!!
        # if useFastRegistration.isChecked():
            # DO ALL THE REGISTRATION IN 2MM
        # else
        #     DO NORMALLY

        slicer.util.showStatusMessage("Step 1/5: Reading DTI Template...")
        if platform.system() is "Windows":
            home = expanduser("%userprofile%")
        else:
            home = expanduser("~")


        if platform.system() is "Windows":
            if (templateDTIResolution == '1mm') & (templateDTI == 'JHU-81'):
                DTITemplate = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU-81'):
                DTITemplate = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-2mm"
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                DTITemplate = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-20-FA-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                DTITemplate = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-20-2mm"
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                DTITemplate = slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                DTITemplate = slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-2mm"
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
        else:
            if (templateDTIResolution == '1mm') & (templateDTI == 'JHU-81'):
                DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU-81'):
                DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = 'JHU-ICBM-FA-2mm'
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-20-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-20-2mm"
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-1mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-1mm"
                T1TemplateMask = "MNI152_T1_1mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                DTITemplate = slicer.util.loadVolume(
                home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-2mm.nii.gz')
                MNITemplateMask = slicer.util.loadVolume(
                home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz')
                MNITemplateBrain = slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-2mm"
                T1TemplateMask = "MNI152_T1_2mm_brain_wm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"

        slicer.util.showStatusMessage("Step 2/5: Registering input volumes...")

        #
        # Registering the T1 image to FLAIR image.
        #
        slicer.util.showStatusMessage("Step 2/5: T1 registration...")
        registrationT12FLAIRTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(registrationT12FLAIRTransform)
        inputT1Volume_reg = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(inputT1Volume_reg)
        regParams = {}
        regParams["fixedVolume"] = inputFLAIRVolume.GetID() #slicer.util.getNode(T1TemplateBrain)
        regParams["movingVolume"] = inputT1Volume.GetID()
        regParams["samplingPercentage"] = 0.02
        regParams["splineGridSize"] = '14,10,12'
        regParams["outputVolume"] = inputT1Volume_reg.GetID()
        regParams["linearTransform"] = registrationT12FLAIRTransform.GetID()
        regParams["initializeTransformMode"] = "useMomentsAlign"
        regParams["useRigid"] = True
        regParams["interpolationMode"] = interpolationMethod.currentText
        regParams["numberOfSamples"] = 200000

        slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)


        #
        # Registering the DTI-FA to FLAIR image
        #
        slicer.util.showStatusMessage("Step 2/5: DTI-FA registration...")
        registrationDTI2FLAIRTransform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(registrationDTI2FLAIRTransform)
        inputFAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(inputFAVolume_reg)
        regParams = {}
        regParams["fixedVolume"] = inputFLAIRVolume.GetID()
        regParams["movingVolume"] = inputFAVolume.GetID()
        regParams["samplingPercentage"] = 0.02
        regParams["splineGridSize"] = '14,10,12'
        regParams["outputVolume"] = inputFAVolume_reg.GetID()
        regParams["linearTransform"] = registrationDTI2FLAIRTransform.GetID()
        regParams["initializeTransformMode"] = "useMomentsAlign"
        regParams["useAffine"] = True
        regParams["interpolationMode"] = interpolationMethod.currentText
        regParams["numberOfSamples"] = 200000

        slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)

        #
        # Registering the MNI-DTI template to FA native space. (Uses only to obtain the registration transformation)
        #

        # Demon Diffeomorphic Registration
        slicer.util.showStatusMessage("Step 2/5: DTI ICBM template registration...")
        registrationTemplateTransform = slicer.vtkMRMLGridTransformNode()
        slicer.mrmlScene.AddNode(registrationTemplateTransform)
        inputTemplateVolume_reg = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(inputTemplateVolume_reg)
        regParams = {}
        regParams["fixedVolume"] = inputFAVolume_reg.GetID()
        regParams["movingVolume"] = slicer.util.getNode(DTITemplateNodeName)
        regParams["samplingPercentage"] = 0.002
        regParams["outputVolume"] = inputTemplateVolume_reg.GetID()
        regParams["outputDisplacementFieldVolume"] = registrationTemplateTransform.GetID()
        regParams["interpolationMode"] = interpolationMethod.currentText

        slicer.cli.run(slicer.modules.brainsdemonwarp, None, regParams, wait_for_completion=True)


        #
        # Applying transformation to DTI template image that will actually be used on the lesion segmentation part
        #TODO FAZER ESTA PARTE PARA USAR OUTRO TEMPLATE DTI NA SEGMENTACAO ... USAR PARA COREGISTRO UM DTI TEMPLATE DIFERENTE

        #
        # Applying registration transform - MD Volume
        #
        if inputMDVolume != None:
            mapsCount=mapsCount+1
            #
            # Registering the MD image with the MNI-DTI template.
            #
            # USE THE BSPLINE TRANSFORM IN THE FA MAP TO WARP THE REST OF THE INPUT IMAGES
            slicer.util.showStatusMessage("Step 2/5: DTI-MD registration...")
            inputMDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputMDVolume_reg)
            resampMDParams = {}
            resampMDParams["inputVolume"] = inputMDVolume.GetID()
            resampMDParams["referenceVolume"] = inputFLAIRVolume.GetID()
            resampMDParams["outputVolume"] = inputMDVolume_reg.GetID()
            resampMDParams["warpTransform"] = registrationDTI2FLAIRTransform.GetID()
            resampMDParams["interpolationMode"] = interpolationMethod.currentText

            slicer.cli.run(slicer.modules.brainsresample, None, resampMDParams, wait_for_completion=True)

        #
        # Applying registration transform - RA Volume
        #
        if inputRAVolume != None:
            mapsCount=mapsCount+1
            #
            # Registering the RA image with the MNI-DTI template.
            #
            slicer.util.showStatusMessage("Step 2/5: DTI-RA registration...")
            inputRAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputRAVolume_reg)
            resampRAParams = {}
            resampRAParams["inputVolume"] = inputRAVolume.GetID()
            resampRAParams["referenceVolume"] = inputFLAIRVolume.GetID()
            resampRAParams["outputVolume"] = inputRAVolume_reg.GetID()
            resampRAParams["warpTransform"] = registrationDTI2FLAIRTransform.GetID()
            resampRAParams["interpolationMode"] = interpolationMethod.currentText

            slicer.cli.run(slicer.modules.brainsresample, None, resampRAParams, wait_for_completion=True)

        #
        # Applying registration transform - Perpendicular Diffusivity Volume
        #
        if inputPerDVolume != None:
            mapsCount=mapsCount+1
            #
            # Registering the Per Diff image with the MNI-DTI template.
            #
            slicer.util.showStatusMessage("Step 2/5: DTI-PerpDiff registration...")
            inputPerDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputPerDVolume_reg)
            resampPerDParams = {}
            resampPerDParams["inputVolume"] = inputPerDVolume.GetID()
            resampPerDParams["referenceVolume"] = inputFLAIRVolume.GetID()
            resampPerDParams["outputVolume"] = inputPerDVolume_reg.GetID()
            resampPerDParams["warpTransform"] = registrationDTI2FLAIRTransform.GetID()
            resampPerDParams["interpolationMode"] = interpolationMethod.currentText

            slicer.cli.run(slicer.modules.brainsresample, None, resampPerDParams, wait_for_completion=True)

        #
        # Applying registration transform - VR Volume
        #
        if inputVRVolume != None:
            mapsCount=mapsCount+1
            #
            # Registering the Per Diff image with the MNI-DTI template.
            #
            slicer.util.showStatusMessage("Step 2/5: DTI-VR registration...")
            inputVRVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputVRVolume_reg)
            resampVRParams = {}
            resampVRParams["inputVolume"] = inputVRVolume.GetID()
            resampVRParams["referenceVolume"] = inputFLAIRVolume.GetID()
            resampVRParams["outputVolume"] = inputVRVolume_reg.GetID()
            resampVRParams["warpTransform"] = registrationDTI2FLAIRTransform.GetID()
            resampVRParams["interpolationMode"] = interpolationMethod.currentText

            slicer.cli.run(slicer.modules.brainsresample, None, resampVRParams, wait_for_completion=True)

        #################################################################################################################
        #                 Initial lesion map aproximation given by the hyperintense lesion of FLAIR image               #
        #################################################################################################################
        slicer.util.showStatusMessage("Step 3/5: Initial lesion map aproximation...")
        # TODO mat

        #
        # CRIAR LABEL USANDO O LST !!!!!!!!!!! TODAS AS IMAGENS ESTAO NO ESPACO DA FLAIR, ENTAO LST VAI PASSAR PARA O ESPACO NATIVO !!!!!!
        #


        #################################################################################################################
        # The pre-processing is done. Below are the evaluated the lesion maps based on the chosen Statistical Analaysis #
        #################################################################################################################
        #################################################################################################################
        #                                    Apply the chosen segmentation approach                                     #
        #################################################################################################################
        if (segmentationApproach == 'LSDP'):
            slicer.util.showStatusMessage("Step 5/5: Performing LSDP segmentation on all data...")
            #
            # Perform the statistical segmentation - FA map
            #
            outputFALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
            slicer.mrmlScene.AddNode(outputFALesionLabelNode)
            statisticalFASegmentationParams = {}
            statisticalFASegmentationParams["inputVolume"] = inputFAVolume_reg.GetID()
            # statisticalFASegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
            statisticalFASegmentationParams["mapType"] = "FracionalAnisotropy"
            statisticalFASegmentationParams["mapResolution"] = templateDTIResolution
            statisticalFASegmentationParams["statMethod"] = "T-Score"
            statisticalFASegmentationParams["tThreshold"] = 5.0
            statisticalFASegmentationParams["outputLabelVolume"] = outputFALesionLabelNode.GetID()

            # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalFASegmentationParams, wait_for_completion=True)

            if inputMDVolume != None:
                #
                # Perform the statistical segmentation - MD map
                #
                outputMDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputMDLesionLabelNode)
                statisticalMDSegmentationParams = {}
                statisticalMDSegmentationParams["inputVolume"] = inputMDVolume_reg.GetID()
                # statisticalMDSegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
                statisticalMDSegmentationParams["mapType"] = "MeanDiffusivity"
                statisticalMDSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalMDSegmentationParams["statMethod"] = "T-Score"
                statisticalMDSegmentationParams["tThreshold"] = 5.0
                statisticalMDSegmentationParams["outputLabelVolume"] = outputMDLesionLabelNode.GetID()

                # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalMDSegmentationParams, wait_for_completion=True)

            if inputRAVolume != None:
                #
                # Perform the statistical segmentation - RA map
                #
                outputRALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputRALesionLabelNode)
                statisticalRASegmentationParams = {}
                statisticalRASegmentationParams["inputVolume"] = inputRAVolume_reg.GetID()
                # statisticalRASegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
                statisticalRASegmentationParams["mapType"] = "RelativeAnisotropy"
                statisticalRASegmentationParams["mapResolution"] = templateDTIResolution
                statisticalRASegmentationParams["statMethod"] = "T-Score"
                statisticalRASegmentationParams["tThreshold"] = 5.0
                statisticalRASegmentationParams["outputLabelVolume"] = outputRALesionLabelNode.GetID()

                # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalRASegmentationParams, wait_for_completion=True)

            if inputPerDVolume != None:
                #
                # Perform the statistical segmentation - Perpendicular Diffusivity map
                #
                outputPerDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputPerDLesionLabelNode)
                statisticalPerDSegmentationParams = {}
                statisticalPerDSegmentationParams["inputVolume"] = inputPerDVolume_reg.GetID()
                # statisticalPerDSegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
                statisticalPerDSegmentationParams["mapType"] = "PerpendicularDiffusivity"
                statisticalPerDSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalPerDSegmentationParams["statMethod"] = "T-Score"
                statisticalPerDSegmentationParams["tThreshold"] = 5.0
                statisticalPerDSegmentationParams["outputLabelVolume"] = outputPerDLesionLabelNode.GetID()

                # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalPerDSegmentationParams, wait_for_completion=True)

            if inputVRVolume != None:
                #
                # Perform the statistical segmentation - VR map
                #
                outputVRLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputVRLesionLabelNode)
                statisticalVRSegmentationParams = {}
                statisticalVRSegmentationParams["inputVolume"] = inputVRVolume_reg.GetID()
                # statisticalVRSegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
                statisticalVRSegmentationParams["mapType"] = "VolumeRatio"
                statisticalVRSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalVRSegmentationParams["statMethod"] = "T-Score"
                statisticalVRSegmentationParams["tThreshold"] = 5.0
                statisticalVRSegmentationParams["outputLabelVolume"] = outputVRLesionLabelNode.GetID()

                # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalVRSegmentationParams, wait_for_completion=True)

            # slicer.util.showStatusMessage("Step 6: Grouping lesion masks...")
            #Grouping all the lesion masks by the lesion propagation in each DTI map
            # finalLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
            # slicer.mrmlScene.AddNode(finalLesionLabelNode)
            outputLabelVolume = outputFALesionLabelNode
            if mapsCount > 1:
                finalLesioLabelParameters = {}

                if inputMDVolume != None:
                    finalLesioLabelParameters["inputVolume1"]= outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"]= outputMDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"]= outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"]=0

                    # slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputRAVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputRALesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    # slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputPerDVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputPerDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    # slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputVRVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputVRLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    # slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)

        elif segmentationApproach == 'SpatialClustering':
            slicer.util.showStatusMessage("Step 5: Performing Spatial Clustering segmentation on all data...")
            outputFALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
            slicer.mrmlScene.AddNode(outputFALesionLabelNode)
            statisticalFASegmentationParams = {}
            statisticalFASegmentationParams["inputVolume"] = inputFAVolume_reg.GetID()
            # statisticalFASegmentationParams["inputLabel"] = INPUT LABEL FROM LST!!!!
            statisticalFASegmentationParams["mapType"] = "FracionalAnisotropy"
            statisticalFASegmentationParams["mapResolution"] = templateDTIResolution
            statisticalFASegmentationParams["statMethod"] = "T-Score"
            statisticalFASegmentationParams["tThreshold"] = 5.0
            statisticalFASegmentationParams["outputLabelVolume"] = outputFALesionLabelNode.GetID()

            # slicer.cli.run(slicer.modules.lspdbrainsegmentation, None, statisticalFASegmentationParams, wait_for_completion=True)

        elif segmentationApproach == 'Bayesian':
            slicer.util.showStatusMessage("Step 5: Performing Bayesian segmentation on all data...")






















            #################################################################################################################
            #                               Remove the gray matter from the input normalized data                           #
            #################################################################################################################
            # #
            # # Prepare the white matter mask from MNI152-T1
            # #
            # slicer.util.showStatusMessage("Step 4/5: Masking white matter in the input volumes ")
            #
            #
            #
            # #
            # # FA White Matter
            # #
            # inputFAVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
            # slicer.mrmlScene.AddNode(inputFAVolume_reg_wm)
            # applyFAMaskParams = {}
            # applyFAMaskParams["InputVolume"] = inputFAVolume_reg.GetID()
            # applyFAMaskParams["MaskVolume"] = slicer.util.getNode(T1TemplateMask)
            # applyFAMaskParams["Label"] = 3
            # applyFAMaskParams["OutputVolume"] = inputFAVolume_reg_wm.GetID()
            #
            # # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyFAMaskParams, wait_for_completion=True)
            #
            #
            # if inputMDVolume != None:
            #     slicer.util.showStatusMessage("Step 4/5: Masking Mean Diffusivity white matter volume...")
            #     #
            #     # MD White Matter
            #     #
            #     inputMDVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
            #     slicer.mrmlScene.AddNode(inputMDVolume_reg_wm)
            #     applyMDMaskParams = {}
            #     # applyMDMaskParams["InputVolume"] = inputMDNode_reg.GetID()
            #     applyMDMaskParams["MaskVolume"] = slicer.util.getNode(T1TemplateMask)
            #     applyMDMaskParams["Label"] = 3
            #     applyMDMaskParams["OutputVolume"] = inputMDVolume_reg_wm.GetID()
            #
            #     # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyMDMaskParams, wait_for_completion=True)
            #
            # if inputRAVolume != None:
            #     slicer.util.showStatusMessage("Step 4/5: Masking Relative Anisotropy white matter volume...")
            #     #
            #     # RA White Matter
            #     #
            #     inputRAVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
            #     slicer.mrmlScene.AddNode(inputRAVolume_reg_wm)
            #     applyRAMaskParams = {}
            #     applyRAMaskParams["InputVolume"] = inputRAVolume_reg.GetID()
            #     applyRAMaskParams["MaskVolume"] = slicer.util.getNode(T1TemplateMask)
            #     applyRAMaskParams["Label"] = 3
            #     applyRAMaskParams["OutputVolume"] = inputRAVolume_reg_wm.GetID()
            #
            #     # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyRAMaskParams, wait_for_completion=True)
            #
            # if inputPerDVolume != None:
            #     slicer.util.showStatusMessage("Step 4/5: Masking Perpendicular Diffusivity white matter volume...")
            #     #
            #     # Perpendicular Diffusivity White Matter
            #     #
            #     inputPerDVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
            #     slicer.mrmlScene.AddNode(inputPerDVolume_reg_wm)
            #     applyPerDMaskParams = {}
            #     applyPerDMaskParams["InputVolume"] = inputPerDVolume_reg.GetID()
            #     applyPerDMaskParams["MaskVolume"] = slicer.util.getNode(T1TemplateMask)
            #     applyPerDMaskParams["Label"] = 3
            #     applyPerDMaskParams["OutputVolume"] = inputPerDVolume_reg_wm.GetID()
            #
            #     # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyPerDMaskParams, wait_for_completion=True)
            #
            # if inputVRVolume != None:
            #     slicer.util.showStatusMessage("Step 4/5: Masking Volume Ratio white matter volume...")
            #     #
            #     # Parallel Diffusivity White Matter
            #     #
            #     inputVRVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
            #     slicer.mrmlScene.AddNode(inputVRVolume_reg_wm)
            #     applyVRMaskParams = {}
            #     applyVRMaskParams["InputVolume"] = inputVRVolume_reg.GetID()
            #     applyVRMaskParams["MaskVolume"] = slicer.util.getNode(T1TemplateMask)
            #     applyVRMaskParams["Label"] = 3
            #     applyVRMaskParams["OutputVolume"] = inputVRVolume_reg_wm.GetID()
            #
            #     # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyVRMaskParams, wait_for_completion=True)

        # Perform the statistical segmentation based on all the input data
        #










        # #
        # # Perform the statistical segmentation - FA map
        # #
        # outputFALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
        # slicer.mrmlScene.AddNode(outputFALesionLabelNode)
        # statisticalFASegmentationParams = {}
        # # statisticalFASegmentationParams["inputVolume"] =
        # # statisticalFASegmentationParams["mapType"] =
        # # statisticalFASegmentationParams["mapResolution"] =
        # # statisticalFASegmentationParams["statMethod"] =
        # # statisticalFASegmentationParams["zThreshold"] =
        # statisticalFASegmentationParams["outputLabelVolume"] = outputLabelVolume

        # slicer.cli.run(slicer.modules.statisticalbrainsegmentation, None, statisticalFASegmentationParams, wait_for_completion=True)

        # #
        # # Split the lesion label
        # #
        # if outputLesionMaskComboBox.currentText != "Global":
        #


        slicer.util.showStatusMessage("DTILesionTrack - Processing completed!")

        return True


class DTILesionTrackTest(ScriptedLoadableModuleTest):
    """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
    """
        self.setUp()
        self.test_DTILesionTrack1()

    def test_DTILesionTrack1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

        self.delayDisplay("Starting the test")
        #
        # first, get some data
        #
        import urllib
        downloads = (
            ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

        for url, name, loader in downloads:
            filePath = slicer.app.temporaryPath + '/' + name
            if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
                logging.info('Requesting download %s from %s...\n' % (name, url))
                urllib.urlretrieve(url, filePath)
            if loader:
                logging.info('Loading %s...' % (name,))
                loader(filePath)
        self.delayDisplay('Finished with download and loading')

        volumeNode = slicer.util.getNode(pattern="FA")
        logic = DTILesionTrackLogic()
        self.assertIsNotNone(logic.hasImageData(volumeNode))
        self.delayDisplay('Test passed!')
