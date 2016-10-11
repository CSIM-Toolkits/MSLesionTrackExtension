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

if (WIN32)
    add_custom_target(build-time-MSLesionTrack-directory ALL
        COMMAND ${CMAKE_COMMAND} -E make_directory %userprofile%\\MSLesionTrack-Data)
endif (WIN32)
if (UNIX)
    add_custom_target(build-time-MSLesionTrack-directory ALL
        COMMAND ${CMAKE_COMMAND} -E make_directory ~/MSLesionTrack-Data)
endif (UNIX)

## we don't want to copy if we're building in the source dir
if (NOT CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)

    # list of files for which we add a copy rule
    if (WIN32)
        set(INPUTS
            DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz
            DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz
            DTI-Templates\\USP-ICBM-FA-20-1mm.nii.gz
            DTI-Templates\\USP-ICBM-FA-20-2mm.nii.gz
	    DTI-Templates\\USP-ICBM-FA-131-1mm.nii.gz
            DTI-Templates\\USP-ICBM-FA-131-2mm.nii.gz
	    DTI-Templates\\USP-ICBM-MD-131-1mm.nii.gz
            DTI-Templates\\USP-ICBM-MD-131-2mm.nii.gz
	    DTI-Templates\\USP-ICBM-RA-131-1mm.nii.gz
            DTI-Templates\\USP-ICBM-RA-131-2mm.nii.gz
	    DTI-Templates\\USP-ICBM-VR-131-1mm.nii.gz
            DTI-Templates\\USP-ICBM-VR-131-2mm.nii.gz
	    DTI-Templates\\USP-ICBM-PerpDiff-131-1mm.nii.gz
            DTI-Templates\\USP-ICBM-PerpDiff-131-2mm.nii.gz

            WMTracts-Templates\\JHU-ICBM-tracts-prob-2mm.nii.gz
            WMTracts-Templates\\JHU-ICBM-tracts-prob-1mm.nii.gz

            Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz
            Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz
   	    Structural-Templates\\MNI152_T1_1mm_brain.nii.gz
	    Structural-Templates\\MNI152_T1_2mm_brain.nii.gz

            StatisticalBrainSegmentation-Templates\\USP-ICBM-FAmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-FAmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MDmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MDmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-RAmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-RAmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-VRmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-VRmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-FAstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-FAstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MDstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MDstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-RAstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-RAstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-VRstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-VRstd-131-2mm.nii.gz

	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MSLesionPriors-46-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates\\USP-ICBM-MSLesionPriors-46-2mm.nii.gz
            )
    endif (WIN32)
    if (UNIX)
        set(INPUTS
            DTI-Templates/JHU-ICBM-FA-1mm.nii.gz
            DTI-Templates/JHU-ICBM-FA-2mm.nii.gz
            DTI-Templates/USP-ICBM-FA-20-1mm.nii.gz
            DTI-Templates/USP-ICBM-FA-20-2mm.nii.gz
	    DTI-Templates/USP-ICBM-FA-131-1mm.nii.gz
            DTI-Templates/USP-ICBM-FA-131-2mm.nii.gz
	    DTI-Templates/USP-ICBM-MD-131-1mm.nii.gz
            DTI-Templates/USP-ICBM-MD-131-2mm.nii.gz
	    DTI-Templates/USP-ICBM-RA-131-1mm.nii.gz
            DTI-Templates/USP-ICBM-RA-131-2mm.nii.gz
	    DTI-Templates/USP-ICBM-VR-131-1mm.nii.gz
            DTI-Templates/USP-ICBM-VR-131-2mm.nii.gz
	    DTI-Templates/USP-ICBM-PerpDiff-131-1mm.nii.gz
            DTI-Templates/USP-ICBM-PerpDiff-131-2mm.nii.gz

            WMTracts-Templates/JHU-ICBM-tracts-prob-2mm.nii.gz
            WMTracts-Templates/JHU-ICBM-tracts-prob-1mm.nii.gz

            Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz
            Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz
   	    Structural-Templates/MNI152_T1_1mm_brain.nii.gz
	    Structural-Templates/MNI152_T1_2mm_brain.nii.gz

            StatisticalBrainSegmentation-Templates/USP-ICBM-FAmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-FAmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-MDmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-MDmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-RAmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-RAmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-VRmean-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-VRmean-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-FAstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-FAstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-MDstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-MDstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-RAstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-RAstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffstd-131-2mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-VRstd-131-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-VRstd-131-2mm.nii.gz

            StatisticalBrainSegmentation-Templates/USP-ICBM-MSLesionPriors-46-1mm.nii.gz
	    StatisticalBrainSegmentation-Templates/USP-ICBM-MSLesionPriors-46-2mm.nii.gz

	    diffeomorphicRegistration.sh
	    antsRegistrationSyN.sh
	    antsRegistrationSyNQuick.sh
            )
    endif (UNIX)


    foreach(item IN LISTS INPUTS)
        message(STATUS ${item})
        if (WIN32)
            add_custom_command(
                #                TARGET ${MODULE_NAME} PRE_BUILD
                OUTPUT "%userprofile%\\MSLesionTrack-Data\\${item}"
                COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_SOURCE_DIR}\\${item}" "%userprofile%\\MSLesionTrack-Data\\${item}"
                DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}\\${item}"
                )
        endif (WIN32)
        if (UNIX)
            add_custom_command(
                #                TARGET ${MODULE_NAME} PRE_BUILD
                OUTPUT "~/MSLesionTrack-Data/${item}"
                COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_SOURCE_DIR}/${item}" "~/MSLesionTrack-Data/${item}"
                DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/${item}"
                )
        endif (UNIX)
    endforeach()
endif()

if (WIN32)
    add_custom_target(data-MSLesionTrack ALL DEPENDS
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\JHU-ICBM-FA-2mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-20-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-FA-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-MD-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-RA-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-VR-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\DTI-Templates\\USP-ICBM-PerpDiff-131-2mm.nii.gz"

        "%userprofile%\\MSLesionTrack-Data\\WMTracts-Templates\\JHU-ICBM-tracts-prob-2mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\WMTracts-Templates\\JHU-ICBM-tracts-prob-1mm.nii.gz"

        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain_wm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain_wm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_2mm_brain.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\Structural-Templates\\MNI152_T1_1mm_brain.nii.gz"

        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-FAmean-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-FAmean-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MDmean-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MDmean-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffmean-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffmean-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-RAmean-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-RAmean-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-VRmean-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-VRmean-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-FAstd-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-FAstd-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MDstd-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MDstd-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffstd-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-PerpDiffstd-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-RAstd-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-RAstd-131-2mm.nii.gz"
	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-VRstd-131-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-VRstd-131-2mm.nii.gz"

	"%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MSLesionPriors-46-1mm.nii.gz"
        "%userprofile%\\MSLesionTrack-Data\\StatisticalBrainSegmentation-Templates\\USP-ICBM-MSLesionPriors-46-2mm.nii.gz"
        )
endif (WIN32)
if (UNIX)
    add_custom_target(data-MSLesionTrack ALL DEPENDS
        "~/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/JHU-ICBM-FA-2mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-20-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-20-2mm.nii.gz"
	"~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-FA-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-MD-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-VR-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-RA-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/DTI-Templates/USP-ICBM-PerpDiff-131-2mm.nii.gz"

        "~/MSLesionTrack-Data/WMTracts-Templates/JHU-ICBM-tracts-prob-2mm.nii.gz"
        "~/MSLesionTrack-Data/WMTracts-Templates/JHU-ICBM-tracts-prob-1mm.nii.gz"

        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain_wm.nii.gz"
        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain_wm.nii.gz"
        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_2mm_brain.nii.gz"
        "~/MSLesionTrack-Data/Structural-Templates/MNI152_T1_1mm_brain.nii.gz"

        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-FAmean-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-FAmean-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MDmean-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MDmean-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffmean-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffmean-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-RAmean-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-RAmean-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-VRmean-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-VRmean-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-FAstd-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-FAstd-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MDstd-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MDstd-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffstd-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-PerpDiffstd-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-RAstd-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-RAstd-131-2mm.nii.gz"
	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-VRstd-131-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-VRstd-131-2mm.nii.gz"

	"~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MSLesionPriors-46-1mm.nii.gz"
        "~/MSLesionTrack-Data/StatisticalBrainSegmentation-Templates/USP-ICBM-MSLesionPriors-46-2mm.nii.gz"

	"~/MSLesionTrack-Data/diffeomorphicRegistration.sh"
	"~/MSLesionTrack-Data/antsRegistrationSyN.sh"
	"~/MSLesionTrack-Data/antsRegistrationSyNQuick.sh"
        )
endif (UNIX)

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

    # Register the unittest subclass in the main script as a ctest.
    # Note that the test will also be available at runtime.
    slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

    # Additional build-time testing
    add_subdirectory(Testing)
endif()
