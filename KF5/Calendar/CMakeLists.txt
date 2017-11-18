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

set(_pkg "KF5.Calendar")
project(${_pkg})

#
# Get the information needed to create bindings for a set of related components.
# Increase the VERBOSE setting for diagnostics.
#
get_binding_info(
    VERBOSE 0
    COMPONENTS KF5CalendarCore KF5CalendarSupport KF5CalendarUtils
    PKGCONFIG_DEPENDENCIES libical)
#
# Customise the automatically generated information.
#
list(FILTER h_files EXCLUDE REGEX ".*/libical/.*.h")
set(missing_cxx_libs)
foreach(lib IN LISTS link_libraries)
    if(lib MATCHES ".*/${CMAKE_SHARED_LIBRARY_PREFIX}(ical|icalss)${CMAKE_SHARED_LIBRARY_SUFFIX}")
        string(REGEX REPLACE "(.*/${CMAKE_SHARED_LIBRARY_PREFIX})(ical|icalss)(${CMAKE_SHARED_LIBRARY_SUFFIX})" "\\1\\2_cxx\\3" lib ${lib})
        list(APPEND missing_cxx_libs ${lib})
    endif()
endforeach()
list(APPEND link_libraries ${missing_cxx_libs})
set(linkdefs "")
#
# Generate the bindings.
#
add_bindings(${_pkg} "Shaheed Haque" "srhaque@theiet.org" "${version}" "${include_dirs}" "${link_libraries}" "${linkdefs}" "${h_dirs}" "${h_files}")
unset(_pkg)
