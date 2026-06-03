##############################################################################
# cmake configuration file for LCContent
#
# returns following variables:
#
#   LCContent_FOUND      : set to TRUE if LCContent found
#
#   LCContent_ROOT       : path to this LCContent installation
#   LCContent_VERSION    : package version
#   LCContent_LIBRARIES  : list of LCContent libraries (NOT including COMPONENTS)
#   LCContent_INCLUDE_DIRS  : list of paths to be used with INCLUDE_DIRECTORIES
#   LCContent_LIBRARY_DIRS  : list of paths to be used with LINK_DIRECTORIES
#
##############################################################################

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was LCContentConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set_and_check(LCContent_ROOT "/scratch/trholmes/mucol/v2.11/LCContent/install")
set_and_check(LCContent_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include")
set_and_check(LCContent_LIBRARY_DIRS "${PACKAGE_PREFIX_DIR}/lib")
set(LCContent_LIBRARIES "LCContent::LCContent")

include(CMakeFindDependencyMacro)
find_dependency(PandoraSDK REQUIRED)

include("${CMAKE_CURRENT_LIST_DIR}/LCContentTargets.cmake")

check_required_components(LCContent)

