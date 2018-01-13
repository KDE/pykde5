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
# The main content is the function get_binding_info() which simplifies
# gathering the information needed by the CMake support code packaged with
# https://pypi.python.org/pypi/cppyy-backend as CPPYY_ADD_BINDINGS().
#
# Example:
#
# #
# # Get the information needed to create bindings for a set of related components.
# #
# get_binding_info(
#     COMPONENTS KF5Akonadi KF5AkonadiCalendar KF5AkonadiContact KF5AkonadiMime KF5AkonadiNotes KF5AkonadiSearch
#     NATIVE_COMPONENTS KF5AkonadiSearch
#     DEPENDENCIES KF5Konq KF5Attica)
# #
# # Customise the automatically generated information.
# #
# list(FILTER h_files EXCLUDE REGEX ".*_export.h")
# list(FILTER h_files EXCLUDE REGEX ".*_version.h")
# list(FILTER h_files EXCLUDE REGEX ".*/qtest_akonadi.h")
# #
# # Generate the bindings for KF5.Akonadi.
# #
# add_bindings("KF5.Akonadi" "Shaheed" "srhaque@theiet.org" "${version}"
#     "${include_dirs}" "${link_libraries}" "${linkdefs}" "${h_dirs}" "${h_files}")
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
find_package(Cppyy 6.10.4 REQUIRED)

include(FindPkgConfig)
include(CMakeFindDependencyMacro)
include(CppyyMacrosQt5)
include(CppyyMacrosKF5)

#
# Find the includes, libraries etc. for a pkg-config component.
#
#   get_pkgconfig_info(
#       component
#       existing_dependencies
#       VERBOSE level)
#
# Arguments and options:
#
#   VERBOSE level       Greater than zero to turn on diagnostics
#
# Returns via PARENT_SCOPE variables:
#
#   libraries           The libraries of component.
#
#   includes            The includes of component.
#
#   compile_flags       The compile flags of component.
#
function(get_pkgconfig_info component existing_dependencies)
    cmake_parse_arguments(
        ARG
        ""
        "RECURSION_LEVEL;VERBOSE"
        ""
        ${ARGN})
    if(NOT "${ARG_UNPARSED_ARGUMENTS}" STREQUAL "")
        message(SEND_ERROR "Unexpected arguments specified '${ARG_UNPARSED_ARGUMENTS}'")
    endif()
    if("${ARG_RECURSION_LEVEL}" STREQUAL "")
        set(ARG_RECURSION_LEVEL 0)
    else()
        math(EXPR ARG_RECURSION_LEVEL "${ARG_RECURSION_LEVEL}+1")
    endif()
    if("${ARG_VERBOSE}" STREQUAL "")
        set(ARG_VERBOSE 0)
    endif()
    pkg_check_modules(${component} ${component})
    set(libraries)
    set(includes ${${component}_INCLUDE_DIRS})
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
    set(removed_includes)
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
        set(tmp)
        foreach(include ${includes})
            #
            # Clean up malformed paths.
            #
            string(REGEX REPLACE "/$" "" include ${include})
            string(REGEX REPLACE "//+" "/" include ${include})
            #
            # Not sure why the headers seem to include this. Having them here
            # causes too wide a search space.
            #
            if(include STREQUAL "${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}")
                #
                # Discard.
                #
            elseif(include STREQUAL "${CMAKE_CXX_IMPLICIT_INCLUDE_DIRECTORIES}/KF5")
                list(APPEND removed_includes ${include})
                list(REMOVE_DUPLICATES removed_includes)
            elseif(include MATCHES ".*/qt5$")
                list(APPEND removed_includes ${include})
                list(REMOVE_DUPLICATES removed_includes)
            else()
                list(APPEND tmp ${include})
                list(REMOVE_DUPLICATES tmp)
            endif()
        endforeach()
        set(includes ${tmp})
    endif()
    if(DEFINED compile_flags)
        list(REMOVE_DUPLICATES compile_flags)
    endif()
    set(libraries "${libraries}" PARENT_SCOPE)
    set(includes "${includes}" PARENT_SCOPE)
    set(compile_flags "${compile_flags}" PARENT_SCOPE)
    set(removed_includes "${removed_includes}" PARENT_SCOPE)
endfunction(get_targets_info)

#
# Return the information required to create the bindings for a set of components.
#
#   get_binding_info(
#       VERBOSE level
#       COMPONENTS components
#       NATIVE_COMPONENTS components
#       DEPENDENCIES extras)
#
# Arguments and options:
#
#   VERBOSE level       Greater than zero to turn on diagnostics
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
#   PKGCONFIG_DEPENDENCIES dependency
#                       Any pkgconfig dependencies.
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
function(get_binding_info)
    cmake_parse_arguments(
        ARG
        ""
        "VERBOSE"
        "COMPONENTS;NATIVE_COMPONENTS;DEPENDENCIES;PKGCONFIG_DEPENDENCIES"
        ${ARGN})
    if(NOT "${ARG_UNPARSED_ARGUMENTS}" STREQUAL "")
        message(SEND_ERROR "Unexpected arguments specified '${ARG_UNPARSED_ARGUMENTS}'")
    endif()
    if("${ARG_COMPONENTS}" STREQUAL "")
        message(SEND_ERROR "No COMPONENTS specified")
    endif()
    #
    # Find dependencies and other info for CMake components.
    #
    set(_DEPENDENCIES)
    set(_H_DIRS)
    set(_H_FILES)
    set(_COMPILE_OPTIONS)
    set(_INCLUDE_DIRS)
    set(_LINK_LIBRARIES)
    set(_REMOVED_INCLUDES)
    foreach(component IN LISTS ARG_COMPONENTS)
        if(component MATCHES "^KF5")
            get_kf5_cmake_info(${component} "${_DEPENDENCIES}"
                VERBOSE ${ARG_VERBOSE})
        elseif(component MATCHES "^Qt5")
            get_qt5_cmake_info(${component} "${_DEPENDENCIES}"
                VERBOSE ${ARG_VERBOSE})
        endif()
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
        if(ARG_VERBOSE)
            message("COMPONENTS ${component}:
    targets=${targets}
    dependencies=${dependencies}
    include=${includes}
    libraries=${libraries}
    compile_flags=${compile_flags}
    removed_includes=${removed_includes}
")
        endif()
        list(APPEND _H_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        list(APPEND _REMOVED_INCLUDES "${removed_includes}")
        if(_H_DIRS)
            list(REMOVE_DUPLICATES _H_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
        if(_REMOVED_INCLUDES)
            list(REMOVE_DUPLICATES _REMOVED_INCLUDES)
        endif()
    endforeach(component)
    #
    # Find other info for non-CMake components.
    #
    foreach(component IN LISTS ARG_NATIVE_COMPONENTS)
        get_kf5_native_info(${component})
        if(ARG_VERBOSE)
            message("NATIVE_COMPONENTs ${component}:
    targets=${targets}
    dependencies=${dependencies}
    include=${includes}
    libraries=${libraries}
    compile_flags=${compile_flags}
")
        endif()
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
        if(component MATCHES "^KF5")
            get_kf5_cmake_info(${component} "${_DEPENDENCIES}"
                VERBOSE ${ARG_VERBOSE})
        elseif(component MATCHES "^Qt5")
            get_qt5_cmake_info(${component} "${_DEPENDENCIES}"
                VERBOSE ${ARG_VERBOSE})
        endif()
        get_targets_info(${component} "${targets}")
        if(ARG_VERBOSE)
            message("DEPENDENCIES ${component}:
    targets=${targets}
    dependencies=${dependencies}
    include=${includes}
    libraries=${libraries}
    compile_flags=${compile_flags}
    removed_includes=${removed_includes}
")
        endif()
        list(APPEND _INCLUDE_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        list(APPEND _REMOVED_INCLUDES "${removed_includes}")
        if(_INCLUDE_DIRS)
            list(REMOVE_DUPLICATES _INCLUDE_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
        if(_REMOVED_INCLUDES)
            list(REMOVE_DUPLICATES _REMOVED_INCLUDES)
        endif()
    endforeach(component)
    foreach(component IN LISTS ARG_PKGCONFIG_DEPENDENCIES)
        get_pkgconfig_info(${component} "${_DEPENDENCIES}"
            VERBOSE ${ARG_VERBOSE})
        if(ARG_VERBOSE)
            message("DEPENDENCIES ${component}:
    targets=${targets}
    dependencies=${dependencies}
    include=${includes}
    libraries=${libraries}
    compile_flags=${compile_flags}
    removed_includes=${removed_includes}
")
        endif()
        list(APPEND _INCLUDE_DIRS ${includes})
        list(APPEND _LINK_LIBRARIES ${libraries})
        list(APPEND _COMPILE_OPTIONS "${compile_flags}")
        list(APPEND _REMOVED_INCLUDES "${removed_includes}")
        if(_INCLUDE_DIRS)
            list(REMOVE_DUPLICATES _INCLUDE_DIRS)
        endif()
        if(_LINK_LIBRARIES)
            list(REMOVE_DUPLICATES _LINK_LIBRARIES)
        endif()
        if(_COMPILE_OPTIONS)
            list(REMOVE_DUPLICATES _COMPILE_OPTIONS)
        endif()
        if(_REMOVED_INCLUDES)
            list(REMOVE_DUPLICATES _REMOVED_INCLUDES)
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
    # Restore any removed items. By putting them last, we reduce the chance
    # that a legacy header gets picked up ahead of specific dependencies.
    #
    list(APPEND _INCLUDE_DIRS ${_REMOVED_INCLUDES})
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
endfunction(get_binding_info)

#
# The key design choice is that building and installing Python components
# should be driven using Pythonic-facilities.
#
# Internally, those can and do use generic, non-KDE-specific CMake logic
# to drive the C++ part of the build. Generic logic should be fine since
# we are building cppyy artefacts, with definitions taken from KDE headers
# (and not bulk KDE code). Famous last words...
#
function(add_bindings pkg author author_email version include_dirs link_libraries linkdefs h_dirs h_files)
    string(REPLACE "\\" "\\\\\\" linkdefs "${linkdefs}")
    file(GLOB extra_codes INCLUDE_DIRECTORIES false ${CMAKE_CURRENT_LIST_DIR}/extra_*.cpp)
    file(GLOB extra_headers INCLUDE_DIRECTORIES false ${CMAKE_CURRENT_LIST_DIR}/extra_*.h)
    file(GLOB extra_pythons INCLUDE_DIRECTORIES false RELATIVE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_LIST_DIR}/extra_*.py)
    cppyy_add_bindings(
        "${pkg}" "${version}" "${author}" "${author_email}"
        LANGUAGE_STANDARD "14"
        GENERATE_OPTIONS "-fvisibility=hidden;-D__PIC__;-Wno-macro-redefined"
        COMPILE_OPTIONS "-Wno-deprecated-declarations;-Wno-overloaded-virtual;-fstack-protector-strong"
        EXTRA_CODES "${extra_codes}"
        EXTRA_HEADERS "${extra_headers}"
        EXTRA_PYTHONS "${extra_pythons}"
        INCLUDE_DIRS "${include_dirs}"
        LINK_LIBRARIES "${link_libraries}"
        LINKDEFS "${linkdefs}"
        H_DIRS "${h_dirs}"
        H_FILES "${h_files}")
    #
    # Create the wheel using pip2/pip3 support as a post-build step.
    #
    foreach(pip IN LISTS PIP_EXECUTABLES)
        add_custom_command(
            TARGET ${target} POST_BUILD
            COMMAND ${pip} wheel .
            WORKING_DIRECTORY ${pkg_dir}
            COMMENT "Create universal wheel")
        #
        # Since the wheel is universal, we only need create it once.
        #
        break()
    endforeach()
    #
    # The install consists of pip2/pip3 installs.
    #
    string(REPLACE "." "/" pkg_dir ${pkg})
    set(pkg_dir ${CMAKE_CURRENT_BINARY_DIR})
    install(CODE "
set(pkg_dir ${pkg_dir})
set(PIP_EXECUTABLES ${PIP_EXECUTABLES})
#
# What are the wheel names? We don't need to know.
#
foreach(pip IN LISTS PIP_EXECUTABLES)
    message(\"$\{pip\} install wheel\")
    execute_process(
        COMMAND $\{pip\} install --upgrade --force-reinstall --pre .
        ERROR_VARIABLE _stderr
        RESULT_VARIABLE _rc
        OUTPUT_STRIP_TRAILING_WHITESPACE
        WORKING_DIRECTORY $\{pkg_dir\})
    if(NOT \"$\{_rc\}\" STREQUAL \"0\")
        message(FATAL_ERROR \"Error during install: ($\{_rc\}) $\{_stderr\}\")
    endif()
endforeach()")
endfunction(add_bindings)
