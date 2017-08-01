#-----------------------------------------------------------------------------
set(MODULE_NAME DTILesionTrack)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
    ${MODULE_NAME}.py
    )

file(GLOB DTILesionTrack_Template RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/DTI-Templates/*.nii.gz")
file(GLOB DTILesionTrack_StatTemplates RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/StatisticalBrainSegmentation-Templates/*.nii.gz")
file(GLOB DTILesionTrack_StructTemplates RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/Structural-Templates/*.nii.gz")
file(GLOB DTILesionTrack_WMTemplates RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/WMTracts-Templates/*.nii.gz")
file(GLOB DTILesionTrack_Scripts RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}" "Resources/*.sh")
set(MODULE_PYTHON_RESOURCES
    Resources/Icons/${MODULE_NAME}.png
    ${DTILesionTrack_Template}
    ${DTILesionTrack_StatTemplates}
    ${DTILesionTrack_StructTemplates}
    ${DTILesionTrack_WMTemplates}
    ${DTILesionTrack_Scripts}
    )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
    NAME ${MODULE_NAME}
    SCRIPTS ${MODULE_PYTHON_SCRIPTS}
    RESOURCES ${MODULE_PYTHON_RESOURCES}
    WITH_GENERIC_TESTS
    )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

    # Register the unittest subclass in the main script as a ctest.
    # Note that the test will also be available at runtime.
    slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

    # Additional build-time testing
    add_subdirectory(Testing)
endif()
