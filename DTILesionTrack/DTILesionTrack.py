import os
import sys
import platform
import unittest

from os.path import expanduser

import vtk, qt, ctk, slicer
from SimpleITK.SimpleITK import MaskNegated
from numpy.f2py.auxfuncs import throw_error
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
        self.parent.title = "DTI Lesion Track"
        self.parent.categories = ["Segmentation.MS Lesion Track"]
        self.parent.dependencies = []
        self.parent.contributors = [
            "Antonio Carlos da S. Senra Filho (University of Sao Paulo), Luiz Otavio Murta Junior (University of Sao Paulo)"]  # replace with "Firstname Lastname (Organization)"
        self.parent.helpText = """
    This module aims to segment abnormals voxels from a multidimensional MRI data, resulting from T1, T2-FLAIR and DTI scalar maps
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
        if platform.system() is "Windows":
            home = expanduser("%userprofile%")
        else:
            home = expanduser("~")

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
        self.inputFLAIRSelector.setToolTip("T2-FLAIR Volume")
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
        self.inputT1Selector.setToolTip("T1 Volume")
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
        self.inputFASelector.setToolTip("DTI Fractional Anisotropy (FA) Volume")
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
        self.inputMDSelector.setToolTip("DTI Mean Diffusivity (MD) Volume")
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
        self.inputRASelector.setToolTip("DTI Relative Anisotropy (RA) Volume")
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
        self.inputPerDSelector.setToolTip("DTI Perpendicular Diffusivity Volume")
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
        self.inputVRSelector.setToolTip("DTI Volume Ratio Volume")
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
        self.outputSelector.renameEnabled = True
        self.outputSelector.removeEnabled = True
        self.outputSelector.noneEnabled = False
        self.outputSelector.showHidden = False
        self.outputSelector.showChildNodeTypes = False
        self.outputSelector.setMRMLScene(slicer.mrmlScene)
        self.outputSelector.setToolTip(
            "Output a global label mask which inform the lesions segmented in the white matter.")
        parametersOutputFormLayout.addRow("Lesion Label ", self.outputSelector)

        #
        # output label selector
        #
        self.TemporaryFolderSelector = ctk.ctkDirectoryButton()
        self.TemporaryFolderSelector.setToolTip( "Output folder where intermediate files will be saved.")
        parametersOutputFormLayout.addRow("Output Folder ", self.TemporaryFolderSelector)

        #
        # Brain extraction on T1 and FLAIR
        #
        self.setApplyBrainExtractedBooleanWidget = ctk.ctkCheckBox()
        self.setApplyBrainExtractedBooleanWidget.setChecked(False)
        self.setApplyBrainExtractedBooleanWidget.setToolTip(
            "Apply previous brain extraction step before move on the registration process. If the input T1 and FLAIR images are already brain extracted, you can leave this step blank.")
        parametersOutputFormLayout.addRow("Apply brain extraction on T1 and FLAIR", self.setApplyBrainExtractedBooleanWidget)

        #
        # Noise attenuation on T1 and FLAIR
        #
        self.setApplyNoiseAttenuationWidget = ctk.ctkCheckBox()
        self.setApplyNoiseAttenuationWidget.setChecked(False)
        self.setApplyNoiseAttenuationWidget.setToolTip(
            "Apply noise attenuation process on the input T1 and FLAIR images.")
        parametersOutputFormLayout.addRow("Apply noise attenuation on T1 and FLAIR",
                                          self.setApplyNoiseAttenuationWidget)

        #
        # Use Quick ANTs registration
        #
        self.setUseANTsnWidget = ctk.ctkCheckBox()
        self.setUseANTsnWidget.setChecked(True)
        self.setUseANTsnWidget.setToolTip(
            "Use a fast ANTs diffeomorphic registration script on DTI scalar maps in order to fit the brain template to the native space.")
        parametersOutputFormLayout.addRow("Use quick ANTs diffeomorphic registration",
                                          self.setUseANTsnWidget)

        #
        # Output in ICBM space
        #
        self.setUseICBMSpaceWidget = ctk.ctkCheckBox()
        self.setUseICBMSpaceWidget.setChecked(True)
        self.setUseICBMSpaceWidget.setToolTip(
            "The final image label will be set in the ICBM space. If not, the output label will be set to native space.")
        parametersOutputFormLayout.addRow("Output in ICBM space",
                                          self.setUseICBMSpaceWidget)

        #
        # Noise Attenuation Parameters Area
        #
        parametersNoiseAttenuationCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersNoiseAttenuationCollapsibleButton.text = "Noise Attenuation Parameters"
        self.layout.addWidget(parametersNoiseAttenuationCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersNoiseAttenuationFormLayout = qt.QFormLayout(parametersNoiseAttenuationCollapsibleButton)

        #
        # Filtering Parameters: Condutance
        #
        self.setFilteringCondutanceWidget = qt.QSpinBox()
        self.setFilteringCondutanceWidget.setMaximum(10)
        self.setFilteringCondutanceWidget.setMinimum(0)
        self.setFilteringCondutanceWidget.setValue(5)
        self.setFilteringCondutanceWidget.setToolTip("Condutance parameter.")
        parametersNoiseAttenuationFormLayout.addRow("Condutance ", self.setFilteringCondutanceWidget)

        #
        # Filtering Parameters: Number of iterations
        #
        self.setFilteringNumberOfIterationWidget = qt.QSpinBox()
        self.setFilteringNumberOfIterationWidget.setMaximum(50)
        self.setFilteringNumberOfIterationWidget.setMinimum(0)
        self.setFilteringNumberOfIterationWidget.setValue(5)
        self.setFilteringNumberOfIterationWidget.setToolTip("Number of iterations parameter.")
        parametersNoiseAttenuationFormLayout.addRow("Number Of Iterations ", self.setFilteringNumberOfIterationWidget)

        #
        # Filtering Parameters: Q value
        #
        self.setFilteringQWidget = qt.QDoubleSpinBox()
        self.setFilteringQWidget.setMaximum(2)
        self.setFilteringQWidget.setMinimum(0)
        self.setFilteringQWidget.setSingleStep(0.1)
        self.setFilteringQWidget.setValue(1.2)
        self.setFilteringQWidget.setToolTip("Q value parameter.")
        parametersNoiseAttenuationFormLayout.addRow("Q Value ", self.setFilteringQWidget)

        #
        # Advanced Parameters Area
        #
        parametersAdvancedCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersAdvancedCollapsibleButton.text = "Advanced Parameters"
        self.layout.addWidget(parametersAdvancedCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersAdvancedFormLayout = qt.QFormLayout(parametersAdvancedCollapsibleButton)

        #
        # DTI Template Area
        #
        self.setDTITemplateWidget = ctk.ctkComboBox()
        self.setDTITemplateWidget.addItem("USP-20")
        self.setDTITemplateWidget.addItem("USP-131")
        self.setDTITemplateWidget.setToolTip(
            "Choose the DTI template where the input images will be registered. Options: ICBM-DTI-20 (3.0T 16 averages from University of Sao Paulo) or ICBM-DTI-131 (3.0T from University of Sao Paulo)")
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
        # Statistical Analysis Area
        #
        self.setSegmentationApproachWidget = ctk.ctkComboBox()
        self.setSegmentationApproachWidget.addItem("Bayesian")
        self.setSegmentationApproachWidget.addItem("LSDP")
        self.setSegmentationApproachWidget.addItem("SpatialClustering")
        self.setSegmentationApproachWidget.setToolTip(
            "Choose the DTI template where the input images will be registered. Options: Local Statistical Diffusibility Properties (LSDP), Spatial Clustering Outlier, Bayesian ...")
        parametersAdvancedFormLayout.addRow("Segmentation Approach ", self.setSegmentationApproachWidget)

        #
        # LSDP Threshold
        #
        self.setLSDPThresholdQWidget = qt.QDoubleSpinBox()
        self.setLSDPThresholdQWidget.setMaximum(50)
        self.setLSDPThresholdQWidget.setMinimum(0)
        self.setLSDPThresholdQWidget.setSingleStep(0.5)
        self.setLSDPThresholdQWidget.setValue(2.5)
        self.setLSDPThresholdQWidget.setToolTip("T-Score t-test threshold value. This parameter is only used when Segmentation Approach if LSDP.")
        parametersAdvancedFormLayout.addRow("LSDP Threshold ", self.setLSDPThresholdQWidget)

        #
        # Clustering Approach
        #
        self.setThresholdMethodWidget = ctk.ctkComboBox()
        self.setThresholdMethodWidget.addItem("Otsu")
        self.setThresholdMethodWidget.addItem("MaxEntropy")
        self.setThresholdMethodWidget.addItem("Yen")
        self.setThresholdMethodWidget.addItem("IsoData")
        self.setThresholdMethodWidget.addItem("Moments")
        self.setThresholdMethodWidget.addItem("Renyi")
        self.setThresholdMethodWidget.setToolTip(
            "Choose the type of clustering approach that will be used to estimate the lesions on the brain white matter space. This parameter is only used when Segmentation Approach if SpatialClustering")
        parametersAdvancedFormLayout.addRow("Clustering Approach ", self.setThresholdMethodWidget)

        #
        # Clustering Number of Classes
        #
        self.setClusterNumberOfClassesWidget = qt.QSpinBox()
        self.setClusterNumberOfClassesWidget.setMaximum(10)
        self.setClusterNumberOfClassesWidget.setMinimum(1)
        self.setClusterNumberOfClassesWidget.setValue(2)
        self.setClusterNumberOfClassesWidget.setToolTip("Number of Classes where will be used to agregates the lesion voxel intensity. This parameter is only used when Segmentation Approach if SpatialClustering")
        parametersAdvancedFormLayout.addRow("Number of Classes ", self.setClusterNumberOfClassesWidget)

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
                  , self.TemporaryFolderSelector
                  , self.setApplyBrainExtractedBooleanWidget
                  , self.setApplyNoiseAttenuationWidget
                  , self.setUseANTsnWidget
                  , self.setUseICBMSpaceWidget
                  , self.setFilteringCondutanceWidget
                  , self.setFilteringNumberOfIterationWidget
                  , self.setFilteringQWidget
                  , self.setInterpolationMethodBooleanWidget
                  , self.setTemplateResolutionBooleanWidget.currentText
                  , self.setDTITemplateWidget.currentText
                  , self.setSegmentationApproachWidget.currentText
                  , self.setLSDPThresholdQWidget
                  , self.setThresholdMethodWidget.currentText
                  , self.setClusterNumberOfClassesWidget
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
            inputVRVolume, outputLabelVolume, folderSelector, applyBET, applyNoiseAttenuation, applyQuickANTS, outputICBMSpace,
            filterCondutance, filterNumInt, filterQ, interpolationMethod,templateDTIResolution, templateDTI,
            segmentationApproach, lsdpTScoreThreshold, thresholdMethod, clusterNumberOfClasses):
        """
    Run the actual algorithm
    """
        logging.info('Processing started')
        slicer.util.showStatusMessage("Processing started")
        mapsCount=1

        #################################################################################################################
        #                                       Check the programs dependencies                                         #
        #################################################################################################################
        if not os.environ.has_key("ANTSPATH"):
            slicer.util.showStatusMessage("ERROR: ANTs registration toolkit is not installed in your system. Check the ANTSPATH variable.")
            return True

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

        #
        # T1 and FLAIR pre-processing: bias field correction
        #
        slicer.util.showStatusMessage("Pre-processing: Bias field correction on T1...")
        n4params = {}
        n4params["inputImageName"] = inputT1Volume.GetID()
        n4params["outputImageName"] = inputT1Volume.GetID()
        slicer.cli.run(slicer.modules.n4itkbiasfieldcorrection, None, n4params, wait_for_completion=True)

        slicer.util.showStatusMessage("Pre-processing: Bias field correction on T2-FLAIR...")
        n4params = {}
        n4params["inputImageName"] = inputFLAIRVolume.GetID()
        n4params["outputImageName"] = inputFLAIRVolume.GetID()
        slicer.cli.run(slicer.modules.n4itkbiasfieldcorrection, None, n4params, wait_for_completion=True)

        #
        # T1 and FLAIR pre-processing: noise attenuation
        #
        if applyNoiseAttenuation.isChecked():
            slicer.util.showStatusMessage("Pre-processing: T1 noise attenuation...")
            filterParams = {}
            filterParams["inputVolume"] = inputT1Volume.GetID()
            filterParams["outputVolume"] = inputT1Volume.GetID()
            filterParams["condutance"] = filterCondutance.value
            filterParams["iterations"] = filterNumInt.value
            filterParams["q"] = filterQ.value
            slicer.cli.run(slicer.modules.aadimagefilter, None, filterParams, wait_for_completion=True)

            slicer.util.showStatusMessage("Pre-processing: T2-FLAIR noise attenuation...")
            filterParams = {}
            filterParams["inputVolume"] = inputFLAIRVolume.GetID()
            filterParams["outputVolume"] = inputFLAIRVolume.GetID()
            filterParams["condutance"] = filterCondutance.value
            filterParams["iterations"] = filterNumInt.value
            filterParams["q"] = filterQ.value
            slicer.cli.run(slicer.modules.aadimagefilter, None, filterParams, wait_for_completion=True)

        slicer.util.showStatusMessage("Step 1/5: Reading brain templates...")
        if platform.system() is "Windows":
            home = expanduser("%userprofile%")
        else:
            home = expanduser("~")

        #Read FA Template
        if platform.system() is "Windows":
            if (templateDTIResolution == '1mm') & (templateDTI == 'JHU-81'):
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU-81'):
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-2mm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-20-FA-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-20-2mm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                slicer.util.loadVolume(
                home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-2mm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
        else:
            if (templateDTIResolution == '1mm') & (templateDTI == 'JHU-81'):
                slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "JHU-ICBM-FA-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU-81'):
                slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = 'JHU-ICBM-FA-2mm'
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-20-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-20-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-20-2mm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"
            elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-1mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-1mm"
                T1TemplateBrain = "MNI152_T1_1mm_brain"
            elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                slicer.util.loadVolume(
                home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-2mm.nii.gz')
                slicer.util.loadVolume(
                    home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz')
                DTITemplateNodeName = "USP-ICBM-FA-131-2mm"
                T1TemplateBrain = "MNI152_T1_2mm_brain"

        if inputMDVolume != None:
            #Read MD Template
            if platform.system() is "Windows":
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-20-1mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-20-MD-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-20-2mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-131-1mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-131-2mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-131-2mm"
            else:
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    DTITemplate = slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-20-1mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-20-2mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-131-1mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-131-2mm.nii.gz')
                    MDTemplateNodeName = "USP-ICBM-MD-131-2mm"

        if inputRAVolume != None:
            # Read RA Template
            if platform.system() is "Windows":
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-20-1mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-20-RA-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-20-2mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-131-1mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-131-2mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-131-2mm"
            else:
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    DTITemplate = slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-20-1mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-20-2mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-131-1mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-131-2mm.nii.gz')
                    RATemplateNodeName = "USP-ICBM-RA-131-2mm"

        if inputPerDVolume != None:
            # Read Perp Diff Template
            if platform.system() is "Windows":
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-20-1mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-20-PerpDiff-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-20-2mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-131-1mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-131-2mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-131-2mm"
            else:
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    DTITemplate = slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-20-1mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-20-2mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-131-1mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-131-2mm.nii.gz')
                    PerpDiffTemplateNodeName = "USP-ICBM-PerpDiff-131-2mm"

        if inputVRVolume != None:
            # Read VR Template
            if platform.system() is "Windows":
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-20-1mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-20-VR-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-20-2mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-131-1mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-131-2mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-131-2mm"
            else:
                if (templateDTIResolution == '1mm') & (templateDTI == 'USP-20'):
                    DTITemplate = slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-20-1mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-20'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-20-2mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-20-2mm"
                elif (templateDTIResolution == '1mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-131-1mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-131-1mm"
                elif (templateDTIResolution == '2mm') & (templateDTI == 'USP-131'):
                    slicer.util.loadVolume(
                        home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-131-2mm.nii.gz')
                    VRTemplateNodeName = "USP-ICBM-VR-131-2mm"

        slicer.util.showStatusMessage("Step 2/5: Registering input volumes...")

        #
        # Registering the FLAIR image to T1 image.
        #
        slicer.util.showStatusMessage("Step 2/5: T1 registration...")
        registrationFLAIR2T1Transform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(registrationFLAIR2T1Transform)
        inputFLAIRVolume_reg = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(inputFLAIRVolume_reg)
        regParams = {}
        regParams["fixedVolume"] = inputT1Volume.GetID()
        regParams["movingVolume"] = inputFLAIRVolume.GetID()
        regParams["samplingPercentage"] = 0.02
        regParams["splineGridSize"] = '14,10,12'
        regParams["outputVolume"] = inputFLAIRVolume_reg.GetID()
        regParams["linearTransform"] = registrationFLAIR2T1Transform.GetID()
        regParams["initializeTransformMode"] = "useMomentsAlign"
        regParams["useRigid"] = True
        regParams["interpolationMode"] = interpolationMethod.currentText
        regParams["numberOfSamples"] = 200000

        slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)


        #
        # Registering the DTI-FA to T1 image
        #
        slicer.util.showStatusMessage("Step 2/5: DTI-FA registration...")
        registrationDTI2T1Transform = slicer.vtkMRMLLinearTransformNode()
        slicer.mrmlScene.AddNode(registrationDTI2T1Transform)
        inputFAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
        slicer.mrmlScene.AddNode(inputFAVolume_reg)
        regParams = {}
        regParams["fixedVolume"] = inputT1Volume.GetID()
        regParams["movingVolume"] = inputFAVolume.GetID()
        regParams["samplingPercentage"] = 0.02
        regParams["splineGridSize"] = '14,10,12'
        regParams["outputVolume"] = inputFAVolume_reg.GetID()
        regParams["linearTransform"] = registrationDTI2T1Transform.GetID()
        regParams["initializeTransformMode"] = "useMomentsAlign"
        regParams["useAffine"] = True
        regParams["interpolationMode"] = interpolationMethod.currentText
        regParams["numberOfSamples"] = 200000

        slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)

        #
        # Registering the MNI-DTI template to FA native space.
        #

        slicer.util.showStatusMessage("Step 2/5: DTI template registration...")
        if applyQuickANTS.isChecked:
            #Saving files into tmp folder
            #Patient FA
            slicer.util.saveNode(inputFAVolume_reg, folderSelector.directory+'/patient-FA.nii.gz')
            # FA Template
            slicer.util.saveNode(slicer.util.getNode(DTITemplateNodeName), folderSelector.directory + '/DTI-Template-FA.nii.gz')

            # Use ANTs registration
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh")
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/antsRegistrationSyNQuick.sh")
            os.system(home+"/MSLesionTrack-Data/diffeomorphicRegistration.sh "+folderSelector.directory+" Y"+ " N")

            #Read registered images and tranforms
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate1Warp.nii.gz')# DTI Template to native space
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate1InverseWarp.nii.gz')
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate0GenericAffine.mat')# DTI Template to native space
            slicer.util.loadVolume(folderSelector.directory + '/regTemplateWarped.nii.gz')#DTI Template into patient space
            slicer.util.loadVolume(folderSelector.directory + '/regTemplateInverseWarped.nii.gz')#Patient in ICBM space
        else:
            # Saving files into tmp folder
            # Patient FA
            slicer.util.saveNode(inputFAVolume, folderSelector.directory + '/patient-FA.nii.gz')
            # FA Template
            slicer.util.saveNode(slicer.util.getNode(DTITemplateNodeName),folderSelector.directory + '/DTI-Template-FA.nii.gz')

            # Use ANTs registration
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh")
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/antsRegistrationSyN.sh")
            os.system(home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh " + folderSelector.directory+" N"+ " N")

            # Read registered images and tranforms
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate1Warp.nii.gz')  # DTI Template to native space
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate1InverseWarp.nii.gz')
            slicer.util.loadTransform(folderSelector.directory + '/regTemplate0GenericAffine.mat')  # DTI Template to native space
            slicer.util.loadVolume(folderSelector.directory + '/regTemplateWarped.nii.gz')  # DTI Template into patient space
            slicer.util.loadVolume(folderSelector.directory + '/regTemplateInverseWarped.nii.gz')  # Patient in ICBM space

        # TODO COREGISTRO COM MD, nao linear, PRECISA SER FEITO NOVAMENTE...so chamar o script ANTs
        #
        # Applying registration transform - MD Volume
        #
        if inputMDVolume != None:
            mapsCount=mapsCount+1
            #
            # Registering the MD image with the MNI-DTI template.
            #
            slicer.util.showStatusMessage("Step 2/4: DTI-MD registration...")
            inputMDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputMDVolume_reg)
            resampMDParams = {}
            resampMDParams["inputVolume"] = inputMDVolume.GetID()
            resampMDParams["referenceVolume"] = inputT1Volume.GetID()
            resampMDParams["outputVolume"] = inputMDVolume_reg.GetID()
            resampMDParams["warpTransform"] = registrationDTI2T1Transform.GetID()
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
            slicer.util.showStatusMessage("Step 2/4: DTI-RA registration...")
            inputRAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputRAVolume_reg)
            resampRAParams = {}
            resampRAParams["inputVolume"] = inputRAVolume.GetID()
            resampRAParams["referenceVolume"] = inputT1Volume.GetID()
            resampRAParams["outputVolume"] = inputRAVolume_reg.GetID()
            resampRAParams["warpTransform"] = registrationDTI2T1Transform.GetID()
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
            slicer.util.showStatusMessage("Step 2/4: DTI-PerpDiff registration...")
            inputPerDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputPerDVolume_reg)
            resampPerDParams = {}
            resampPerDParams["inputVolume"] = inputPerDVolume.GetID()
            resampPerDParams["referenceVolume"] = inputT1Volume.GetID()
            resampPerDParams["outputVolume"] = inputPerDVolume_reg.GetID()
            resampPerDParams["warpTransform"] = registrationDTI2T1Transform.GetID()
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
            slicer.util.showStatusMessage("Step 2/4: DTI-VR registration...")
            inputVRVolume_reg = slicer.vtkMRMLScalarVolumeNode()
            slicer.mrmlScene.AddNode(inputVRVolume_reg)
            resampVRParams = {}
            resampVRParams["inputVolume"] = inputVRVolume.GetID()
            resampVRParams["referenceVolume"] = inputT1Volume.GetID()
            resampVRParams["outputVolume"] = inputVRVolume_reg.GetID()
            resampVRParams["warpTransform"] = registrationDTI2T1Transform.GetID()
            resampVRParams["interpolationMode"] = interpolationMethod.currentText

            slicer.cli.run(slicer.modules.brainsresample, None, resampVRParams, wait_for_completion=True)


        #################################################################################################################
        # The pre-processing is done. Below are the evaluated the lesion maps based on the chosen Statistical Analaysis #
        #################################################################################################################
        #################################################################################################################
        #                                       Apply the DTI segmentation approach                                     #
        #################################################################################################################
        if (segmentationApproach == 'LSDP'):
            slicer.util.showStatusMessage("Step 3/5: Performing LSDP segmentation on all data...")
            #
            # Perform the statistical segmentation - FA map
            #
            statisticalFASegmentationParams = {}
            statisticalFASegmentationParams["inputVolume"] = slicer.util.getNode('regTemplateInverseWarped')
            statisticalFASegmentationParams["mapType"] = "FractionalAnisotropy"
            statisticalFASegmentationParams["mapResolution"] = templateDTIResolution
            statisticalFASegmentationParams["statMethod"] = "T-Score"
            statisticalFASegmentationParams["tThreshold"] = lsdpTScoreThreshold.value
            statisticalFASegmentationParams["outputLabel"] = outputLabelVolume.GetID()

            slicer.cli.run(slicer.modules.lsdpbrainsegmentation, None, statisticalFASegmentationParams, wait_for_completion=True)

            if inputMDVolume != None:
                #SyN
                inputLSDPMDinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputLSDPMDinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputMDVolume_reg.GetID()
                antsParams["outputVolume"] = inputLSDPMDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams,  wait_for_completion=True)

                #Affine
                antsParams={}
                antsParams["inputVolume"]= inputLSDPMDinICBMVolume.GetID()
                antsParams["outputVolume"]= inputLSDPMDinICBMVolume.GetID()
                antsParams["referenceVolume"]= slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"]= slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"]="linear"
                antsParams["inverseITKTransformation"]=True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform the statistical segmentation - MD map
                #
                outputMDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputMDLesionLabelNode)
                statisticalMDSegmentationParams = {}
                statisticalMDSegmentationParams["inputVolume"] = inputLSDPMDinICBMVolume.GetID()
                statisticalMDSegmentationParams["mapType"] = "MeanDiffusivity"
                statisticalMDSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalMDSegmentationParams["statMethod"] = "T-Score"
                statisticalMDSegmentationParams["tThreshold"] = lsdpTScoreThreshold.value
                statisticalMDSegmentationParams["outputLabel"] = outputMDLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.lsdpbrainsegmentation, None, statisticalMDSegmentationParams, wait_for_completion=True)

            if inputRAVolume != None:
                # SyN
                inputLSDPRAinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputLSDPRAinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputRAVolume_reg.GetID()
                antsParams["outputVolume"] = inputLSDPRAinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputLSDPRAinICBMVolume.GetID()
                antsParams["outputVolume"] = inputLSDPRAinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform the statistical segmentation - RA map
                #
                outputRALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputRALesionLabelNode)
                statisticalRASegmentationParams = {}
                statisticalRASegmentationParams["inputVolume"] = inputLSDPRAinICBMVolume.GetID()
                statisticalRASegmentationParams["mapType"] = "RelativeAnisotropy"
                statisticalRASegmentationParams["mapResolution"] = templateDTIResolution
                statisticalRASegmentationParams["statMethod"] = "T-Score"
                statisticalRASegmentationParams["tThreshold"] = lsdpTScoreThreshold.value
                statisticalRASegmentationParams["outputLabel"] = outputRALesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.lsdpbrainsegmentation, None, statisticalRASegmentationParams,
                               wait_for_completion=True)

            if inputPerDVolume != None:
                # SyN
                inputLSDPPerDinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputLSDPPerDinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputPerDVolume_reg.GetID()
                antsParams["outputVolume"] = inputLSDPPerDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputLSDPPerDinICBMVolume.GetID()
                antsParams["outputVolume"] = inputLSDPPerDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform the statistical segmentation - Perpendicular Diffusivity map
                #
                outputPerDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputPerDLesionLabelNode)
                statisticalPerDSegmentationParams = {}
                statisticalPerDSegmentationParams["inputVolume"] = inputLSDPPerDinICBMVolume.GetID()
                statisticalPerDSegmentationParams["mapType"] = "PerpendicularDiffusivity"
                statisticalPerDSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalPerDSegmentationParams["statMethod"] = "T-Score"
                statisticalPerDSegmentationParams["tThreshold"] = lsdpTScoreThreshold.value
                statisticalPerDSegmentationParams["outputLabel"] = outputPerDLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.lsdpbrainsegmentation, None, statisticalPerDSegmentationParams,
                               wait_for_completion=True)

            if inputVRVolume != None:
                # SyN
                inputLSDPVRinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputLSDPVRinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputVRVolume_reg.GetID()
                antsParams["outputVolume"] = inputLSDPVRinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = interpolationMethod.currentText
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputLSDPVRinICBMVolume.GetID()
                antsParams["outputVolume"] = inputLSDPVRinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform the statistical segmentation - VR map
                #
                outputVRLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputVRLesionLabelNode)
                statisticalVRSegmentationParams = {}
                statisticalVRSegmentationParams["inputVolume"] = inputLSDPVRinICBMVolume.GetID()
                statisticalVRSegmentationParams["mapType"] = "VolumeRatio"
                statisticalVRSegmentationParams["mapResolution"] = templateDTIResolution
                statisticalVRSegmentationParams["statMethod"] = "T-Score"
                statisticalVRSegmentationParams["tThreshold"] = lsdpTScoreThreshold.value
                statisticalVRSegmentationParams["outputLabel"] = outputVRLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.lsdpbrainsegmentation, None, statisticalVRSegmentationParams,
                               wait_for_completion=True)

            if mapsCount > 1:
                    finalLesioLabelParameters = {}

                    if inputMDVolume != None:
                        finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["inputVolume2"] = outputMDLesionLabelNode.GetID()
                        finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["order"] = 0

                        slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                       wait_for_completion=True)
                    if inputRAVolume != None:
                        finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["inputVolume2"] = outputRALesionLabelNode.GetID()
                        finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["order"] = 0

                        slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                       wait_for_completion=True)
                    if inputPerDVolume != None:
                        finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["inputVolume2"] = outputPerDLesionLabelNode.GetID()
                        finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["order"] = 0

                        slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                       wait_for_completion=True)
                    if inputVRVolume != None:
                        finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["inputVolume2"] = outputVRLesionLabelNode.GetID()
                        finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                        finalLesioLabelParameters["order"] = 0

                        slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                       wait_for_completion=True)
        elif segmentationApproach == 'SpatialClustering':
            slicer.util.showStatusMessage("Step 3/5: Performing Spatial Clustering segmentation on all data...")

            clusterParams = {}
            clusterParams["inputVolume"] = slicer.util.getNode('regTemplateInverseWarped')
            clusterParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
            clusterParams["outputVolume"] = outputLabelVolume.GetID()
            clusterParams["dtiMap"] = "FractionalAnisotropy"
            clusterParams["mapResolution"] = templateDTIResolution
            clusterParams["thrMethod"] = thresholdMethod
            clusterParams["numClass"] = clusterNumberOfClasses.value

            slicer.cli.run(slicer.modules.clusteringscalardiffusionsegmentation, None, clusterParams, wait_for_completion=True)

            if inputMDVolume != None:
                # SyN
                inputMDICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputMDICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputMDVolume_reg.GetID()
                antsParams["outputVolume"] = inputMDICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputMDICBMVolume.GetID()
                antsParams["outputVolume"] = inputMDICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                outputMDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputMDLesionLabelNode)
                clusterParams = {}
                clusterParams["inputVolume"] = inputMDICBMVolume.GetID()
                clusterParams["referenceVolume"] = slicer.util.getNode(MDTemplateNodeName)
                clusterParams["outputVolume"] = outputMDLesionLabelNode.GetID()
                clusterParams["dtiMap"] = "MeanDiffusivity"
                clusterParams["mapResolution"] = templateDTIResolution
                clusterParams["thrMethod"] = thresholdMethod
                clusterParams["numClass"] = clusterNumberOfClasses.value

                slicer.cli.run(slicer.modules.clusteringscalardiffusionsegmentation, None, clusterParams, wait_for_completion=True)
            if inputRAVolume != None:
                # SyN
                inputRAICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputRAICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputRAVolume_reg.GetID()
                antsParams["outputVolume"] = inputRAICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputRAICBMVolume.GetID()
                antsParams["outputVolume"] = inputRAICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                outputRALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputRALesionLabelNode)
                clusterParams = {}
                clusterParams["inputVolume"] = inputRAICBMVolume.GetID()
                clusterParams["referenceVolume"] = slicer.util.getNode(RATemplateNodeName)
                clusterParams["outputVolume"] = outputRALesionLabelNode.GetID()
                clusterParams["dtiMap"] = "RelativeAnisotropy"
                clusterParams["mapResolution"] = templateDTIResolution
                clusterParams["thrMethod"] = thresholdMethod
                clusterParams["numClass"] = clusterNumberOfClasses.value

                slicer.cli.run(slicer.modules.clusteringscalardiffusionsegmentation, None, clusterParams,
                               wait_for_completion=True)
            if inputPerDVolume != None:
                # SyN
                inputPerDICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputPerDICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputPerDVolume_reg.GetID()
                antsParams["outputVolume"] = inputPerDICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputPerDICBMVolume.GetID()
                antsParams["outputVolume"] = inputPerDICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                outputPerDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputPerDLesionLabelNode)
                clusterParams = {}
                clusterParams["inputVolume"] = inputPerDICBMVolume.GetID()
                clusterParams["referenceVolume"] = slicer.util.getNode(PerpDiffTemplateNodeName)
                clusterParams["outputVolume"] = outputPerDLesionLabelNode.GetID()
                clusterParams["dtiMap"] = "PerpendicularDiffusivity"
                clusterParams["mapResolution"] = templateDTIResolution
                clusterParams["thrMethod"] = thresholdMethod
                clusterParams["numClass"] = clusterNumberOfClasses.value

                slicer.cli.run(slicer.modules.clusteringscalardiffusionsegmentation, None, clusterParams,
                               wait_for_completion=True)
            if inputVRVolume != None:
                # SyN
                inputVRICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputVRICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputVRVolume_reg.GetID()
                antsParams["outputVolume"] = inputVRICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputVRICBMVolume.GetID()
                antsParams["outputVolume"] = inputVRICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                outputVRLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputVRLesionLabelNode)
                clusterParams = {}
                clusterParams["inputVolume"] = inputVRICBMVolume.GetID()
                clusterParams["referenceVolume"] = slicer.util.getNode(VRTemplateNodeName)
                clusterParams["outputVolume"] = outputVRLesionLabelNode.GetID()
                clusterParams["dtiMap"] = "VolumeRatio"
                clusterParams["mapResolution"] = templateDTIResolution
                clusterParams["thrMethod"] = thresholdMethod
                clusterParams["numClass"] = clusterNumberOfClasses.value

                slicer.cli.run(slicer.modules.clusteringscalardiffusionsegmentation, None, clusterParams,
                               wait_for_completion=True)

            if mapsCount > 1:
                finalLesioLabelParameters = {}

                if inputMDVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputMDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                   wait_for_completion=True)
                if inputRAVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputRALesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                   wait_for_completion=True)
                if inputPerDVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputPerDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                   wait_for_completion=True)
                if inputVRVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputVRLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters,
                                   wait_for_completion=True)
        elif segmentationApproach == 'Bayesian':
            slicer.util.showStatusMessage("Step 3/5: Performing Bayesian segmentation on all data...")
            #
            #Perform Bayesian segmentation in FA map
            #
            bayesParams = {}
            bayesParams["inputVolume"] = slicer.util.getNode('regTemplateInverseWarped')
            bayesParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
            bayesParams["mapType"] = "FractionalAnisotropy"
            bayesParams["priorsImage"] = "Multiple Sclerosis Lesions"
            bayesParams["mapResolution"] = templateDTIResolution
            bayesParams["thrMethod"] = thresholdMethod
            bayesParams["outputLabel"] = outputLabelVolume.GetID()

            slicer.cli.run(slicer.modules.bayesiandtisegmentation, None, bayesParams, wait_for_completion=True)

            if inputMDVolume != None:
                # SyN
                inputBayesMDinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputBayesMDinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputMDVolume_reg.GetID()
                antsParams["outputVolume"] = inputBayesMDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(MDTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputBayesMDinICBMVolume.GetID()
                antsParams["outputVolume"] = inputBayesMDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(MDTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform Bayesian segmentation in MD map
                #
                outputMDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputMDLesionLabelNode)
                bayesParams = {}
                bayesParams["inputVolume"] = inputBayesMDinICBMVolume.GetID()
                bayesParams["referenceVolume"] = slicer.util.getNode(MDTemplateNodeName)
                bayesParams["mapType"] = "MeanDiffusivity"
                bayesParams["priorsImage"] = "Multiple Sclerosis Lesions"
                bayesParams["mapResolution"] = templateDTIResolution
                bayesParams["thrMethod"] = thresholdMethod
                bayesParams["outputLabel"] = outputMDLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.bayesiandtisegmentation, None, bayesParams, wait_for_completion=True)
            if inputRAVolume != None:
                # SyN
                inputBayesRAinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputBayesRAinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputRAVolume_reg.GetID()
                antsParams["outputVolume"] = inputBayesRAinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(RATemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputBayesRAinICBMVolume.GetID()
                antsParams["outputVolume"] = inputBayesRAinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(RATemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform Bayesian segmentation in RA map
                #
                outputRALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputRALesionLabelNode)
                bayesParams = {}
                bayesParams["inputVolume"] = inputBayesRAinICBMVolume.GetID()
                bayesParams["referenceVolume"] = slicer.util.getNode(RATemplateNodeName)
                bayesParams["mapType"] = "RelativeAnisotropy"
                bayesParams["priorsImage"] = "Multiple Sclerosis Lesions"
                bayesParams["mapResolution"] = templateDTIResolution
                bayesParams["thrMethod"] = thresholdMethod
                bayesParams["outputLabel"] = outputRALesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.bayesiandtisegmentation, None, bayesParams, wait_for_completion=True)
            if inputPerDVolume != None:
                # SyN
                inputBayesPerDinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputBayesPerDinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputPerDVolume_reg.GetID()
                antsParams["outputVolume"] = inputBayesPerDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(PerpDiffTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputBayesPerDinICBMVolume.GetID()
                antsParams["outputVolume"] = inputBayesPerDinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(PerpDiffTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform Bayesian segmentation in Perp Diff map
                #
                outputPerDLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputPerDLesionLabelNode)
                bayesParams = {}
                bayesParams["inputVolume"] = inputBayesPerDinICBMVolume.GetID()
                bayesParams["referenceVolume"] = slicer.util.getNode(PerpDiffTemplateNodeName)
                bayesParams["mapType"] = "PerpendicularDiffusivity"
                bayesParams["priorsImage"] = "Multiple Sclerosis Lesions"
                bayesParams["mapResolution"] = templateDTIResolution
                bayesParams["thrMethod"] = thresholdMethod
                bayesParams["outputLabel"] = outputPerDLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.bayesiandtisegmentation, None, bayesParams, wait_for_completion=True)
            if inputVRVolume != None:
                # # SyN
                inputBayesVRinICBMVolume = slicer.vtkMRMLScalarVolumeNode()
                slicer.mrmlScene.AddNode(inputBayesVRinICBMVolume)
                antsParams = {}
                antsParams["inputVolume"] = inputVRVolume_reg.GetID()
                antsParams["outputVolume"] = inputBayesVRinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(VRTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate1InverseWarp')
                antsParams["typeOfField"] = "displacement"
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = False

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                # Affine
                antsParams = {}
                antsParams["inputVolume"] = inputBayesVRinICBMVolume.GetID()
                antsParams["outputVolume"] = inputBayesVRinICBMVolume.GetID()
                antsParams["referenceVolume"] = slicer.util.getNode(VRTemplateNodeName)
                antsParams["transformationFile"] = slicer.util.getNode('regTemplate0GenericAffine')
                antsParams["interpolationType"] = "linear"
                antsParams["inverseITKTransformation"] = True

                slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

                #
                # Perform Bayesian segmentation in VR map
                #
                outputVRLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
                slicer.mrmlScene.AddNode(outputVRLesionLabelNode)
                bayesParams = {}
                bayesParams["inputVolume"] = inputBayesVRinICBMVolume.GetID()
                bayesParams["referenceVolume"] = slicer.util.getNode(VRTemplateNodeName)
                bayesParams["mapType"] = "VolumeRatio"
                bayesParams["priorsImage"] = "Multiple Sclerosis Lesions"
                bayesParams["mapResolution"] = templateDTIResolution
                bayesParams["thrMethod"] = thresholdMethod
                bayesParams["outputLabel"] = outputVRLesionLabelNode.GetID()

                slicer.cli.run(slicer.modules.bayesiandtisegmentation, None, bayesParams, wait_for_completion=True)

            if mapsCount > 1:
                finalLesioLabelParameters = {}

                if inputMDVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputMDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputRAVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputRALesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputPerDVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputPerDLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)
                if inputVRVolume != None:
                    finalLesioLabelParameters["inputVolume1"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["inputVolume2"] = outputVRLesionLabelNode.GetID()
                    finalLesioLabelParameters["outputVolume"] = outputLabelVolume.GetID()
                    finalLesioLabelParameters["order"] = 0

                    slicer.cli.run(slicer.modules.addscalarvolumes, None, finalLesioLabelParameters, wait_for_completion=True)

        #
        # Label Shape Constraints
        #
        labelShapeParams = {}
        labelShapeParams["inputVolume"] = outputLabelVolume.GetID()
        labelShapeParams["outputVolume"] = outputLabelVolume.GetID()
        labelShapeParams["labelToSmooth"] = mapsCount
        labelShapeParams["numberOfIterations"] = 50
        labelShapeParams["maxRMSError"] = 0.01
        labelShapeParams["gaussianSigma"] = 0.5

        slicer.cli.run(slicer.modules.labelmapsmoothing, None, labelShapeParams, wait_for_completion=True)

        #################################################################################################################
        #                                  Apply the T1 and FLAIR segmentation approach                                 #
        #################################################################################################################
        slicer.util.showStatusMessage("Step 4/5: T1 and T2-FLAIR lesion segmentation...")
        #
        # White Matter evaluation in T1 and FLAIR images - outlier detection
        #
        if applyQuickANTS.isChecked:
            # Saving files into tmp folder
            # Patient T1
            slicer.util.saveNode(inputT1Volume, folderSelector.directory + '/patient-T1.nii.gz')
            # Patient FLAIR
            slicer.util.saveNode(inputFLAIRVolume_reg, folderSelector.directory + '/patient-FLAIR.nii.gz')
            # MNI Template
            slicer.util.saveNode(slicer.util.getNode(T1TemplateBrain),folderSelector.directory + '/MNI-Template-T1.nii.gz')

            # Use ANTs registration
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh")
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/antsRegistrationSyNQuick.sh")
            os.system(home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh " + folderSelector.directory + " Y" + " Y")
        else:
            # Saving files into tmp folder
            # Patient T1
            slicer.util.saveNode(inputT1Volume, folderSelector.directory + '/patient-T1.nii.gz')
            # Patient FLAIR
            slicer.util.saveNode(inputFLAIRVolume_reg, folderSelector.directory + '/patient-FLAIR.nii.gz')
            # MNI Template
            slicer.util.saveNode(slicer.util.getNode(T1TemplateBrain),folderSelector.directory + '/MNI-Template-T1.nii.gz')

            # Use ANTs registration
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh")
            os.system("chmod u+x " + home + "/MSLesionTrack-Data/antsRegistrationSyNQuick.sh")
            os.system(home + "/MSLesionTrack-Data/diffeomorphicRegistration.sh " + folderSelector.directory + " N" + " Y")

        # Apply Structural Brain Segmentation
        os.system("chmod u+x " + home + "/MSLesionTrack-Data/structuralLesionSegmentation.sh")
        os.system("gunzip "+ folderSelector.directory +"/regStructInverseWarped.nii.gz")
        os.system(home +"/MSLesionTrack-Data/structuralLesionSegmentation.sh "+folderSelector.directory+"/regStructInverseWarped.nii")

        #
        # Merge DTI and T1/FLAIR Labels
        #
        slicer.util.showStatusMessage("Step 5/5: Merging DTI/T1/T2-FLAIR lesion map...")
        # Load structural label
        slicer.util.loadVolume(folderSelector.directory + '/struct-lesion-label.nii.gz')  # T1 and T2-FLAIR Lesion Label in ICBM Space

        mergeLabels= {}
        mergeLabels["inputVolume1"] = outputLabelVolume.GetID()
        mergeLabels["inputVolume2"] = slicer.util.getNode("struct-lesion-label")
        mergeLabels["outputVolume"] = outputLabelVolume.GetID()
        mergeLabels["order"] = 0

        slicer.cli.run(slicer.modules.addscalarvolumes, None, mergeLabels, wait_for_completion=True)

        #
        #  Registering back to native space
        #
        if not outputICBMSpace.isChecked():
            slicer.util.showStatusMessage("Opt: Transforming label map to native space...")
            # Read registered images and tranforms
            slicer.util.loadTransform(folderSelector.directory + '/regStruct1Warp.nii.gz')  # T1/FLAIR to native space
            slicer.util.loadTransform(folderSelector.directory + '/regStruct0GenericAffine.mat')  # T1/FLAIR to native space

            # Affine
            antsParams = {}
            antsParams["inputVolume"] = outputLabelVolume.GetID()
            antsParams["outputVolume"] = outputLabelVolume.GetID()
            antsParams["referenceVolume"] = inputT1Volume.GetID()
            antsParams["transformationFile"] = slicer.util.getNode('regStruct0GenericAffine')
            antsParams["interpolationType"] = "nn"
            antsParams["inverseITKTransformation"] = False

            slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

            # SyN
            antsParams = {}
            antsParams["inputVolume"] = outputLabelVolume.GetID()
            antsParams["outputVolume"] = outputLabelVolume.GetID()
            antsParams["referenceVolume"] = inputT1Volume.GetID()
            antsParams["transformationFile"] = slicer.util.getNode('regStruct1Warp')
            antsParams["typeOfField"] = "displacement"
            antsParams["interpolationType"] = "nn"
            antsParams["inverseITKTransformation"] = False

            slicer.cli.run(slicer.modules.resamplescalarvectordwivolume, None, antsParams, wait_for_completion=True)

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
