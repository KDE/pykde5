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
# Example:
#

#
# Find the targets and dependencies for a CMake KDE component.
#
#   get_kf5_cmake_info(
#       component
#       VERBOSE level)
#
# Arguments and options:
#
#   VERBOSE level       Greater than zero to turn on diagnostics
#
# Returns via PARENT_SCOPE variables:
#
#   targets             The targets of component.
#
#   dependencies        The targets of dependencies of component.
#
set(_KF5_DEPENDENCIES)
function(get_kf5_cmake_info component)
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
    find_dependency(${component})
    set(pfx "KF5")
    #
    # Loop over all cmake files.
    #
    set(real_targets)
    set(real_dependencies)
    set(file_glob  ${${component}_DIR}/*.cmake)
    file(GLOB files ${file_glob})
    foreach(f ${files})
        #
        # Targets.
        #
        set(regex " *add_library\\(([^ \\)]+).*")
        file(STRINGS ${f} matches REGEX ${regex})
        if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
            message("${f}:${component}: Target matches \"${matches}\"")
        endif()
        foreach(match ${matches})
            #
            # Extract the target.
            #
            string(REGEX REPLACE ${regex} "\\1" match "${match}")
            if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
                message("${f}:${component}: Target match \"${match}\"")
            endif()
            set(target ${match})
            if(TARGET ${target})
                list(APPEND real_targets ${target})
                if(real_targets)
                    list(REMOVE_DUPLICATES real_targets)
                endif()
            else()
                message(STATUS "Ignoring invalid target \"${match}\" for ${component} in ${f}")
            endif()
        endforeach()
        #
        # Dependencies.
        #
        set(regex " *find_dependency\\(([^ \\)]+).*")
        file(STRINGS ${f} matches REGEX ${regex})
        if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
            message("${f}:${component}: Dependency matches \"${matches}\"")
        endif()
        foreach(match ${matches})
            #
            # Extract the dependency.
            #
            string(REGEX REPLACE ${regex} "\\1" match "${match}")
            if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
                message("${f}:${component}: Dependency match \"${match}\"")
            endif()
            set(dependency ${match})
            if(NOT ${dependency} STREQUAL "")
                if(NOT dependency IN_LIST real_dependencies)
                    list(APPEND real_dependencies ${dependency})
                    #
                    # Recurse...if we have not been here before.
                    #
                    if(NOT dependency IN_LIST _KF5_DEPENDENCIES)
                        if(dependency MATCHES "^${pfx}")
                            get_kf5_cmake_info(${dependency}
                                RECURSION_LEVEL ${ARG_RECURSION_LEVEL}
                                VERBOSE ${ARG_VERBOSE})
                            list(APPEND real_dependencies ${dependencies})
                            list(REMOVE_DUPLICATES real_dependencies)
                        elseif(dependency MATCHES "^Qt5")
                            get_qt5_cmake_info(${dependency}
                                RECURSION_LEVEL ${ARG_RECURSION_LEVEL}
                                VERBOSE ${ARG_VERBOSE})
                            list(APPEND real_dependencies ${dependencies})
                            list(REMOVE_DUPLICATES real_dependencies)
                        else()
                            message(STATUS "Cannot recurse into dependency \"${dependency}\" for ${component} in ${f}")
                        endif()
                    endif()
                endif()
            else()
                message(STATUS "Ignoring invalid dependency \"${dependency}\" for ${component} in ${f}")
            endif()
        endforeach()
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
