#-----------------------------------------------------------------------------
set(MODULE_NAME DTILesionTrack)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
    ${MODULE_NAME}.py
    )

set(MODULE_PYTHON_RESOURCES
    Resources/Icons/${MODULE_NAME}.png
    )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
    NAME ${MODULE_NAME}
    SCRIPTS ${MODULE_PYTHON_SCRIPTS}
    RESOURCES ${MODULE_PYTHON_RESOURCES}
    WITH_GENERIC_TESTS
    )

#if (WIN32)
#    add_custom_target(build-time-MSLesionTrack-directory ALL
#        COMMAND ${CMAKE_COMMAND} -E make_directory %userprofile%\\MSLesionTrack-Data)
#endif (WIN32)
#if (UNIX)
#    add_custom_target(build-time-MSLesionTrack-directory ALL
#        COMMAND ${CMAKE_COMMAND} -E make_directory ~/MSLesionTrack-Data)
#endif (UNIX)

### we don't want to copy if we're building in the source dir
#if (NOT CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)

#    # list of files for which we add a copy rule
#    if (WIN32)
#        set(INPUTS
#            DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz
#            DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz
#            DTI-Templates\\USP-ICBM-FA-256-1mm.nii.gz
#            DTI-Templates\\USP-ICBM-FA-256-2mm.nii.gz
#            WMTracts-Templates\\JHU-ICBM-tracts-prob-2mm.nii.gz
#            WMTracts-Templates\\JHU-ICBM-tracts-prob-1mm.nii.gz
#            Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz
#            Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statFA-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statMD-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statRA-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statVR-1mm.nii.gz
##            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPerD-1mm.nii.gz
##            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPard-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statFA-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statMD-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statRA-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statVR-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPerD-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPard-2mm.nii.gz

#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-FA-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-MD-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-RA-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-Tr-1mm.nii.gz
##                        StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-PerD-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-ParD-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-FA-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-MD-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-RA-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-Tr-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-PerD-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-ParD-2mm.nii.gz
#            )
#    endif (WIN32)
#    if (UNIX)
#        set(INPUTS
#            DTI-Templates/JHU-ICBM-FA-1mm.nii.gz
#            DTI-Templates/JHU-ICBM-FA-2mm.nii.gz
#            DTI-Templates/USP-ICBM-FA-256-1mm.nii.gz
#            DTI-Templates/USP-ICBM-FA-256-2mm.nii.gz
#            WMTracts-Templates/JHU-ICBM-tracts-prob-2mm.nii.gz
#            WMTracts-Templates/JHU-ICBM-tracts-prob-1mm.nii.gz
#            Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz
#            Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statFA-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statMD-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statRA-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statVR-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statPerD-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statParD-1mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statFA-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statMD-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statRA-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statVR-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statPerD-2mm.nii.gz
#            StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statParD-2mm.nii.gz

#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-FA-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-MD-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-RA-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-Tr-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-PerD-1mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-ParD-1mm.nii.gz
#            #           StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-FA-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-MD-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-RA-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-Tr-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-PerD-2mm.nii.gz
#            #            StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-ParD-2mm.nii.gz
#            )
#    endif (UNIX)


#    foreach(item IN LISTS INPUTS)
#        message(STATUS ${item})
#        if (WIN32)
#            add_custom_command(
#                #                TARGET ${MODULE_NAME} PRE_BUILD
#                OUTPUT "%userprofile%\\MSLesionTrack-Data\\${item}"
#                COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_SOURCE_DIR}\\${item}" "%userprofile%\\MSLesionTrack-Data\\${item}"
#                DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}\\${item}"
#                )
#        endif (WIN32)
#        if (UNIX)
#            add_custom_command(
#                #                TARGET ${MODULE_NAME} PRE_BUILD
#                OUTPUT "~/MSLesionTrack-Data/${item}"
#                COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_SOURCE_DIR}/${item}" "~/MSLesionTrack-Data/${item}"
#                DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/${item}"
#                )
#        endif (UNIX)
#    endforeach()
#endif()

#if (WIN32)
#    add_custom_target(data-MSLesionTrack ALL DEPENDS
#        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-256-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-256-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\WMTracts-Templates\\JHU-ICBM-tracts-prob-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\WMTracts-Templates\\JHU-ICBM-tracts-prob-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statFA-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statMD-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statVR-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statRA-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPerD-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statParD-1mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statFA-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statMD-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statVR-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statRA-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statPerD-2mm.nii.gz"
#        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-20-N16-statParD-2mm.nii.gz"

#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-FA-1mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-MD-1mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-Tr-1mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-RA-1mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-PerD-1mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-ParD-1mm.nii.gz"
#        #   "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-FA-2mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-MD-2mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-Tr-2mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-RA-2mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-PerD-2mm.nii.gz"
#        #    "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MS-BayesPriors-ParD-2mm.nii.gz"
#        )
#endif (WIN32)
#if (UNIX)
#    add_custom_target(data-MSLesionTrack ALL DEPENDS
#        "~/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz"
#        "~/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-2mm.nii.gz"
#        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-256-1mm.nii.gz"
#        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-256-2mm.nii.gz"
#        "~/MSLesionTrack-Data/WMTracts-Templates/JHU-ICBM-tracts-prob-2mm.nii.gz"
#        "~/MSLesionTrack-Data/WMTracts-Templates/JHU-ICBM-tracts-prob-1mm.nii.gz"
#        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz"
#        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statFA-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statMD-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statRA-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statVR-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statPerD-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statParD-1mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statFA-2mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statMD-2mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statRA-2mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statVR-2mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statPerD-2mm.nii.gz"
#        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-20-N16-statParD-2mm.nii.gz"

#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-FA-1mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-MD-1mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-RA-1mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-Tr-1mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-PerD-1mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-ParD-1mm.nii.gz"
#        #   "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-FA-2mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-MD-2mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-RA-2mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-Tr-2mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-PerD-2mm.nii.gz"
#        #    "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MS-BayesPriors-ParD-2mm.nii.gz"
#        )
#endif (UNIX)

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

    # Register the unittest subclass in the main script as a ctest.
    # Note that the test will also be available at runtime.
    slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

    # Additional build-time testing
    add_subdirectory(Testing)
endif()