# Copyright 2017 Shaheed Haque <srhaque@theiet.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#
# This is a helper script used to locate binaries, libraries and other
# platform-dependent items for use in creating Python bindings based on
# https://pypi.python.org/pypi/cppyy.
#
# The main content is the function get_binding_info_kf5() which simplifies
# gathering the information needed by the CMake support code packaged with
# https://pypi.python.org/pypi/cppyy-backend as CPPYY_ADD_BINDINGS().
#
# Example:
#
# #
# # Get the information needed to create create bindings for a set of related
# # KF5 components.
# #
# get_binding_info_kf5(
#     COMPONENTS KF5Akonadi KF5AkonadiCalendar KF5AkonadiContact KF5AkonadiMime KF5AkonadiNotes KF5AkonadiSearch
#     NATIVE_COMPONENTS KF5AkonadiSearch
#     DEPENDENCIES KF5Konq KF5Attica)
# #
# # Customise the automatically generated information.
# #
# list(FILTER h_files EXCLUDE REGEX ".*_export.h")
# list(FILTER h_files EXCLUDE REGEX ".*_version.h")
# list(FILTER h_files EXCLUDE REGEX ".*/qtest_akonadi.h")
# list(APPEND include_dirs ${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}/KF5)
# #
# # Generate the bindings for KF5.Akonadi.
# #
# CPPYY_ADD_BINDINGS(
#     "KF5.Akonadi" "${version}" "Shaheed" "srhaque@theiet.org"
#     LANGUAGE_STANDARD "14"
#     GENERATE_OPTIONS "-D__PIC__;-Wno-macro-redefined"
#     INCLUDE_DIRS ${include_dirs}
#     COMPILE_OPTIONS "-Wno-deprecated-declarations"
#     LINK_LIBRARIES ${link_libraries}
#     LINKDEFS "#include <QString>\n"
#     H_DIRS ${h_dirs}
#     H_FILES ${h_files})
#
cmake_minimum_required(VERSION 3.9)

execute_process(COMMAND cling-config --cmake
    OUTPUT_VARIABLE _stdout
    ERROR_VARIABLE _stderr
    RESULT_VARIABLE _rc
    OUTPUT_STRIP_TRAILING_WHITESPACE)
if(_rc)
    message(FATAL_ERROR "Error finding cling's CMake support: (${_rc}) ${_stderr}")
endif()
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${_stdout})
find_package(Cppyy 0.8.4 REQUIRED)

#include(FeatureSummary)
include(FindPkgConfig)
include(CMakeFindDependencyMacro)

#
# Find the includes, libraries etc. for a pkg-config component.
#
function(get_pkgconfig_info component)
    set(libraries)
    set(includes ${${component}_INCLUDEDIR})
    set(compile_flags ${${component}_CFLAGS})
    foreach(tmp ${${component}_LIBRARIES})
        find_library(lib${tmp} NAMES ${tmp} PATHS ${${component}_LIBRARIES})
        list(APPEND libraries ${lib${tmp}})
    endforeach()
    set(libraries "${libraries}" PARENT_SCOPE)
    set(includes "${includes}" PARENT_SCOPE)
    set(compile_flags "${compile_flags}" PARENT_SCOPE)
endfunction(get_pkgconfig_info)

#
# Find the targets and dependencies for a CMake KDE component.
#
set(_DEPENDENCIES)
function(get_kf5_cmake_info component)
    find_dependency(${component})
    set(real_targets)
    set(real_dependencies)
    #
    # Loop over all cmake files.
    #
    set(file_glob  ${${component}_DIR}/*.cmake)
    file(GLOB files ${file_glob})
    foreach(f ${files})
        #
        # Targets.
        #
        file(STRINGS ${f} matches REGEX "^ *add_library\\(.*\\) *")
        if(NOT matches STREQUAL "")
            foreach(target ${matches})
                string(REGEX REPLACE " *add_library\\(([^ \\)]+).*" "\\1" target ${target})
                if(TARGET ${target})
                    list(APPEND real_targets ${target})
                    if(real_targets)
                        list(REMOVE_DUPLICATES real_targets)
                    endif()
                else()
                    message(STATUS "Ignoring invalid target \"${target}\" for ${component} in ${f}")
                endif()
            endforeach()
        endif()
        #
        # Dependencies.
        #
        file(STRINGS ${f} matches REGEX "^ *find_dependency\\(.*\\) *")
        if(NOT matches STREQUAL "")
            foreach(dependency ${matches})
                string(REGEX REPLACE " *find_dependency\\(([^ \\)]+).*" "\\1" dependency ${dependency})
                if(NOT ${dependency} STREQUAL "")
                    list(APPEND real_dependencies ${dependency})
                    list(REMOVE_DUPLICATES real_dependencies)
                    #
                    # Recurse...if we have not been here before.
                    #
                    string(FIND ${dependency} "KF5" found)
                    if(found EQUAL 0 AND NOT dependency IN_LIST _DEPENDENCIES)
                        get_kf5_cmake_info(${dependency})
                        list(APPEND real_dependencies ${dependencies})
                        list(REMOVE_DUPLICATES real_dependencies)
                    endif()
                else()
                    message(STATUS "Ignoring invalid dependency \"${dependency}\" for ${component} in ${f}")
                endif()
            endforeach()
        endif()
    endforeach()
    set(targets "${real_targets}" PARENT_SCOPE)
    set(dependencies "${real_dependencies}" PARENT_SCOPE)
endfunction(get_kf5_cmake_info)

#
# Find the targets (and not dependencies!) for a native KDE component.
#
function(get_kf5_native_info component)
    set(_INCLUDE_DIRS)
    string(REGEX REPLACE "^KF5" "" tmp ${component})
    foreach(dir IN LISTS CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES)
        set(dir ${dir}/KF5)
        file(GLOB tmp2 LIST_DIRECTORIES true ${dir}/${tmp}*)
        foreach(tmp3 IN LISTS tmp2)
            if(IS_DIRECTORY ${tmp3})
              if(NOT ${tmp3} IN_LIST _INCLUDE_DIRS)
                list(APPEND _INCLUDE_DIRS ${tmp3})
              endif()
            endif()
        endforeach(tmp3)
        file(GLOB_RECURSE tmp2 LIST_DIRECTORIES true ${dir}/${tmp}/*)
        foreach(tmp3 IN LISTS tmp2)
            if(IS_DIRECTORY ${tmp3})
              if(NOT ${tmp3} IN_LIST _INCLUDE_DIRS)
                list(APPEND _INCLUDE_DIRS ${tmp3})
              endif()
            endif()
        endforeach(tmp3)
    endforeach(dir)
    set(_LIBRARIES)
    foreach(dir IN LISTS CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES)
        file(GLOB_RECURSE tmp2 LIST_DIRECTORIES true ${dir}/${CMAKE_SHARED_LIBRARY_PREFIX}${component}*${CMAKE_SHARED_LIBRARY_SUFFIX})
        foreach(tmp3 IN LISTS tmp2)
            if(NOT IS_DIRECTORY ${tmp3})
              if(NOT ${tmp3} IN_LIST _LIBRARIES)
                list(APPEND _LIBRARIES ${tmp3})
              endif()
            endif()
        endforeach(tmp3)
    endforeach(dir)
    set(libraries "${_LIBRARIES}" PARENT_SCOPE)
    set(includes "${_INCLUDE_DIRS}" PARENT_SCOPE)
    set(compile_flags "" PARENT_SCOPE)
endfunction(get_kf5_native_info)

#
# Find the targets (and not dependencies!) for a CMake Qt component.
#
function(get_qt5_cmake_info component)
    find_dependency(${component})
    #
    # Targets.
    #
    string(REPLACE "Qt5" "Qt5::" target ${component})
    if(NOT TARGET ${target})
        message(STATUS "Ignoring invalid target \"${target}\" for ${component}")
        set(target "")
    endif()
    set(targets "${target}" PARENT_SCOPE)
    #
    # Dependencies.
    #
    set(dependencies "" PARENT_SCOPE)
endfunction(get_qt5_cmake_info)

#
# Fetch a target property, recursing if necessary.
#
function(get_target_property_recursive target property)
    set(result)
    get_target_property(values ${target} ${property})
    if(values STREQUAL "values-NOTFOUND")
        # Skip
        # message(STATUS "Warning: Target ${target} has no property ${property}")
    else()
        foreach(value ${values})
            string(FIND ${value} "$<TARGET_PROPERTY:" found)
            if(found EQUAL 0)
                #
                # Recurse. The format is:
                #
                # $<TARGET_PROPERTY:KF5::WebKit,INTERFACE_INCLUDE_DIRECTORIES>
                #
                string(REGEX REPLACE "\\$<TARGET_PROPERTY:(.*),(.*)>" "\\1" nested_tgt ${value})
                string(REGEX REPLACE "\\$<TARGET_PROPERTY:(.*),(.*)>" "\\2" nested_prop ${value})
                get_target_property_recursive(${nested_tgt} ${nested_prop})
                list(APPEND result ${get_target_property_recursive_result})
            else()
                list(APPEND result ${value})
            endif()
        endforeach()
    endif()
    set(get_target_property_recursive_result "${result}" PARENT_SCOPE)
endfunction(get_target_property_recursive)

#
# Find the includes, libraries etc. for a component.
#
function(get_targets_info component targets)
    if(targets STREQUAL "")
        message(STATUS "Warning: No targets for ${component}")
        return()
    endif()
    #
    # Make a combined list of includes, libraries etc.
    #
    # There is a potential impedence mismatch between the directory-centric
    # Pythonic notion of a package, and the possibility that the the multiple
    # targets *might* have conflicting options. Luckily, this seems not to be
    # a problem in KF5.
    #
    set(libraries)
    set(includes)
    set(compile_flags)
    foreach(target ${targets})
        if(TARGET ${target})
            get_target_property(tmp ${target} LOCATION)
            list(APPEND libraries ${tmp})
            get_target_property_recursive(${target} INTERFACE_INCLUDE_DIRECTORIES)
            list(APPEND includes ${get_target_property_recursive_result})
            get_target_property_recursive(${target} INTERFACE_COMPILE_DEFINITIONS)
            foreach(definition ${get_target_property_recursive_result})
                if(${definition} MATCHES ".*QT_NO_DEBUG>")
                    #
                    # Qt uses the formulation "$<$<NOT:$<CONFIG:Debug>>:QT_NO_DEBUG>".
                    #
                elseif(${definition} MATCHES "QT_.*_LIB")
                    #
                    # Qt uses the formulation "QT_CORE_LIB" even for INTERFACE_COMPILE_FLAGS.
                    #
                else()
                    list(APPEND compile_flags "-D${definition}")
                endif()
            endforeach()
            get_target_property_recursive(${target} INTERFACE_COMPILE_OPTIONS)
            list(APPEND compile_flags ${get_target_property_recursive_result})
        else()
            message(STATUS "Warning: Ignoring invalid target \"${target}\" in ${f}")
        endif()
    endforeach()
    #
    # De-duplicate and write results.
    #
    if(DEFINED includes)
        list(REMOVE_DUPLICATES includes)
        #
        # Not sure why the headers seem to include this.
        #
        list(REMOVE_ITEM includes "${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}")
        list(REMOVE_ITEM includes "${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}/KF5")
    endif()
    if(DEFINED compile_flags)
        list(REMOVE_DUPLICATES compile_flags)
    endif()
    set(libraries "${libraries}" PARENT_SCOPE)
    set(includes "${includes}" PARENT_SCOPE)
    set(compile_flags "${compile_flags}" PARENT_SCOPE)
endfunction(get_targets_info)

#
# Return the information required to create the bindings for a set of KF5 components.
#
#   get_binding_info_kf5(
#       COMPONENTS components
#       NATIVE_COMPONENTS components
#       DEPENDENCIES extras)
#
# Arguments and options:
#
#   COMPONENTS component
#                       The CMake packages to include in the bindings.
#
#   NATIVE_COMPONENTS component
#                       The native packages to include in the bindings.
#
#   DEPENDENCIES dependency
#                       Any CMake packages not detected by the automatic
#                       dependency extraction logic.
#
# Returns via PARENT_SCOPE variables:
#
#   version             The version of the first of the COMPONENTS.
#
#   h_dirs              All include dirs for targets in COMPONENTS and
#                       NATIVE_COMPONENTS.
#
#   h_files             All header files under h_dirs.
#
#   include_dirs        All include dirs for targets in DEPENDENCIES.
#
#   compile_options     All compile options associated with COMPONENTS,
#                       NATIVE_COMPONENTS and DEPENDENCIES.
#
#   link_libraries      All libraries for targets in COMPONENTS and
#                       NATIVE_COMPONENTS and DEPENDENCIES.
#
function(get_binding_info_kf5)
    cmake_parse_arguments(
        ARG
        ""
        ""
        "COMPONENTS;NATIVE_COMPONENTS;DEPENDENCIES"
        ${ARGN})
    if(NOT "${ARG_UNPARSED_ARGUMENTS}" STREQUAL "")
        message(SEND_ERROR "Unexpected arguments specified '${ARG_UNPARSED_ARGUMENTS}'")
    endif()
    if("${ARG_COMPONENTS}" STREQUAL "")
        message(SEND_ERROR "No COMPONENTS specified")
    endif()
    #
    # Find dependencies and other info.
    #
    set(_H_DIRS)
    set(_H_FILES)
    set(_COMPILE_OPTIONS)
    set(_INCLUDE_DIRS)
    set(_LINK_LIBRARIES)
    foreach(component IN LISTS ARG_COMPONENTS)
        get_kf5_cmake_info(${component})
        #
        # Automatic dependencies.
        #
        list(APPEND _DEPENDENCIES ${dependencies})
        if(_DEPENDENCIES)
            list(REMOVE_DUPLICATES _DEPENDENCIES)
        endif()
        #
        # Other info.
        #
        get_targets_info(${component} ${targets})
        list(APPEND _H_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        if(_H_DIRS)
            list(REMOVE_DUPLICATES _H_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
    endforeach(component)
    foreach(component IN LISTS ARG_NATIVE_COMPONENTS)
        get_kf5_native_info(${component})
        #
        # Other info.
        #
        list(APPEND _H_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        if(_H_DIRS)
            list(REMOVE_DUPLICATES _H_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
    endforeach(component)
    #
    # Find all header files.
    #
    set(tmp ${_H_DIRS})
    foreach(include IN LISTS _H_DIRS)
        file(GLOB_RECURSE tmp2 LIST_DIRECTORIES true ${include}/*)
        foreach(tmp3 IN LISTS tmp2)
            if(IS_DIRECTORY ${tmp3})
              if(NOT ${tmp3} IN_LIST tmp)
                list(APPEND tmp ${tmp3})
              endif()
            else()
              if(NOT ${tmp3} IN_LIST _H_FILES)
                list(APPEND _H_FILES ${tmp3})
              endif()
            endif()
        endforeach(tmp3)
    endforeach(include)
    set(_H_DIRS ${tmp})
    #
    # Add dependencies.
    #
    foreach(component IN LISTS _DEPENDENCIES ARG_DEPENDENCIES)
        string(FIND ${component} "KF5" found_kf5)
        string(FIND ${component} "Qt5" found_qt5)
        if(component MATCHES "^KF5")
            get_kf5_cmake_info(${component})
        elseif(component MATCHES "^Qt5")
            get_qt5_cmake_info(${component})
        endif()
        get_targets_info(${component} "${targets}")
        list(APPEND _INCLUDE_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        if(_INCLUDE_DIRS)
            list(REMOVE_DUPLICATES _INCLUDE_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
    endforeach(component)
    #
    # Find all include dirs.
    #
    set(tmp ${_INCLUDE_DIRS})
    foreach(include IN LISTS _INCLUDE_DIRS)
        file(GLOB_RECURSE tmp2 LIST_DIRECTORIES true ${include}/*)
        foreach(tmp3 IN LISTS tmp2)
            if(IS_DIRECTORY ${tmp3} AND NOT ${tmp3} IN_LIST tmp)
                list(APPEND tmp ${tmp3})
            endif()
        endforeach(tmp3)
    endforeach(include)
    set(_INCLUDE_DIRS ${tmp})
    #
    # Find the version from the first component.
    #
    list(GET ARG_COMPONENTS 0 first_component)
    include(${${first_component}_DIR}/${first_component}ConfigVersion.cmake)
    #
    # Return results.
    #
    set(version ${PACKAGE_VERSION} PARENT_SCOPE)
    set(h_dirs ${_H_DIRS} PARENT_SCOPE)
    set(h_files ${_H_FILES} PARENT_SCOPE)
    set(include_dirs ${_INCLUDE_DIRS} PARENT_SCOPE)
    set(compile_options ${_COMPILE_OPTIONS} PARENT_SCOPE)
    set(link_libraries ${_LINK_LIBRARIES} PARENT_SCOPE)
endfunction(get_binding_info_kf5)

#
# The key design choice is that building and installing Python components
# should be driven using Pythonic-facilities.
#
# Internally, those can and do use generic, non-KDE-specific CMake logic
# to drive the C++ part of the build. Generic logic should be fine since
# we are building cppyy artefacts, with definitions taken from KDE headers
# (and not bulk KDE code). Famous last words...
#
function(create_binding_targets pkg target setup_py)
    #
    # TODO: Proper Python2/3 support.
    #
    install(CODE "
execute_process(
    COMMAND pip wheel .
    COMMAND pip3 wheel .
    ERROR_VARIABLE _stderr
    RESULT_VARIABLE _rc
    OUTPUT_STRIP_TRAILING_WHITESPACE
    WORKING_DIRECTORY ${pkg})
if(NOT \"$\{_rc\}\" STREQUAL \"0\")
    message(FATAL_ERROR \"Error building wheels: ($\{_rc\}) $\{_stderr\}\")
endif()
file(GLOB wheels RELATIVE ${CMAKE_CURRENT_BINARY_DIR} ${pkg}/*.whl)
execute_process(
    COMMAND pip install --pre $\{wheels\}
    COMMAND pip3 install --pre $\{wheels\}
    ERROR_VARIABLE _stderr
    RESULT_VARIABLE _rc
    OUTPUT_STRIP_TRAILING_WHITESPACE
    WORKING_DIRECTORY ${pkg})
if(NOT \"$\{_rc\}\" STREQUAL \"0\")
    message(FATAL_ERROR \"Error during install: ($\{_rc\}) $\{_stderr\}\")
endif()")
endfunction(create_binding_targets)
