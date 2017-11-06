cmake_minimum_required(VERSION 3.9)

project(pykde5)

find_package(ECM 5.38.0 REQUIRED)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} ${ECM_KDE_MODULE_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
include(FeatureSummary)


include(CppyyMacros)

###############################################################################
# KF5 from https://api.kde.org/frameworks
###############################################################################
#
# Tier1.
#
add_subdirectory(KF5.Attica)
add_subdirectory(KF5.BluezQt)
#BreezeIcons
#ECM
#KApiDox
add_subdirectory(KF5.Archive)
add_subdirectory(KF5.Codecs)
add_subdirectory(KF5.Config)
add_subdirectory(KF5.CoreAddons)
add_subdirectory(KF5.DBusAddons)
add_subdirectory(KF5.DNSSD)
add_subdirectory(KF5.GuiAddons)
add_subdirectory(KF5.I18n)
add_subdirectory(KF5.IdleTime)
#add_subdirectory(KF5.Kirigami2)
add_subdirectory(KF5.ItemModels)
add_subdirectory(KF5.ItemViews)
add_subdirectory(KF5.Plotting)
add_subdirectory(KF5.SyntaxHighlighting)
#KUserFeedback
add_subdirectory(KF5.Wayland)
add_subdirectory(KF5.WidgetsAddons)
add_subdirectory(KF5.WindowSystem)
add_subdirectory(KF5.ModemManagerQt)
add_subdirectory(KF5.NetworkManagerQt)
add_subdirectory(KF5.Prison)
add_subdirectory(KF5.Solid)
add_subdirectory(KF5.Sonnet)
add_subdirectory(KF5.ThreadWeaver)
#
# Tier 2.
#
add_subdirectory(KF5.Activities)
add_subdirectory(KF5.Auth)
add_subdirectory(KF5.Completion)
add_subdirectory(KF5.Crash)
add_subdirectory(KF5.DocTools)
add_subdirectory(KF5.FileMetaData)
#KImageFormats
add_subdirectory(KF5.JobWidgets)
add_subdirectory(KF5.Notifications)
add_subdirectory(KF5.Package)
add_subdirectory(KF5.Pty)
add_subdirectory(KF5.UnitConversion)
#
# Tier 3.
#
add_subdirectory(KF5.Baloo)
add_subdirectory(KF5.ActivitiesStats)
add_subdirectory(KF5.Bookmarks)
add_subdirectory(KF5.KCMUtils)
add_subdirectory(KF5.ConfigWidgets)
add_subdirectory(KF5.Declarative)
#KDED
#add_subdirectory(KF5.DesignerPlugin)
add_subdirectory(KF5.Su)
add_subdirectory(KF5.WebKit)
add_subdirectory(KF5.Emoticons)
add_subdirectory(KF5.GlobalAccel)
add_subdirectory(KF5.IconThemes)
#add_subdirectory(KF5.Init)
add_subdirectory(KF5.KIO)
add_subdirectory(KF5.NewStuff)
add_subdirectory(KF5.NotifyConfig)
add_subdirectory(KF5.Parts)
add_subdirectory(KF5.People)
add_subdirectory(KF5.Runner)
add_subdirectory(KF5.Service)
add_subdirectory(KF5.TextEditor)
add_subdirectory(KF5.TextWidgets)
add_subdirectory(KF5.Wallet)
add_subdirectory(KF5.XmlGui)
add_subdirectory(KF5.XmlRpcClient)
add_subdirectory(KF5.Plasma)
#
# Tier 4.
#
#FrameworkIntegration
#
# Porting Aids.
#
add_subdirectory(KF5.KDELibs4Support)
add_subdirectory(KF5.KHtml)
add_subdirectory(KF5.JS)
add_subdirectory(KF5.MediaPlayer)
add_subdirectory(KF5.Kross)
#
# Other.
#
add_subdirectory(KF5.Akonadi)
add_subdirectory(KF5.AlarmCalendar)
add_subdirectory(KF5.Blog)
add_subdirectory(KF5.Calendar)
#add_subdirectory(KF5.ComposerEditorNG)
add_subdirectory(KF5.Contacts)
add_subdirectory(KF5.EventViews)
#add_subdirectory(KF5.FollowupReminder)
add_subdirectory(KF5.FrameworkIntegration)
#add_subdirectory(KF5.GAPI)
add_subdirectory(KF5.Gpgmepp)
add_subdirectory(KF5.GrantleeTheme)
add_subdirectory(KF5.Gravatar)
add_subdirectory(KF5.Holidays)
add_subdirectory(KF5.IdentityManagement)
add_subdirectory(KF5.IMAP)
add_subdirectory(KF5.IncidenceEditor)
add_subdirectory(KF5.KaddressbookGrantlee)
add_subdirectory(KF5.KDcraw)
add_subdirectory(KF5.KDEGames)
add_subdirectory(KF5.KdepimDBusInterfaces)
add_subdirectory(KF5.KDGantt2)
add_subdirectory(KF5.KExiv2)
#add_subdirectory(KF5.KFace)
#add_subdirectory(KF5.KGeoMap)
add_subdirectory(KF5.Kipi)
add_subdirectory(KF5.KMahjongglib)
add_subdirectory(KF5.KontactInterface)
#add_subdirectory(KF5.Ldap)
add_subdirectory(KF5.Libkdepim)
add_subdirectory(KF5.Libkleo)
add_subdirectory(KF5.LibKSieve)
#add_subdirectory(KF5.Mail)
add_subdirectory(KF5.Mbox)
#add_subdirectory(KF5.Message)
add_subdirectory(KF5.Mime)
#add_subdirectory(KF5.PimCommon)
add_subdirectory(KF5.PimTextEdit)
add_subdirectory(KF5.Sane)
add_subdirectory(KF5.Screen)
add_subdirectory(KF5.SendLater)
add_subdirectory(KF5.Syndication)
add_subdirectory(KF5.TemplateParser)
add_subdirectory(KF5.Tnef)

feature_summary(WHAT ALL FATAL_ON_MISSING_REQUIRED_PACKAGES)
