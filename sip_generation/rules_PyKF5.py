#
# Copyright 2016 by Shaheed Haque (srhaque@theiet.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA.
#
"""
SIP binding customisation for PyKF5. This modules describes:

    * The SIP file generator rules.

    * The SIP compilation rules.

"""

import rules_engine

from clang.cindex import AccessSpecifier


def _container_discard(container, sip, matcher):
    sip["name"] = ""


def _function_discard(container, function, sip, matcher):
    sip["name"] = ""


def _function_discard_class(container, function, sip, matcher):
    sip["fn_result"] = sip["fn_result"].replace("class ", "")


def _function_discard_impl(container, function, sip, matcher):
    if function.extent.start.column == 1:
        sip["name"] = ""


def _parameter_out_kdatetime_negzero(container, function, parameter, sip, matcher):
    sip["annotations"].add("Out")


def _parameter_rewrite_without_colons(container, function, parameter, sip, matcher):
    sip["decl"] = sip["decl"].replace("::", "")


def _parameter_transfer_to_parent(container, function, parameter, sip, matcher):
    if function.is_static_method():
        sip["annotations"].add("Transfer")
    else:
        sip["annotations"].add("TransferThis")


def _parameter_set_max_int(container, function, parameter, sip, matcher):
    sip["init"] = "(uint)-1"


def _parameter_strip_class_enum(container, function, parameter, sip, matcher):
    sip["decl"] = sip["decl"].replace("class ", "").replace("enum ", "")


def _typedef_discard(container, typedef, sip, matcher):
    sip["name"] = ""


def _typedef_rewrite_as_int(container, typedef, sip, matcher):
    sip["decl"] = "int"


def _typedef_rewrite_without_colons(container, typedef, sip, matcher):
    sip["decl"] = sip["decl"].strip(":")


def _typedef_rewrite_enums(container, typedef, sip, matcher):
    sip["decl"] = sip["args"][0]


def _variable_discard(container, variable, sip, matcher):
    sip["name"] = ""


def _variable_discard_protected(container, variable, sip, matcher):
    if variable.access_specifier == AccessSpecifier.PROTECTED:
        sip["name"] = ""


def container_rules():

    return [
        #
        # SIP does not seem to be able to handle these.
        #
        [".*", "(QMetaTypeId|QTypeInfo)<.*>", ".*", ".*", ".*", _container_discard],
        #
        # SIP does not seem to be able to handle empty containers.
        #
        ["Akonadi::AkonadiCore", "Monitor|Protocol", ".*", ".*", ".*", _container_discard],
        ["KParts::ScriptableExtension", "Null|Undefined", ".*", ".*", ".*", _container_discard],
        #
        # SIP does not seem to be able to handle templated containers.
        #
        [".*", ".*<.*", ".*", ".*", ".*", _container_discard],
        ["KPluginFactory", "InheritanceChecker<impl>", ".*", ".*", ".*", _container_discard],
        #
        # This is pretty much a disaster area. TODO: can we rescue some parts?
        #
        [".*", "KConfigCompilerSignallingItem", ".*", ".*", ".*", _container_discard],
        ["ConversionCheck", ".*", ".*", ".*", ".*", _container_discard],
    ]


def function_rules():

    return [
        #
        # Discard functions emitted by QOBJECT.
        #
        [".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", ".*", ".*", _function_discard],
        #
        # SIP does not support operator=.
        #
        [".*", "operator=", ".*", ".*", ".*", _function_discard],
        #
        # Protected functions which require access to private stuff.
        #
        ["KJob", ".*", ".*", ".*", ".*KJob::QPrivateSignal.*", _function_discard],
        #
        # TODO: Temporarily remove any functions which require templates. SIP seems to support, e.g. QPairs,
        # but we have not made them work yet.
        #
        [".*", ".*", ".+", ".*", ".*", _function_discard],
        [".*", ".*", ".*", ".*", ".*<.*>.*", _function_discard],
        [".*", ".*", ".*", ".*<.*>.*", ".*", _function_discard],
        [".*", ".*<.*>.*", ".*", ".*", ".*", _function_discard],
        #
        # Strip protected functions which require private stuff to work.
        #
        ["KPluginFactory", "KPluginFactory", ".*", ".*", ".*KPluginFactoryPrivate", _function_discard],
        ["KJob", "KJob", ".*", ".*", "KJobPrivate.*", _function_discard],
        ["KCompositeJob", "KCompositeJob", ".*", ".*", "KCompositeJobPrivate.*", _function_discard],
        #
        # This class has inline implementations in the header file.
        #
        ["KIconEngine|KIconLoader::Group|KPluginName", ".*", ".*", ".*", ".*", _function_discard_impl],
        ["kiconloader.h", "operator\+\+", ".*", ".*", ".*", _function_discard_impl],
        #
        # kshell.h, kconfigbase.sip have inline operators.
        #
        [".*", "operator\|", ".*", ".*", "", _function_discard],
        #
        # kuser.h has inline operators.
        #
        [".*", "operator!=", ".*", ".*", "const KUser(Group){0,1} &other", _function_discard],
        ["KFileItem", "operator QVariant", ".*", ".*", ".*", _function_discard],
        ["KService", "operator KPluginName", ".*", ".*", ".*", _function_discard],
        #
        # SIP thinks there are duplicate signatures.
        #
        ["KMacroExpanderBase", "expandMacrosShellQuote", ".*", ".*", "QString &str", _function_discard],
        ["KMultiTabBar", "button|tab", ".*", ".*", ".*", _function_discard_class],
    ]


def parameter_rules():

    return [
        #
        # Annotate with Transfer or TransferThis when we see a parent object.
        #
        [".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", _parameter_transfer_to_parent],
        ["KDateTime", "fromString", "negZero", ".*", ".*", _parameter_out_kdatetime_negzero],
        ["KPty", "tcGetAttr|tcSetAttr", "ttmode", ".*", ".*", _parameter_rewrite_without_colons],
        ["KUser|KUserGroup", ".*", "maxCount", ".*", ".*", _parameter_set_max_int],
        #
        # TODO: Temporarily trim any parameters which start "enum".
        #
        ["KAboutData", ".*", "licenseType", ".*", ".*", _parameter_strip_class_enum],
        ["KMultiTabBarButton", ".*Event", ".*", ".*", ".*", _parameter_strip_class_enum],
        ["KRockerGesture", "KRockerGesture", ".*", ".*", ".*", _parameter_strip_class_enum],
    ]


def typedef_rules():

    return [
        #
        # Rewrite QFlags<> templates as int.
        #
        [".*", ".*", ".*", "QFlags<.*>", _typedef_rewrite_as_int],
        #
        # Rewrite uid_t, gid_t as int.
        #
        [".*", ".*", ".*", "uid_t|gid_t", _typedef_rewrite_as_int],
        #
        # Rewrite without leading "::".
        #
        ["org::kde", "KDirNotify", "", ".*", _typedef_rewrite_without_colons],
        ["org::kde", "KSSLDInterface", "", ".*", _typedef_rewrite_without_colons],
        #
        #
        #
        ["KProtocolInfo", "FileNameUsedForCopying", ".*", ".*", _typedef_rewrite_enums],
        ["KSycoca", "DatabaseType", ".*", ".*", _typedef_rewrite_enums],
        #
        # There are two version of KSharedConfigPtr in ksharedconfig.h and kconfiggroup.h.
        #
        [".*", "KSharedConfigPtr", ".*", "QExplicitlySharedDataPointer<KSharedConfig>", _typedef_discard],
        #
        # There are two version of Display in kstartupinfo.h and kxmessages.h.
        #
        ["kstartupinfo.h|kxmessages.h", "Display", ".*", ".*", _typedef_discard],
        ["kmimetypetrader.h", "KServiceOfferList", ".*", ".*", _typedef_discard],
    ]


def variable_rules():

    return [
        #
        # Discard variable emitted by QOBJECT.
        #
        [".*", "staticMetaObject", ".*", _variable_discard],
        #
        # Discard "private" variables (check they are protected!).
        #
        [".*", "d_ptr", ".*", _variable_discard_protected],
        #
        # Discard variable emitted by QOBJECT.
        #
        [".*", "d", ".*Private.*", _variable_discard],
    ]


class RuleSet(rules_engine.RuleSet):
    """
    SIP file generator rules. This is a set of (short, non-public) functions
    and regular expression-based matching rules.
    """
    def __init__(self, includes, sips):
        self._includes = super(RuleSet, self)._check_directory_list(includes)
        self._sips = super(RuleSet, self)._check_directory_list(sips)
        self._container_db = rules_engine.ContainerRuleDb(container_rules)
        self._fn_db = rules_engine.FunctionRuleDb(function_rules)
        self._param_db = rules_engine.ParameterRuleDb(parameter_rules)
        self._typedef_db = rules_engine.TypedefRuleDb(typedef_rules)
        self._var_db = rules_engine.VariableRuleDb(variable_rules)

    def container_rules(self):
        return self._container_db

    def function_rules(self):
        return self._fn_db

    def param_rules(self):
        return self._param_db

    def typedef_rules(self):
        return self._typedef_db

    def var_rules(self):
        return self._var_db

    def includes(self):
        return self._includes

    def sips(self):
        return self._sips

    def project_name(self):
        """Project name"""
        return "PyKF5"

    def modules(self):
        """
        The SIP modules we want to actually generate compiled bindings from.
        """
        return [
            "AkonadiAgentBase/AkonadiAgentBasemod.sip",
            "akonadi/akonadimod.sip",
            "Akonadi/Calendar/Calendarmod.sip",
            "Akonadi/Contact/Contactmod.sip",
            "AkonadiCore/AkonadiCoremod.sip",
            "Akonadi/KMime/KMimemod.sip",
            "Akonadi/Notes/Notesmod.sip",
            "akonadi/private/privatemod.sip",
            "AkonadiSearch/PIM/PIMmod.sip",
            "Akonadi/SocialUtils/SocialUtilsmod.sip",
            "AkonadiWidgets/AkonadiWidgetsmod.sip",
            "AkonadiXml/AkonadiXmlmod.sip",
            "Attica/Attica/Atticamod.sip",
            "BalooWidgets/Baloo/Baloomod.sip",
            "BluezQt/BluezQt/BluezQtmod.sip",
            "gpgme++/gpgme++mod.sip",
            "gpgme++/interfaces/interfacesmod.sip",
            "KActivities/KActivities/KActivitiesmod.sip",
            "KAlarmCal/KAlarmCal/KAlarmCalmod.sip",
            "KArchive/KArchivemod.sip",
            "KAuth/KAuthmod.sip",
            "KBlog/KBlog/KBlogmod.sip",
            "KBookmarks/KBookmarksmod.sip",
            "KCalCore/KCalCore/KCalCoremod.sip",
            "KCalUtils/KCalUtils/KCalUtilsmod.sip",
            "KCMUtils/KCMUtilsmod.sip",
            "KCMUtils/ksettings/ksettingsmod.sip",
            "KCodecs/KCodecsmod.sip",
            "KCompletion/KCompletionmod.sip",
            "KConfigCore/KConfigCoremod.sip",
            "KConfigGui/KConfigGuimod.sip",
            "KConfigWidgets/KConfigWidgetsmod.sip",
            "KContacts/KContacts/KContactsmod.sip",
            "KCoreAddons/KCoreAddonsmod.sip",
            "KCrash/KCrashmod.sip",
            "KDBusAddons/KDBusAddonsmod.sip",
            "KDeclarative/KDeclarative/KDeclarativemod.sip",
            "KDeclarative/KQuickAddons/KQuickAddonsmod.sip",
            "KDeclarative/QuickAddons/QuickAddonsmod.sip",
            "KDESu/KDESu/KDESumod.sip",
            "KDEWebKit/KDEWebKitmod.sip",
            "KDNSSD/DNSSD/DNSSDmod.sip",
            "KEmoticons/KEmoticonsmod.sip",
            "KF5KDEGames/highscore/highscoremod.sip",
            "KF5KDEGames/KDE/KDEmod.sip",
            "KF5KDEGames/KF5KDEGamesmod.sip",
            "KF5KDEGames/libkdegamesprivate/kgame/kgamemod.sip",
            "KF5KDEGames/libkdegamesprivate/libkdegamesprivatemod.sip",
            "KF5KMahjongg/KF5KMahjonggmod.sip",
            "KFileMetaData/KFileMetaData/KFileMetaDatamod.sip",
            "KGAPI/KGAPI/Blogger/Bloggermod.sip",
            "KGAPI/KGAPI/Calendar/Calendarmod.sip",
            "KGAPI/KGAPI/Contacts/Contactsmod.sip",
            "KGAPI/KGAPI/Drive/Drivemod.sip",
            "KGAPI/KGAPI/KGAPImod.sip",
            "KGAPI/KGAPI/Latitude/Latitudemod.sip",
            "KGAPI/KGAPI/Maps/Mapsmod.sip",
            "KGAPI/KGAPI/Tasks/Tasksmod.sip",
            "KGlobalAccel/KGlobalAccelmod.sip",
            "KGlobalAccel/private/privatemod.sip",
            "KGuiAddons/KGuiAddonsmod.sip",
            "KHolidays/KHolidays/KHolidaysmod.sip",
            "KHtml/dom/dommod.sip",
            "KHtml/KHtmlmod.sip",
            "KI18n/KI18nmod.sip",
            "KIconThemes/KIconThemesmod.sip",
            "KIdentityManagement/KIdentityManagement/KIdentityManagementmod.sip",
            "KIdleTime/KIdleTimemod.sip",
            "KIdleTime/private/privatemod.sip",
            "KIMAP/KIMAP/KIMAPmod.sip",
            "kimaptest/kimaptestmod.sip",
            "KIOCore/KIOCoremod.sip",
            "KIOCore/KIO/KIOmod.sip",
            "KIOFileWidgets/KIOFileWidgetsmod.sip",
            "kio/kiomod.sip",
            "KIOWidgets/KIO/KIOmod.sip",
            "KIOWidgets/KIOWidgetsmod.sip",
            "KItemModels/KItemModelsmod.sip",
            "KItemViews/KItemViewsmod.sip",
            "KJobWidgets/KJobWidgetsmod.sip",
            "kjs/bytecode/bytecodemod.sip",
            "KJsEmbed/KJsEmbed/KJsEmbedmod.sip",
            "kjs/kjsmod.sip",
            "KLDAP/KLDAP/KLDAPmod.sip",
            "KMbox/KMbox/KMboxmod.sip",
            "KMediaPlayer/KMediaPlayer/KMediaPlayermod.sip",
            "KMime/KMime/KMimemod.sip",
            "KNewStuff3/KNS3/KNS3mod.sip",
            "KNotifications/KNotificationsmod.sip",
            "KNotifyConfig/KNotifyConfigmod.sip",
            "KontactInterface/KontactInterface/KontactInterfacemod.sip",
            "KPackage/KPackage/KPackagemod.sip",
            "KParts/KParts/KPartsmod.sip",
            "KParts/KPartsmod.sip",
            "KPeople/KPeopleBackend/KPeopleBackendmod.sip",
            "KPeople/KPeople/KPeoplemod.sip",
            "KPeople/kpeople/widgets/widgetsmod.sip",
            "KPIMTextEdit/KPIMTextEdit/KPIMTextEditmod.sip",
            "KPlotting/KPlottingmod.sip",
            "KPty/KPtymod.sip",
            "KrossCore/Kross/Core/Coremod.sip",
            "KrossUi/Kross/Ui/Uimod.sip",
            "KRunner/KRunner/KRunnermod.sip",
            "KScreen/KScreen/KScreenmod.sip",
            "KService/KServicemod.sip",
            "KStyle/KStylemod.sip",
            "KTextEditor/KTextEditor/KTextEditormod.sip",
            "KTextWidgets/KTextWidgetsmod.sip",
            "KTNEF/KTNEF/KTNEFmod.sip",
            "KUnitConversion/KUnitConversion/KUnitConversionmod.sip",
            "KWallet/KWalletmod.sip",
            "KWidgetsAddons/KWidgetsAddonsmod.sip",
            "KWindowSystem/KWindowSystemmod.sip",
            "KWindowSystem/private/privatemod.sip",
            "KXmlGui/KXmlGuimod.sip",
            "KXmlRpcClient/KXmlRpcClient/KXmlRpcClientmod.sip",
            "MailTransport/MailTransport/MailTransportmod.sip",
            "mod.sip",
            "NetworkManagerQt/NetworkManagerQt/NetworkManagerQtmod.sip",
            "Plasma/Plasmamod.sip",
            "plasma/scripting/scriptingmod.sip",
            "PRISON/prison/prisonmod.sip",
            "purpose/purposemod.sip",
            "purpose/Purpose/Purposemod.sip",
            "purposewidgets/PurposeWidgets/PurposeWidgetsmod.sip",
            "qgpgme/qgpgmemod.sip",
            "Solid/Solid/Solidmod.sip",
            "SonnetCore/Sonnet/Sonnetmod.sip",
            "SonnetUi/Sonnet/Sonnetmod.sip",
            "Syndication/Syndication/Atom/Atommod.sip",
            "Syndication/Syndication/Rdf/Rdfmod.sip",
            "Syndication/Syndication/Rss2/Rss2mod.sip",
            "Syndication/Syndication/Syndicationmod.sip",
            "ThreadWeaver/ThreadWeaver/ThreadWeavermod.sip",
            "wtf/wtfmod.sip",
            "XsltKde/XsltKdemod.sip",
        ]
