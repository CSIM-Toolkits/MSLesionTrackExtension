#!/bin/bash

usage(){
  echo "This script is intended to call the ANTs registration procedure in order to perform diffeomorphic SyN registration on DTI scalar maps."
  echo "(basename $0) <Main folder> <Quick registration [Y/N]>"
  echo ""
  echo  "Main folder = The location where is found the input files for ANTs registration."
  echo  "Quick registration = Choose if use the fast ANTs registration script. Default = N"
}

if [[ $# -lt 2 ]]; then
  usage
  exit
fi

MAIN_FOLDER=$1
USE_QUICK=$2

if [[ -d "$MAIN_FOLDER" ]]; then
  #Performing registration
  if [[ $USE_QUICK == "Y" ]]; then
    cd ${MAIN_FOLDER}
    ~/MSLesionTrack-Data/antsRegistrationSyNQuick.sh -d 3 -f patient-FA.nii.gz -m DTI-Template-FA.nii.gz -o regTemplate
  elif [[ $USE_QUICK == "N" ]]; then
    cd ${MAIN_FOLDER}
    ~/MSLesionTrack-Data/antsRegistrationSyN.sh -d 3 -f patient-FA.nii.gz -m DTI-Template-FA.nii.gz -o regTemplate
  else
    echo "Quick registration is Y or N."
    exit
  fi
else
    echo "The input directory does not exist!"
    exit
fi
