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
# Cppyy-based bindings for KF5.
#
cmake_minimum_required(VERSION 3.9)

project(KF5)

find_package(ECM 5.38.0 REQUIRED)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/../cmake)
include(FeatureSummary)


include(CppyyMacros)

###############################################################################
# KF5 from https://api.kde.org/frameworks
###############################################################################
#
# Tier1.
#
#BreezeIcons
#ECM
#KApiDox
#Kirigami2
#KUserFeedback
list(APPEND components Attica BluezQt Archive Codecs Config
    CoreAddons DBusAddons DNSSD GuiAddons I18n
    IdleTime ItemModels ItemViews Plotting
    SyntaxHighlighting Wayland WidgetsAddons WindowSystem
    ModemManagerQt NetworkManagerQt Prison Solid Sonnet
    ThreadWeaver)
#
# Tier 2.
#
#KImageFormats
list(APPEND components Activities Auth Completion Crash
    DocTools FileMetaData JobWidgets Notifications
    Package Pty UnitConversion)
#
# Tier 3.
#
#KDED
#DesignerPlugin
#Init
list(APPEND components Baloo ActivitiesStats Bookmarks
    KCMUtils ConfigWidgets Declarative Su WebKit
    Emoticons GlobalAccel IconThemes KIO NewStuff
    NotifyConfig Parts People Runner Service
    TextEditor TextWidgets Wallet XmlGui XmlRpcClient
    Plasma)
#
# Tier 4.
#
list(APPEND components FrameworkIntegration)
#
# Porting Aids.
#
#KDELibs4Support
#JS
list(APPEND components KHtml MediaPlayer Kross)
#
# Other.
#
#ComposerEditorNG
#FollowupReminder
#GAPI
#KFace
#KGeoMap
#Ldap
#Mail
#Message
#PimCommon
list(APPEND components Akonadi AlarmCalendar Blog Calendar
    Contacts EventViews Gpgmepp
    GrantleeTheme Gravatar Holidays IdentityManagement IMAP
    IncidenceEditor KaddressbookGrantlee KDcraw KDEGames
    KdepimDBusInterfaces KDGantt2 KExiv2 Kipi KMahjongglib
    KontactInterface Libkdepim Libkleo LibKSieve Mbox
    Mime PimTextEdit Sane Screen SendLater Syndication
    TemplateParser Tnef)

foreach(component IN LISTS components)
    add_subdirectory(${component})
endforeach()
feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)

###############################################################################
# Testing.
###############################################################################
enable_testing()
foreach(component IN LISTS components)
    add_test(NAME KF5${component}Cppyy
        COMMAND pytest test.py
        WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${component}")
endforeach()
