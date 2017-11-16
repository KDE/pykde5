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
# Cppyy-based bindings for Qt5.
#
cmake_minimum_required(VERSION 3.9)

project(qt5)

find_package(ECM 5.38.0 REQUIRED)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/../cmake)
include(FeatureSummary)


include(CppyyMacros)

###############################################################################
# Qt5 from http://doc.qt.io/qt-5/qtmodules.html
###############################################################################
#
# Qt Essentials.
#
list(APPEND components Qt5.Core Qt5.Gui Qt5.Network Qt5.Qml Qt5.Quick Qt5.Sql
    Qt5.Test Qt5.Widgets)
#
# Qt Addons.
#
list(APPEND components Qt5.Concurrent Qt5.DBus Qt5.OpenGL Qt5.Positioning
    Qt5.PrintSupport Qt5.Script Qt5.Sensors Qt5.SerialPort Qt5.Svg
    Qt5.WebChannel Qt5.WebEngine Qt5.WebSockets Qt5.WebView Qt5.X11Extras
    Qt5.Xml Qt5.WaylandCompositor Qt5.Charts)
#
# Other stuff.
#
#Qt5.WebKit
list(APPEND components Qt5.TextToSpeech)

foreach(component IN LISTS components)
    add_subdirectory(${component})
endforeach()
feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)

###############################################################################
# Testing.
###############################################################################
enable_testing()
foreach(component IN LISTS components)
    string(REPLACE "." "/" subdir ${component})
    add_test(NAME ${component}
        COMMAND pytest test.py
        WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${component}")
endforeach()
