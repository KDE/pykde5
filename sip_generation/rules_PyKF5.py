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
"""SIP file generator rules for PyKF5."""


from clang.cindex import AccessSpecifier


def container_discard(container, sip, matcher):
    sip["name"] = ""


def function_discard(container, function, sip, matcher):
    sip["name"] = ""


def function_discard_class(container, function, sip, matcher):
    sip["fn_result"] = sip["fn_result"].replace("class ", "")


def function_discard_impl(container, function, sip, matcher):
    if function.extent.start.column == 1:
        sip["name"] = ""


def parameter_out_kdatetime_negzero(container, function, parameter, sip, matcher):
    sip["annotations"].add("Out")


def parameter_rewrite_without_colons(container, function, parameter, sip, matcher):
    sip["decl"] = sip["decl"].replace("::", "")


def parameter_transfer_to_parent(container, function, parameter, sip, matcher):
    if function.is_static_method():
        sip["annotations"].add("Transfer")
    else:
        sip["annotations"].add("TransferThis")


def parameter_set_max_int(container, function, parameter, sip, matcher):
    sip["init"] = "(uint)-1"


def parameter_strip_class_enum(container, function, parameter, sip, matcher):
    sip["decl"] = sip["decl"].replace("class ", "").replace("enum ", "")


def typedef_discard(container, typedef, sip, matcher):
    sip["name"] = ""


def typedef_rewrite_as_int(container, typedef, sip, matcher):
    sip["decl"] = "int"


def typedef_rewrite_without_colons(container, typedef, sip, matcher):
    sip["decl"] = sip["decl"].strip(":")


def typedef_rewrite_enums(container, typedef, sip, matcher):
    sip["decl"] = sip["args"][0]


def variable_discard(container, variable, sip, matcher):
    sip["name"] = ""


def variable_discard_protected(container, variable, sip, matcher):
    if variable.access_specifier == AccessSpecifier.PROTECTED:
        sip["name"] = ""


def container_rules():

    return [
        #
        # SIP does not seem to be able to handle these.
        #
        [".*", "(QMetaTypeId|QTypeInfo)<.*>", ".*", ".*", ".*", container_discard],
        #
        # SIP does not seem to be able to handle empty containers.
        #
        ["Akonadi::AkonadiCore", "Monitor|Protocol", ".*", ".*", ".*", container_discard],
        ["KParts::ScriptableExtension", "Null|Undefined", ".*", ".*", ".*", container_discard],
        #
        # SIP does not seem to be able to handle templated containers.
        #
        [".*", ".*<.*", ".*", ".*", ".*", container_discard],
        ["KPluginFactory", "InheritanceChecker<impl>", ".*", ".*", ".*", container_discard],
        #
        # This is pretty much a disaster area. TODO: can we rescue some parts?
        #
        [".*", "KConfigCompilerSignallingItem", ".*", ".*", ".*", container_discard],
        ["ConversionCheck", ".*", ".*", ".*", ".*", container_discard],
    ]


def function_rules():

    return [
        #
        # Discard functions emitted by QOBJECT.
        #
        [".*", "metaObject|qt_metacast|tr|trUtf8|qt_metacall|qt_check_for_QOBJECT_macro", ".*", ".*", ".*", function_discard],
        #
        # SIP does not support operator=.
        #
        [".*", "operator=", ".*", ".*", ".*", function_discard],
        #
        # Protected functions which require access to private stuff.
        #
        ["KJob", ".*", ".*", ".*", ".*KJob::QPrivateSignal.*", function_discard],
        #
        # TODO: Temporarily remove any functions which require templates. SIP seems to support, e.g. QPairs,
        # but we have not made them work yet.
        #
        [".*", ".*", ".+", ".*", ".*", function_discard],
        [".*", ".*", ".*", ".*", ".*<.*>.*", function_discard],
        [".*", ".*", ".*", ".*<.*>.*", ".*", function_discard],
        [".*", ".*<.*>.*", ".*", ".*", ".*", function_discard],
        #
        # Strip protected functions which require private stuff to work.
        #
        ["KPluginFactory", "KPluginFactory", ".*", ".*", ".*KPluginFactoryPrivate", function_discard],
        ["KJob", "KJob", ".*", ".*", "KJobPrivate.*", function_discard],
        ["KCompositeJob", "KCompositeJob", ".*", ".*", "KCompositeJobPrivate.*", function_discard],
        #
        # This class has inline implementations in the header file.
        #
        ["KIconEngine|KIconLoader::Group|KPluginName", ".*", ".*", ".*", ".*", function_discard_impl],
        ["kiconloader.h", "operator\+\+", ".*", ".*", ".*", function_discard_impl],
        #
        # kshell.h, kconfigbase.sip have inline operators.
        #
        [".*", "operator\|", ".*", ".*", "", function_discard],
        #
        # kuser.h has inline operators.
        #
        [".*", "operator!=", ".*", ".*", "const KUser(Group){0,1} &other", function_discard],
        ["KFileItem", "operator QVariant", ".*", ".*", ".*", function_discard],
        ["KService", "operator KPluginName", ".*", ".*", ".*", function_discard],
        #
        # SIP thinks there are duplicate signatures.
        #
        ["KMacroExpanderBase", "expandMacrosShellQuote", ".*", ".*", "QString &str", function_discard],
        ["KMultiTabBar", "button|tab", ".*", ".*", ".*", function_discard_class],
    ]


def parameter_rules():

    return [
        #
        # Annotate with Transfer or TransferThis when we see a parent object.
        #
        [".*", ".*", ".*", r"[KQ][A-Za-z_0-9]+\W*\*\W*parent", ".*", parameter_transfer_to_parent],
        ["KDateTime", "fromString", "negZero", ".*", ".*", parameter_out_kdatetime_negzero],
        ["KPty", "tcGetAttr|tcSetAttr", "ttmode", ".*", ".*", parameter_rewrite_without_colons],
        ["KUser|KUserGroup", ".*", "maxCount", ".*", ".*", parameter_set_max_int],
        #
        # TODO: Temporarily trim any parameters which start "enum".
        #
        ["KAboutData", ".*", "licenseType", ".*", ".*", parameter_strip_class_enum],
        ["KMultiTabBarButton", ".*Event", ".*", ".*", ".*", parameter_strip_class_enum],
        ["KRockerGesture", "KRockerGesture", ".*", ".*", ".*", parameter_strip_class_enum],
    ]


def typedef_rules():

    return [
        #
        # Rewrite QFlags<> templates as int.
        #
        [".*", ".*", ".*", "QFlags<.*>", typedef_rewrite_as_int],
        #
        # Rewrite uid_t, gid_t as int.
        #
        [".*", ".*", ".*", "uid_t|gid_t", typedef_rewrite_as_int],
        #
        # Rewrite without leading "::".
        #
        ["org::kde", "KDirNotify", "", ".*", typedef_rewrite_without_colons],
        ["org::kde", "KSSLDInterface", "", ".*", typedef_rewrite_without_colons],
        #
        #
        #
        ["KProtocolInfo", "FileNameUsedForCopying", ".*", ".*", typedef_rewrite_enums],
        ["KSycoca", "DatabaseType", ".*", ".*", typedef_rewrite_enums],
        #
        # There are two version of KSharedConfigPtr in ksharedconfig.h and kconfiggroup.h.
        #
        [".*", "KSharedConfigPtr", ".*", "QExplicitlySharedDataPointer<KSharedConfig>", typedef_discard],
        #
        # There are two version of Display in kstartupinfo.h and kxmessages.h.
        #
        ["kstartupinfo.h|kxmessages.h", "Display", ".*", ".*", typedef_discard],
        ["kmimetypetrader.h", "KServiceOfferList", ".*", ".*", typedef_discard],
    ]


def variable_rules():

    return [
        #
        # Discard variable emitted by QOBJECT.
        #
        [".*", "staticMetaObject", ".*", variable_discard],
        #
        # Discard "private" variables (check they are protected!).
        #
        [".*", "d_ptr", ".*", variable_discard_protected],
        #
        # Discard variable emitted by QOBJECT.
        #
        [".*", "d", ".*Private.*", variable_discard],
    ]
