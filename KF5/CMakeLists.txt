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
#KF5.Kirigami2
#KUserFeedback
list(APPEND components KF5.Attica KF5.BluezQt KF5.Archive KF5.Codecs KF5.Config
    KF5.CoreAddons KF5.DBusAddons KF5.DNSSD KF5.GuiAddons KF5.I18n 
    KF5.IdleTime KF5.ItemModels KF5.ItemViews KF5.Plotting 
    KF5.SyntaxHighlighting KF5.Wayland KF5.WidgetsAddons KF5.WindowSystem 
    KF5.ModemManagerQt KF5.NetworkManagerQt KF5.Prison KF5.Solid KF5.Sonnet 
    KF5.ThreadWeaver)
#
# Tier 2.
#
#KImageFormats
list(APPEND components KF5.Activities KF5.Auth KF5.Completion KF5.Crash
    KF5.DocTools KF5.FileMetaData KF5.JobWidgets KF5.Notifications
    KF5.Package KF5.Pty KF5.UnitConversion)
#
# Tier 3.
#
#KDED
#KF5.DesignerPlugin
#KF5.Init
list(APPEND components KF5.Baloo KF5.ActivitiesStats KF5.Bookmarks
    KF5.KCMUtils KF5.ConfigWidgets KF5.Declarative KF5.Su KF5.WebKit
    KF5.Emoticons KF5.GlobalAccel KF5.IconThemes KF5.KIO KF5.NewStuff
    KF5.NotifyConfig KF5.Parts KF5.People KF5.Runner KF5.Service
    KF5.TextEditor KF5.TextWidgets KF5.Wallet KF5.XmlGui KF5.XmlRpcClient
    KF5.Plasma)
#
# Tier 4.
#
list(APPEND components KF5.FrameworkIntegration)
#
# Porting Aids.
#
#KF5.KDELibs4Support
#KF5.JS
list(APPEND components KF5.KHtml KF5.MediaPlayer KF5.Kross)
#
# Other.
#
#KF5.ComposerEditorNG
#KF5.FollowupReminder
#KF5.GAPI
#KF5.KFace
#KF5.KGeoMap
#KF5.Ldap
#KF5.Mail
#KF5.Message
#KF5.PimCommon
list(APPEND components KF5.Akonadi KF5.AlarmCalendar KF5.Blog KF5.Calendar
    KF5.Contacts KF5.EventViews KF5.Gpgmepp
    KF5.GrantleeTheme KF5.Gravatar KF5.Holidays KF5.IdentityManagement KF5.IMAP
    KF5.IncidenceEditor KF5.KaddressbookGrantlee KF5.KDcraw KF5.KDEGames
    KF5.KdepimDBusInterfaces KF5.KDGantt2 KF5.KExiv2 KF5.Kipi KF5.KMahjongglib
    KF5.KontactInterface KF5.Libkdepim KF5.Libkleo KF5.LibKSieve KF5.Mbox
    KF5.Mime KF5.PimTextEdit KF5.Sane KF5.Screen KF5.SendLater KF5.Syndication
    KF5.TemplateParser KF5.Tnef)

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
