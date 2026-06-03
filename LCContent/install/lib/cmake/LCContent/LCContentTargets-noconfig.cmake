#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "LCContent::LCContent" for configuration ""
set_property(TARGET LCContent::LCContent APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(LCContent::LCContent PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libLCContent.so"
  IMPORTED_SONAME_NOCONFIG "libLCContent.so"
  )

list(APPEND _cmake_import_check_targets LCContent::LCContent )
list(APPEND _cmake_import_check_files_for_LCContent::LCContent "${_IMPORT_PREFIX}/lib/libLCContent.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
