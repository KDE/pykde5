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
# Find the targets (and not dependencies!) for a CMake Qt component.
#
#   get_qt5_cmake_info(
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
#   targets             The targets of component.
#
#   dependencies        The targets of dependencies of component.
#
function(get_qt5_cmake_info component existing_dependencies)
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
    set(pfx "Qt5")
    #
    # Targets.
    #
    string(REPLACE "${pfx}" "${pfx}::" target ${component})
    if(NOT TARGET ${target})
        message(STATUS "Ignoring invalid target \"${target}\" for ${component}")
        set(target "")
    endif()
    #
    # Loop over all cmake files.
    #
    set(real_dependencies)
    set(file_glob  ${${component}_DIR}/*.cmake)
    file(GLOB files ${file_glob})
    foreach(f ${files})
        #
        # Dependencies.
        #
        set(regex " *set\\(_${component}_MODULE_DEPENDENCIES \"([^\"]+)\".*\\) *")
        file(STRINGS ${f} matches REGEX ${regex})
        if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
            message("${f}:${component}: Dependency matches \"${matches}\"")
        endif()
        string(REGEX REPLACE ${regex} "\\1" matches "${matches}")
        set(matches ${matches})
        foreach(match ${matches})
            #
            # Extract the dependency.
            #
            string(REGEX REPLACE ${regex} "\\1" match "${match}")
            if(ARG_VERBOSE GREATER ARG_RECURSION_LEVEL)
                message("${f}:${component}: Dependency match \"${match}\"")
            endif()
            string(REGEX REPLACE ${regex} "\\1" match "${match}")
            foreach(dependency ${match})
                if(NOT ${dependency} STREQUAL "")
                    #
                    # Add the prefix.
                    #
                    set(dependency "${pfx}${dependency}")
                    #
                    # Recurse...if we have not been here before.
                    #
                    if(NOT dependency IN_LIST existing_dependencies AND NOT dependency IN_LIST real_dependencies)
                        list(APPEND real_dependencies ${dependency})
                        if(dependency MATCHES "^${pfx}")
                            get_qt5_cmake_info(${dependency} "${existing_dependencies}"
                                RECURSION_LEVEL ${ARG_RECURSION_LEVEL}
                                VERBOSE ${ARG_VERBOSE})
                            list(APPEND real_dependencies ${dependencies})
                            list(REMOVE_DUPLICATES real_dependencies)
                            list(APPEND existing_dependencies ${dependencies})
                            list(REMOVE_DUPLICATES existing_dependencies)
                        else()
                            list(APPEND existing_dependencies ${dependencies})
                            list(REMOVE_DUPLICATES existing_dependencies)
                            message(STATUS "Cannot recurse into dependency \"${dependency}\" for ${component} in ${f}")
                        endif()
                        #message(STATUS "Skip duplicate dependency \"${dependency}\"")
                    endif()
                else()
                    message(STATUS "Ignoring invalid dependencies \"${match}\" for ${component} in ${f}")
                endif()
            endforeach()
        endforeach()
    endforeach()
    set(targets "${target}" PARENT_SCOPE)
    set(dependencies "${real_dependencies}" PARENT_SCOPE)
endfunction(get_qt5_cmake_info)

#
# Find the targets (and not dependencies!) for a CMake Qt component.
#
function(get_qt5_cmake_info2 component)
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
endfunction(get_qt5_cmake_info2)
