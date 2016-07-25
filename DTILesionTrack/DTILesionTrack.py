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
    self.parent.title = "DTI Lesion Track" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Segmentation.MS Lesion Track"]
    self.parent.dependencies = []
    self.parent.contributors = ["Antonio Carlos da S. Senra Filho (University of Sao Paulo), Luiz Otavio Murta Junior (University of Sao Paulo)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This module aims to segment abnormals voxels from diffusion maps provided from DTI images,
     such as the fractional anisotropy (FA), mean diffusivity (MD) and others. This tool is optimized
      to analyse the lesion patterns observed in Multiple Sclerosis disease.
    """
    self.parent.acknowledgementText = """
    This work was partially funded by CNPq grant 201871/2015-7/SWE and CAPES.
""" # replace with organization, grant and thanks.

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
    self.inputFASelector.setMRMLScene( slicer.mrmlScene )
    self.inputFASelector.setToolTip( "DTI Fractional Anisotropy (FA) map." )
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
    self.inputMDSelector.setMRMLScene( slicer.mrmlScene )
    self.inputMDSelector.setToolTip( "DTI Mean Diffusivity (MD) map." )
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
    self.inputRASelector.setMRMLScene( slicer.mrmlScene )
    self.inputRASelector.setToolTip( "DTI Relative Anisotropy (RA) map." )
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
    self.inputPerDSelector.setMRMLScene( slicer.mrmlScene )
    self.inputPerDSelector.setToolTip( "DTI Perpendicular Diffusivity map." )
    parametersInputFormLayout.addRow("DTI-Perpendicular Diff. Volume ", self.inputPerDSelector)

    #
    # input Parallel Diffusivity volume selector
    #
    self.inputParDSelector = slicer.qMRMLNodeComboBox()
    self.inputParDSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputParDSelector.selectNodeUponCreation = True
    self.inputParDSelector.addEnabled = False
    self.inputParDSelector.removeEnabled = False
    self.inputParDSelector.noneEnabled = True
    self.inputParDSelector.showHidden = False
    self.inputParDSelector.showChildNodeTypes = False
    self.inputParDSelector.setMRMLScene( slicer.mrmlScene )
    self.inputParDSelector.setToolTip( "DTI Parallel Diffusivity map." )
    parametersInputFormLayout.addRow("DTI-Parallel Diff. Volume ", self.inputParDSelector)

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
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Output a global label mask which inform the lesions segmented in the white matter." )
    parametersOutputFormLayout.addRow("Lesion Label ", self.outputSelector)

    #
    # Output Lesion Mask Area
    #
    self.setOutputLesionMaskBooleanWidget = ctk.ctkComboBox()
    self.setOutputLesionMaskBooleanWidget.addItem("Global")
    self.setOutputLesionMaskBooleanWidget.addItem("Separable")
    self.setOutputLesionMaskBooleanWidget.setToolTip("Choose if you want to separate the lesions by different label masks or display as a global lesion label mask.")
    parametersOutputFormLayout.addRow("Output Lesion Mask ", self.setOutputLesionMaskBooleanWidget)

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
    self.setWhiteMatterTracksBooleanWidget = ctk.ctkComboBox()
    self.setWhiteMatterTracksBooleanWidget.addItem("All white matter tracks")
    self.setWhiteMatterTracksBooleanWidget.addItem("Main white matter tracks")
    self.setWhiteMatterTracksBooleanWidget.setToolTip("Choose how many white matter tracks do you want to be analysed in the post-processing step. Option: All tracks = Use all the atlas labels marked in the Mori, et al. ICBM-DTI-81 atlas (DOI:10.1016/j.neuroimage.2007.02.049); Main tracks = Use only the 6 main white matter tracks ()")
    parametersAdvancedFormLayout.addRow("White Matter Tracks Evaluation ", self.setWhiteMatterTracksBooleanWidget)

    #
    # DTI Template Area
    #
    self.setDTITemplateWidget = ctk.ctkComboBox()
    self.setDTITemplateWidget.addItem("JHU")
    self.setDTITemplateWidget.addItem("USP")
    self.setDTITemplateWidget.setToolTip("Choose the DTI template where the input images will be registered. Options: ICBM-DTI-81 (1.5T from John Hopkins University) or ICBM-DTI-320 (3.0T from University of Sao Paulo)")
    parametersAdvancedFormLayout.addRow("DTI Template ", self.setDTITemplateWidget)

    #
    # Template Resolution Area
    #
    self.setTemplateResolutionBooleanWidget = ctk.ctkComboBox()
    self.setTemplateResolutionBooleanWidget.addItem("2mm")
    self.setTemplateResolutionBooleanWidget.addItem("1mm")
    self.setTemplateResolutionBooleanWidget.setToolTip("Choose the spatial resolution which will be used to whole DTI segmentation pipeline. Options: 1mm or 2mm")
    parametersAdvancedFormLayout.addRow("Template Spatial Resolution ", self.setTemplateResolutionBooleanWidget)

    #
    # Interpolation Method Area
    #
    self.setInterpolationMethodBooleanWidget = ctk.ctkComboBox()
    self.setInterpolationMethodBooleanWidget.addItem("BSpline")
    self.setInterpolationMethodBooleanWidget.addItem("Linear")
    self.setInterpolationMethodBooleanWidget.addItem("NearestNeighbor")
    self.setInterpolationMethodBooleanWidget.setToolTip("Choose the interpolation method used to register the input images into the standard space. Options: Linear, Tri-linear and Spline")
    parametersAdvancedFormLayout.addRow("Interpolation ", self.setInterpolationMethodBooleanWidget)

    #
    # BSpline Grid Size Area
    #
    # self.setBSplineGridSizeWidget = ctk.ctkMessageBox()
    # self.setBSplineGridSizeWidget.setToolTip(" Options: Linear, Tri-linear and Spline")
    # parametersAdvancedFormLayout.addRow("Template Spatial Resolution ", self.setBSplineGridSizeWidget)

    # #
    # # Estimates Patient Lesion Load Area
    # #
    # self.setLesionLoadBooleanWidget = ctk.ctkCheckBox()
    # self.setLesionLoadBooleanWidget.setChecked(True)
    # self.setLesionLoadBooleanWidget.setToolTip("Output the lesion load metric estimated from the output label.")
    # parametersAdvancedFormLayout.addRow("Estimates Patient Lesion Load ", self.setLesionLoadBooleanWidget)

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
    logic.run(self.inputFASelector.currentNode()
              ,self.inputMDSelector.currentNode()
              ,self.inputRASelector.currentNode()
              ,self.inputPerDSelector.currentNode()
              ,self.inputParDSelector.currentNode()
              ,self.outputSelector.currentNode()
              ,self.setOutputLesionMaskBooleanWidget
              ,self.setWhiteMatterTracksBooleanWidget
              ,self.setInterpolationMethodBooleanWidget
              ,self.setTemplateResolutionBooleanWidget.currentText
              ,self.setDTITemplateWidget.currentText
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

  def hasImageData(self,volumeNode):
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
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True


  def run(self, inputFAVolume, inputMDVolume, inputRAVolume, inputPerDVolume, inputParDVolume, outputLabelVolume, outputLesionMaskComboBox, whiteMatterMaskType, interpolationMethod, templateDTIResolution, templateDTI):
    """
    Run the actual algorithm
    """
    logging.info('Processing started')
    slicer.util.showStatusMessage("Processing started")

    slicer.util.showStatusMessage("Step 1: Reading DTI Template...")
    if platform.system() is "Windows":
      home = expanduser("%userprofile%")
    else:
      home = expanduser("~")


    # Register images with the DTI template (interpolation, template resolution)
    if platform.system() is "Windows":
      if (templateDTIResolution == '1mm') & (templateDTI == 'JHU'):
        DTITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz')
        DTITemplateNodeName = "JHU-ICBM-FA-1mm"
        T1Template = "MNI152_T1_1mm_brain_wm"
      elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU'):
        DTITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz')
        DTITemplateNodeName = "JHU-ICBM-FA-2mm"
        T1Template = "MNI152_T1_2mm_brain_wm"
      elif (templateDTIResolution == '1mm') & (templateDTI == 'USP'):
        DTITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-1mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz')
        DTITemplateNodeName = "USP-ICBM-FA-1mm"
        T1Template = "MNI152_T1_1mm_brain_wm"
      else:
        DTITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-2mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz')
        DTITemplateNodeName = "USP-ICBM-FA-2mm"
        T1Template = "MNI152_T1_2mm_brain_wm"
    else:
      if (templateDTIResolution == '1mm') & (templateDTI == 'JHU'):
        DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz')
        DTITemplateNodeName = "JHU-ICBM-FA-1mm"
        T1Template = "MNI152_T1_1mm_brain_wm"
      elif (templateDTIResolution == '2mm') & (templateDTI == 'JHU'):
        DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-2mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz')
        DTITemplateNodeName = 'JHU-ICBM-FA-2mm'
        T1Template = "MNI152_T1_2mm_brain_wm"
      elif (templateDTIResolution == '1mm') & (templateDTI == 'USP'):
        DTITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-1mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz')
        DTITemplateNodeName = "USP-ICBM-FA-1mm"
        T1Template = "MNI152_T1_1mm_brain_wm"
      else:
        DTITemplate  = slicer.util.loadVolume(home + '/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-2mm.nii.gz')
        MNITemplate = slicer.util.loadVolume(home + '/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz')
        DTITemplateNodeName = "USP-ICBM-FA-2mm"
        T1Template = "MNI152_T1_2mm_brain_wm"


    slicer.util.showStatusMessage("Step 2: Registering the input maps to DTI Template space...")

    slicer.util.showStatusMessage("Registering FA map...")
    #
    # Registering the FA image with the MNI-DTI template.
    #
    registrationTransform = slicer.vtkMRMLBSplineTransformNode()
    slicer.mrmmrmlScene.AddNode(registrationTransform)
    inputFAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(inputFAVolume_reg)
    regParams = {}
    regParams["fixedVolume"] = slicer.util.getNode(DTITemplateNodeName)
    regParams["movingVolume"] = inputFAVolume.GetID()
    regParams["samplingPercentage"] = 0.02
    regParams["splineGridSize"] = '14,10,12'
    regParams["outputVolume"] = inputFAVolume_reg.GetID()
    regParams["bsplineTransform"] = registrationTransform.GetID()
    regParams["initializeTransformMode"] = "useMomentsAlign"
    regParams["useRigid"] = True
    regParams["useAffine"] = True
    regParams["useBSpline"] = True
    regParams["interpolationMode"] = interpolationMethod.currentText
    regParams["numberOfSamples"] = 200000

    slicer.cli.run(slicer.modules.brainsfit, None, regParams, wait_for_completion=True)

    #
    # Applying registration transform - MD Volume
    #
    if inputMDVolume != None:
      slicer.util.showStatusMessage("Registering MD map...")
      #
      # Registering the MD image with the MNI-DTI template.
      #
      # USE THE BSPLINE TRANSFORM IN THE FA MAP TO WARP THE REST OF THE INPUT IMAGES
      inputMDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputMDVolume_reg)
      resampMDParams = {}
      resampMDParams["inputVolume"] = inputMDVolume.GetID()
      resampMDParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
      resampMDParams["outputVolume"] = inputMDVolume_reg.GetID()
      resampMDParams["warpTransform"] = registrationTransform.GetID()
      resampMDParams["interpolationMode"] = interpolationMethod.currentText
      # Parameter(0 / 0): inputVolume(ImageTo Warp)
      # Parameter(0 / 1): referenceVolume(Reference Image)
      # Parameter(1 / 0): outputVolume(Output Image)
      # Parameter(1 / 1): pixelType(Pixel Type)
      # Parameter(2 / 0): deformationVolume(Displacement Field(deprecated))
      # Parameter(2 / 1): warpTransform(Transform file)
      # Parameter(2 / 2): interpolationMode(Interpolation Mode)

      # slicer.cli.run(slicer.modules.brainsresample, None, resampMDParams, wait_for_completion=True)


    #
    # Applying registration transform - RA Volume
    #
    if inputRAVolume != None:
      slicer.util.showStatusMessage("Registering RA map...")
      #
      # Registering the RA image with the MNI-DTI template.
      #
      inputRAVolume_reg = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputRAVolume_reg)
      resampRAParams = {}
      resampRAParams["inputVolume"] = inputRAVolume.GetID()
      resampRAParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
      resampRAParams["outputVolume"] = inputRAVolume_reg.GetID()
      resampRAParams["warpTransform"] = registrationTransform.GetID()
      resampRAParams["interpolationMode"] = interpolationMethod.currentText

      slicer.cli.run(slicer.modules.brainsresample, None, resampRAParams, wait_for_completion=True)


    if inputPerDVolume != None:
      slicer.util.showStatusMessage("Registering Perpendicular Diffusivity map...")
      #
      # Registering the Per Diff image with the MNI-DTI template.
      #
      inputPerDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputPerDVolume_reg)
      resampPerDParams = {}
      resampPerDParams["inputVolume"] = inputPerDVolume.GetID()
      resampPerDParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
      resampPerDParams["outputVolume"] = inputPerDVolume_reg.GetID()
      resampPerDParams["warpTransform"] = registrationTransform.GetID()
      resampPerDParams["interpolationMode"] = interpolationMethod.currentText

      slicer.cli.run(slicer.modules.brainsresample, None, resampPerDParams, wait_for_completion=True)

    if inputParDVolume != None:
      slicer.util.showStatusMessage("Registering Parallel Diffusivity map...")
      #
      # Registering the Per Diff image with the MNI-DTI template.
      #
      inputParDVolume_reg = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputParDVolume_reg)
      resampParDParams = {}
      resampParDParams["inputVolume"] = inputParDVolume.GetID()
      resampParDParams["referenceVolume"] = slicer.util.getNode(DTITemplateNodeName)
      resampParDParams["outputVolume"] = inputParDVolume_reg.GetID()
      resampParDParams["warpTransform"] = registrationTransform.GetID()
      resampParDParams["interpolationMode"] = interpolationMethod.currentText

      slicer.cli.run(slicer.modules.brainsresample, None, resampParDParams, wait_for_completion=True)

    #
    # Prepare the white matter mask from MNI152-T1
    #

    slicer.util.showStatusMessage("Step 3: Masking the white matter in the input volumes ")

    slicer.util.showStatusMessage("Masking FA white matter volume...")
    #
    # FA White Matter
    #
    inputFAVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(inputFAVolume_reg_wm)
    applyFAMaskParams = {}
    applyFAMaskParams["InputVolume"] = inputFAVolume_reg.GetID()
    applyFAMaskParams["MaskVolume"] = slicer.util.getNode(T1Template)
    applyFAMaskParams["Label"] = 3
    applyFAMaskParams["OutputVolume"] = inputFAVolume_reg_wm.GetID()

    # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyFAMaskParams, wait_for_completion=True)


    if inputMDVolume!=None:
      slicer.util.showStatusMessage("Masking MD white matter volume...")
      #
      # MD White Matter
      #
      inputMDVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputMDVolume_reg_wm)
      applyMDMaskParams = {}
      # applyMDMaskParams["InputVolume"] = inputMDNode_reg.GetID()
      applyMDMaskParams["MaskVolume"] = slicer.util.getNode(T1Template)
      applyMDMaskParams["Label"] = 3
      applyMDMaskParams["OutputVolume"] = inputMDVolume_reg_wm.GetID()

      # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyMDMaskParams, wait_for_completion=True)

    if inputRAVolume != None:
      slicer.util.showStatusMessage("Masking RA white matter volume...")
      #
      # RA White Matter
      #
      inputRAVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputRAVolume_reg_wm)
      applyRAMaskParams = {}
      applyRAMaskParams["InputVolume"] = inputRAVolume_reg.GetID()
      applyRAMaskParams["MaskVolume"] = slicer.util.getNode(T1Template)
      applyRAMaskParams["Label"] = 3
      applyRAMaskParams["OutputVolume"] = inputRAVolume_reg_wm.GetID()

      # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyRAMaskParams, wait_for_completion=True)

    if inputPerDVolume != None:
      slicer.util.showStatusMessage("Masking Perpendicular Diffusivity white matter volume...")
      #
      # Perpendicular Diffusivity White Matter
      #
      inputPerDVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputPerDVolume_reg_wm)
      applyPerDMaskParams = {}
      applyPerDMaskParams["InputVolume"] = inputPerDVolume_reg.GetID()
      applyPerDMaskParams["MaskVolume"] = slicer.util.getNode(T1Template)
      applyPerDMaskParams["Label"] = 3
      applyPerDMaskParams["OutputVolume"] = inputPerDVolume_reg_wm.GetID()

      # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyPerDMaskParams, wait_for_completion=True)

    if inputParDVolume != None:
      slicer.util.showStatusMessage("Masking Parallel Diffusitivy white matter volume...")
      #
      # Parallel Diffusivity White Matter
      #
      inputParDVolume_reg_wm = slicer.vtkMRMLScalarVolumeNode()
      slicer.mrmlScene.AddNode(inputParDVolume_reg_wm)
      applyParDMaskParams = {}
      applyParDMaskParams["InputVolume"] = inputParDVolume_reg.GetID()
      applyParDMaskParams["MaskVolume"] = slicer.util.getNode(T1Template)
      applyParDMaskParams["Label"] = 3
      applyParDMaskParams["OutputVolume"] = inputParDVolume_reg_wm.GetID()

      # slicer.cli.run(slicer.modules.maskscalarvolume, None, applyParDMaskParams, wait_for_completion=True)


    slicer.util.showStatusMessage("Step 4: Performing the Bayesian segmentation on all diffusion maps...")
    #
    # Perform the statistical segmentation - FA map
    #
    outputFALesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
    slicer.mrmlScene.AddNode(outputFALesionLabelNode)
    statisticalFASegmentationParams = {}
    # statisticalFASegmentationParams["inputVolume"] =
    # statisticalFASegmentationParams["mapType"] =
    # statisticalFASegmentationParams["mapResolution"] =
    # statisticalFASegmentationParams["statMethod"] =
    # statisticalFASegmentationParams["zThreshold"] =
    statisticalFASegmentationParams["outputLabelVolume"] = outputLabelVolume

    # slicer.cli.run(slicer.modules.statisticalbrainsegmentation, None, statisticalFASegmentationParams, wait_for_completion=True)


    # if inputMDVolume != None:
    #   #
    #   # Perform the statistical segmentation - MD map
    #   #
    #   outputLesionLabelNode = slicer.vtkMRMLLabelMapVolumeNode()
    #   slicer.mrmlScene.AddNode(outputLesionLabelNode)
    #   statisticalSegmentationParams = {}
    #   # statisticalSegmentationParams["inputVolume"] =
    #   # statisticalSegmentationParams["mapType"] =
    #   # statisticalSegmentationParams["mapResolution"] =
    #   # statisticalSegmentationParams["statMethod"] =
    #   # statisticalSegmentationParams["zThreshold"] =
    #   statisticalSegmentationParams["outputLabelVolume"] = outputLabelVolume
    #
    #   # slicer.cli.run(slicer.modules.statisticalbrainsegmentation, None, statisticalSegmentationParams, wait_for_completion=True)


    # #
    # # Split the lesion label
    # #
    # if outputLesionMaskComboBox.currentText != "Global":
    #


    slicer.util.showStatusMessage("Processing completed!")

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

    for url,name,loader in downloads:
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
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
