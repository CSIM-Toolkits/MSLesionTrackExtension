#!/bin/bash

usage(){
  echo "This script is intended to call the ANTs registration procedure in order to perform diffeomorphic SyN registration on DTI scalar maps."
  echo "(basename $0) <Main folder> <Quick registration [Y/N]> <Structural Registration [Y/N]> <Scripts directory>"
  echo ""
  echo  "Main folder = The location where is found the input files for ANTs registration."
  echo  "Quick registration = Choose if use the fast ANTs registration script. Default = N"
  echo  "Structural Registration = Do registration on structural images. Default = N"
  echo  "Scripts directory = The full path to the directory that contains the registration scripts. Default = the python resources path. "
}

if [[ $# -lt 3 ]]; then
  usage
  exit
fi

MAIN_FOLDER=$1
USE_QUICK=$2
STRUCTURAL_REGISTRATION=$3
SCRIPTS_PATH=$4

if [[ -d "$MAIN_FOLDER" ]]; then
  #Performing registration
  if [[ $USE_QUICK == "Y" && $STRUCTURAL_REGISTRATION == "N" ]]; then
    cd ${MAIN_FOLDER}
    $SCRIPTS_PATH/antsRegistrationSyNQuick.sh -d 3 -f patient-FA.nii.gz -m DTI-Template-FA.nii.gz -o regTemplate
  elif [[ $USE_QUICK == "N" && $STRUCTURAL_REGISTRATION == "N" ]]; then
    cd ${MAIN_FOLDER}
    $SCRIPTS_PATH/antsRegistrationSyN.sh -d 3 -f patient-FA.nii.gz -m DTI-Template-FA.nii.gz -o regTemplate
  elif [[ $USE_QUICK == "Y" && $STRUCTURAL_REGISTRATION == "Y" ]]; then
    cd ${MAIN_FOLDER}
    $SCRIPTS_PATH/antsRegistrationSyNQuick.sh -d 3 -f patient-FLAIR.nii.gz -m MNI-Template-T1.nii.gz -o regStruct
  elif [[ $USE_QUICK == "N" && $STRUCTURAL_REGISTRATION == "Y" ]]; then
    cd ${MAIN_FOLDER}
    $SCRIPTS_PATH/antsRegistrationSyN.sh -d 3 -f patient-FLAIR.nii.gz -m MNI-Template-T1.nii.gz -o regStruct
  else
    echo "Quick registration is Y or N."
    exit
  fi
else
    echo "The input directory does not exist!"
    exit
fi
