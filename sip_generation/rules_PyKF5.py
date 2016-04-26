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
import PyKF5_methodcode

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


def _function_discard_non_const(container, function, sip, matcher):
    if not sip["suffix"]:
        sip["name"] = ""


def _function_discard_protected(container, function, sip, matcher):
    if function.access_specifier == AccessSpecifier.PROTECTED:
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


def _unexposed_discard(container, unexposed, sip, matcher):
    sip["name"] = ""


def _variable_discard(container, variable, sip, matcher):
    sip["name"] = ""


def _variable_discard_protected(container, variable, sip, matcher):
    if variable.access_specifier == AccessSpecifier.PROTECTED:
        sip["name"] = ""


def _variable_array_to_star(container, variable, sip, matcher):
    sip["decl"] = sip["decl"].replace("[]", "*")


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
        ["KCalCore::Duration", "operator bool|operator!", ".*", ".*", "", _function_discard],
        ["KPageDialog", "pageWidget|buttonBox", ".*", ".*", "", _function_discard_non_const],
        [".*", ".*", ".*", ".*", ".*Private.*", _function_discard_protected],
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
        #
        # Redundant typedef.
        #
        ["agenttype.h", "QVariantMap", ".*", ".*", _typedef_discard],
    ]


def unexposed_rules():

    return [
        #
        # Discard ....
        #
        ["Akonadi", ".*", ".*Item::setPayloadImpl.*", _unexposed_discard],
        ["Akonadi", ".*", ".*std::enable_if.*", _unexposed_discard],
        ["exception.h", ".*", ".*AKONADI_EXCEPTION_MAKE_TRIVIAL_INSTANCE.*", _unexposed_discard],
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
        [".*", "d", ".*Private.*", _variable_discard_protected],
        #
        # [] -> *
        #
        ["Akonadi::Item", "FullPayload", ".*", _variable_array_to_star],
        ["Akonadi::Tag", "PLAIN|GENERIC", ".*", _variable_array_to_star],
    ]


methodcode = {

"KParts::BrowserExtension": #"kparts/browserextension.h"
{
    "createNewWindow": # void createNewWindow (const KUrl& url, const KParts::OpenUrlArguments& arguments = KParts::OpenUrlArguments(), const KParts::BrowserArguments& browserArguments = KParts::BrowserArguments(), const KParts::WindowArgs& windowArgs = KParts::WindowArgs(), KParts::ReadOnlyPart** part = 0) [void (const KUrl&, const KParts::OpenUrlArguments& = KParts::OpenUrlArguments(), const KParts::BrowserArguments& = KParts::BrowserArguments(), const KParts::WindowArgs& = KParts::WindowArgs(), KParts::ReadOnlyPart** = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp->KParts::BrowserExtension::createNewWindow (*a0, *a1, *a2, *a3, &a4);
        Py_END_ALLOW_THREADS
        """,
},
"KLocalizedString": #"kdecore/klocalizedstring.h"
{
    "i18n": # QString i18n (const char* text, ...);
        """
        QString result = klocalizedstring_i18n_template(ki18n(a0),a1,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """,

    "i18nc": # QString i18nc (const char* ctxt, const char* text, ...);
        """
        QString result = klocalizedstring_i18n_template(ki18nc(a0,a1),a2,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """,

    "i18np": # QString i18np (const char* sing, const char* plur, ...);
        """
        QString result = klocalizedstring_i18n_template(ki18np(a0,a1),a2,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """,

    "i18ncp": # QString i18ncp (const char* ctxt, const char* sing, const char* plur, ...);
        """
        QString result = klocalizedstring_i18n_template(ki18ncp(a0,a1,a2),a3,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """,
},
"kdecore/kurl.h": #"kdecore/kurl.h"
{
    "__len__": # int __len__ ();
        """
        //returns (int)
        Py_BEGIN_ALLOW_THREADS
        sipRes = sipCpp -> count();
        Py_END_ALLOW_THREADS
        """,

    "__setitem__": # void __setitem__ (int, const KUrl&);
        """
        //takes index | (int) | value | (KUrl)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            (*sipCpp)[a0] = *a1;
        """,

    "__setitem__": # void __setitem__ (SIP_PYSLICE, const KUrl::List&);
        """
        //takes range | (a Python slice) | urlList | (KUrl.List)
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp -> count();

        if (sipConvertFromSliceObject(a0,len,&start,&stop,&step,&slicelength) < 0)
            sipIsErr = 1;
        else
        {
            int vlen = a1 -> count();
            if (vlen != slicelength)
            {
                sipBadLengthForSlice(vlen,slicelength);
                sipIsErr = 1;
            }
            else
            {
                KUrl::List::ConstIterator it = a1 -> begin();
                for (i = 0; i < slicelength; ++i)
                {
                    (*sipCpp)[start] = *it;
                    start += step;
                    ++it;
                }
            }
        }
        """,

    "__delitem__": # void __delitem__ (int);
        """
        //takes index | (int)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipCpp -> removeAt(a0);
        """,

    "__delitem__": # void __delitem__ (SIP_PYSLICE);
        """
        //takes range | (a Python slice)
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp -> count();
        if (sipConvertFromSliceObject(a0,len,&start,&stop,&step,&slicelength) < 0)
            sipIsErr = 1;
        else
            for (i = 0; i < slicelength; ++i)
            {
                sipCpp -> removeAt(start);
                start += step - 1;
            }
        """,

    "[]": # KUrl operator [] (int);
        """
        //returns (KUrl)
        //takes index | (int)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipRes = new KUrl((*sipCpp)[a0]);
        """,

    "[]": # KUrl::List operator [] (SIP_PYSLICE);
        """
        //returns (KUrl.List)
        //takes range | (a Python slice)
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp -> count();

        if (sipConvertFromSliceObject(a0,len,&start,&stop,&step,&slicelength) < 0)
            sipIsErr = 1;
        else
        {
            sipRes = new KUrl::List();

            for (i = 0; i < slicelength; ++i)
            {
                (*sipRes) += (*sipCpp)[start];
                start += step;
            }
        }
        """,

    "+": # KUrl::List operator + (const KUrl::List&);
        """
        //returns (KUrl.List)
        //takes listToAdd | (KUrl.List)
        Py_BEGIN_ALLOW_THREADS
        //    sipRes = new KUrl::List((const KUrl::List&)((*sipCpp) + *a0));
        sipRes = new KUrl::List (*sipCpp);
        (*sipRes) += (*a0);
        Py_END_ALLOW_THREADS
        """,

    "": # KUrl::List operator * (int);
        """
        sipRes = new KUrl::List();

        for (int i = 0; i < a0; ++i)
            (*sipRes) += (*sipCpp);
        """,

    "=": # KUrl::List& operator *= (int);
        """
        //returns (KUrl.List)
        //takes val | (int)
        KUrl::List orig(*sipCpp);

        sipCpp -> clear();

        for (int i = 0; i < a0; ++i)
            (*sipCpp) += orig;
        """,

    "__contains__": # int __contains__ (KUrl);
        """
        //returns (bool)
        //takes a0 | (KUrl)
        // It looks like you can't assign QBool to int.
        sipRes = bool(sipCpp->contains(*a0));
        """,
},
"KCoreConfigSkeleton::ItemBool": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemBool": # ItemBool (const QString& _group, const QString& _key, bool reference, bool defaultValue = 1) [(const QString& _group, const QString& _key, bool& reference, bool defaultValue = 1)];
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemBool (PyItemBool (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemBool (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemInt": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemInt": # ItemInt (const QString& _group, const QString& _key, qint32 reference, qint32 defaultValue = 0) [(const QString& _group, const QString& _key, qint32& reference, qint32 defaultValue = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemInt (PyItemInt (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemInt (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemLongLong": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemLongLong": # ItemLongLong (const QString& _group, const QString& _key, qint64 reference, qint64 defaultValue = 0) [(const QString& _group, const QString& _key, qint64& reference, qint64 defaultValue = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemLongLong (PyItemLongLong (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemLongLong (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemEnum": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemEnum": # ItemEnum (const QString& _group, const QString& _key, qint32 reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice> choices, qint32 defaultValue = 0) [(const QString& _group, const QString& _key, qint32& reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice>& choices, qint32 defaultValue = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipKCoreConfigSkeleton_ItemEnum (*a0, *a1, a2, *a3, a4);
        //    sipCpp = new sipKCoreConfigSkeleton_ItemEnum (PyItemEnum (*a0, *a1, a2, *a3, a4));
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemUInt": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemUInt": # ItemUInt (const QString& _group, const QString& _key, quint32 reference, quint32 defaultValue = 0) [(const QString& _group, const QString& _key, quint32& reference, quint32 defaultValue = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemUInt (PyItemUInt (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemUInt (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemULongLong": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemULongLong": # ItemULongLong (const QString& _group, const QString& _key, quint64 reference, quint64 defaultValue = 0) [(const QString& _group, const QString& _key, quint64& reference, quint64 defaultValue = 0)];
        """
            Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemULongLong (PyItemULongLong (*a0, *a1, a2, a3));
            sipCpp = new sipKCoreConfigSkeleton_ItemULongLong (*a0, *a1, a2, a3);
            Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton::ItemDouble": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemDouble": # ItemDouble (const QString& _group, const QString& _key, double reference, double defaultValue = 0) [(const QString& _group, const QString& _key, double& reference, double defaultValue = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemDouble (PyItemDouble (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemDouble (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """,
},
"KCoreConfigSkeleton": #"kdecore/kcoreconfigskeleton.h"
{
    "addItemBool": # KCoreConfigSkeleton::ItemBool* addItemBool (const QString& name, bool& reference /In/, bool defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemBool (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemInt": # KCoreConfigSkeleton::ItemInt* addItemInt (const QString& name, qint32& reference /In/, qint32 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemInt (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemUInt": # KCoreConfigSkeleton::ItemUInt* addItemUInt (const QString& name, quint32& reference /In/, quint32 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemUInt (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemLongLong": # KCoreConfigSkeleton::ItemLongLong* addItemLongLong (const QString& name, qint64& reference /In/, qint64 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemLongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemInt64": # KCoreConfigSkeleton::ItemLongLong* addItemInt64 (const QString& name, qint64& reference /In/, qint64 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemLongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemULongLong": # KCoreConfigSkeleton::ItemULongLong* addItemULongLong (const QString& name, quint64& reference /In/, quint64 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemULongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemUInt64": # KCoreConfigSkeleton::ItemULongLong* addItemUInt64 (const QString& name, quint64& reference /In/, quint64 defaultValue = 0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemULongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "addItemDouble": # KCoreConfigSkeleton::ItemDouble* addItemDouble (const QString& name, double& reference /In/, double defaultValue = 0.0, const QString& key = QString());
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemDouble (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """,

    "init": # static void init (SIP_PYLIST argv, const QByteArray& appname, const QByteArray& catalog, const KLocalizedString& programName, const QByteArray& version, const KLocalizedString& description = KLocalizedString(), int stdargs = 3) [void (int, char**, const QByteArray&, const QByteArray&, const KLocalizedString&, const QByteArray&, const KLocalizedString& = KLocalizedString(), KCmdLineArgs::StdCmdLineArgs = 3)];
        """
        KCmdLineArgs::StdCmdLineArgs cmdLineArgs = (KCmdLineArgs::StdCmdLineArgs) a6;
        int argc, nargc;
        char **argv;

        // Convert the list.

        if ((argv = pyArgvToC(a0, &argc)) == NULL)
            return NULL;

        // Create it now the arguments are right.
        nargc = argc;

        Py_BEGIN_ALLOW_THREADS
        KCmdLineArgs::init (nargc, argv, *a1, *a2, *a3, *a4, *a5, cmdLineArgs);
        Py_END_ALLOW_THREADS

        // Now modify the original list.

        updatePyArgv (a0, argc, argv);
        """,

    "init": # static void init (SIP_PYLIST argv, const KAboutData* about, int stdargs = 3) [void (int, char**, const KAboutData*, KCmdLineArgs::StdCmdLineArgs = 3)];
        """
        KCmdLineArgs::StdCmdLineArgs cmdLineArgs = (KCmdLineArgs::StdCmdLineArgs) a2;
        int argc, nargc;
        char **argv;

        // Convert the list.

        if ((argv = pyArgvToC(a0, &argc)) == NULL)
            return NULL;

        // Create it now the arguments are right.
        nargc = argc;

        Py_BEGIN_ALLOW_THREADS
        KCmdLineArgs::init (nargc, argv, a1, cmdLineArgs);
        Py_END_ALLOW_THREADS

        // Now modify the original list.

        updatePyArgv (a0, argc, argv);
        """,

    "version": # unsigned int version ();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::version ();
        Py_END_ALLOW_THREADS
        """,

    "versionMajor": # unsigned int versionMajor ();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionMajor ();
        Py_END_ALLOW_THREADS
        """,

    "versionMinor": # unsigned int versionMinor ();
        """
        Py_BEGIN_ALLOW_THREADS
            sipRes = KDE::versionMinor ();
            Py_END_ALLOW_THREADS
        """,

    "versionRelease": # unsigned int versionRelease ();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionRelease ();
        Py_END_ALLOW_THREADS
        """,

    "versionString": # const char* versionString ();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionString ();
        Py_END_ALLOW_THREADS
        """,

    "pykde_version": # unsigned int pykde_version ();
        """
        //version
        sipRes = 0x040002;
        """,

    "pykde_versionMajor": # unsigned int pykde_versionMajor ();
        """
        //major
        sipRes = 0x04;
        """,

    "pykde_versionMinor": # unsigned int pykde_versionMinor ();
        """
        //minor
        sipRes = 0x00;
        """,

    "pykde_versionRelease": # unsigned int pykde_versionRelease ();
        """
        //release
        sipRes = 0x02;
        """,

    "pykde_versionString": # const char* pykde_versionString ();
        """
        //string
        sipRes = "4.0.2 Rev 2";
        """,
},
"KFileItem": #"kio/kfileitem.h"
{
    "__len__": # int __len__ ();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = sipCpp -> count();
        Py_END_ALLOW_THREADS
        """,

    "__setitem__": # void __setitem__ (int, const KFileItem&);
        """
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            (*sipCpp)[a0] = *(KFileItem *)a1;
        """,

    "__setitem__": # void __setitem__ (SIP_PYSLICE, const KFileItemList&);
        """
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp -> count();

        if (sipConvertFromSliceObject(a0,len,&start,&stop,&step,&slicelength) < 0)
            sipIsErr = 1;
        else
        {
            int vlen = a1 -> count();
            if (vlen != slicelength)
            {
                sipBadLengthForSlice(vlen,slicelength);
                sipIsErr = 1;
            }
            else
            {
                KFileItemList::ConstIterator it = a1 -> begin();
                for (i = 0; i < slicelength; ++i)
                {
                    (*sipCpp)[start] = *it;
                    start += step;
                    ++it;
                }
            }
        }
        """,

    "__delitem__": # void __delitem__ (int);
        """
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipCpp -> removeAt ( a0);
        """,

    "__delitem__": # void __delitem__ (SIP_PYSLICE);
        """
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp -> count();
        if (sipConvertFromSliceObject(a0,len,&start,&stop,&step,&slicelength) < 0)
            sipIsErr = 1;
        else
            for (i = 0; i < slicelength; ++i)
            {
                sipCpp -> removeAt (start);
                start += step - 1;
            }
        """,

    "[]": # KFileItem operator [] (int);
        """
        int len;

        len = sipCpp->count();

        if ((a0 = (int)sipConvertFromSequenceIndex(a0, len)) < 0)
            sipIsErr = 1;
        else
            sipRes = new KFileItem((*sipCpp)[a0]);
        """,

    "[]": # KFileItemList operator [] (SIP_PYSLICE);
        """
        SIP_SSIZE_T len, start, stop, step, slicelength, i;

        len = sipCpp->count();

        #if PY_VERSION_HEX >= 0x03020000
        if (PySlice_GetIndicesEx(a0, len, &start, &stop, &step, &slicelength) < 0)
        #else
        if (PySlice_GetIndicesEx((PySliceObject *)a0, len, &start, &stop, &step, &slicelength) < 0)
        #endif
            sipIsErr = 1;
        else
        {
            sipRes = new KFileItemList();

            for (i = 0; i < slicelength; ++i)
            {
                (*sipRes) += (*sipCpp)[start];
                start += step;
            }
        }
        """,

    "Predicate": # explicit Predicate (const Solid::DeviceInterface::Type ifaceType) [(const Solid::DeviceInterface::Type&)];
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new Solid::Predicate (a0);
        Py_END_ALLOW_THREADS
        """,
},
"KTextEditor::MovingRange": #"ktexteditor/movingrange.h"
{
    "start": # KTextEditor::MovingCursor* start ();
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->start();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """,

    "end": # KTextEditor::MovingCursor* end ();
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->end();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """,

    "codeCompletionInterface": # KTextEditor::CodeCompletionInterface *codeCompletionInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CodeCompletionInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "sessionConfigInterface": # KTextEditor::SessionConfigInterface *sessionConfigInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "textHintInterface": # KTextEditor::TextHintInterface *textHintInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TextHintInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "annotationViewInterface": # KTextEditor::AnnotationViewInterface *annotationViewInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationViewInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "configInterface": # KTextEditor::ConfigInterface *configInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "coordinatesToCursorInterface": # KTextEditor::CoordinatesToCursorInterface *coordinatesToCursorInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CoordinatesToCursorInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "templateInterface": # KTextEditor::TemplateInterface *templateInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TemplateInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "templateInterface2": # KTextEditor::TemplateInterface2 *templateInterface2();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TemplateInterface2*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,
},
"KTextEditor::Editor": #"ktexteditor/editor.h"
{
    "commandInterface": # KTextEditor::CommandInterface *commandInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CommandInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "containerInterface": # KTextEditor::ContainerInterface *containerInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ContainerInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,
},
"KTextEditor::Document": #"ktexteditor/document.h"
{
    "annotationInterface": # KTextEditor::AnnotationInterface *annotationInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "markInterface": # KTextEditor::MarkInterface *markInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MarkInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "modificationInterface": # KTextEditor::ModificationInterface *modificationInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ModificationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "searchInterface": # KTextEditor::SearchInterface *searchInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SearchInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "variableInterface": # KTextEditor::VariableInterface *variableInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::VariableInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "movingInterface": # KTextEditor::MovingInterface *movingInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MovingInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "highlightInterface": # KTextEditor::HighlightInterface *highlightInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::HighlightInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "configInterface": # KTextEditor::ConfigInterface *configInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "parameterizedSessionConfigInterface": # KTextEditor::ParameterizedSessionConfigInterface *parameterizedSessionConfigInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ParameterizedSessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "sessionConfigInterface": # KTextEditor::SessionConfigInterface *sessionConfigInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "recoveryInterface": # KTextEditor::RecoveryInterface *recoveryInterface();
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::RecoveryInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """,

    "KApplication": # KApplication (Display* display, SIP_PYLIST list, const QByteArray& rAppName, bool GUIenabled = 1) [(Display*, int&, char**, const QByteArray&, bool = 1)];
        """
        // The Python interface is a list of argument strings that is modified.

        int argc;
        char **argv;

        // Convert the list.
        if ((argv = kdeui_ArgvToC(a1, argc)) == NULL)
            sipIsErr = 1;
        else
        {
            // Create it now the arguments are right.
            static int nargc;
            nargc = argc;

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipKApplication(a0, nargc, argv, *a2, a3);
            Py_END_ALLOW_THREADS

            // Now modify the original list.
            kdeui_UpdatePyArgv(a1, argc, argv);
        }
        """,
},
"NETRootInfo": #"kdeui/netwm.h"
{
    "NETRootInfo": # NETRootInfo (Display* display, Window supportWindow, const char* wmName, SIP_PYLIST properties, int screen = -1, bool doACtivate = 1) [(Display*, Window, const char*, const unsigned long*, int, int = -1, bool = 1)];
        """
        int count   = PyList_Size (a3);
        unsigned long *list = new unsigned long [count];

        for (int i = 0; i < count; i++) {
        #if PY_MAJOR_VERSION >= 3
            list [i] = (unsigned long)PyLong_AsLong (PyList_GET_ITEM (a3, i));
        #else
            list [i] = (unsigned long)PyInt_AS_LONG (PyList_GET_ITEM (a3, i));
        #endif
        }
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipNETRootInfo (a0, a1, a2, list, count, a4, a5);
        Py_END_ALLOW_THREADS

        delete list;
        """,

    "NETRootInfo": # NETRootInfo (Display* display, SIP_PYLIST properties, int screen = -1, bool doActivate = 1) [(Display*, const unsigned long*, int, int = -1, bool = 1)];
        """
        int count   = PyList_Size (a1);
        unsigned long *list = new unsigned long [count];

        for (int i = 0; i < count; i++)
        #if PY_MAJOR_VERSION >= 3
            list [i] = (unsigned long)PyLong_AsLong(PyList_GET_ITEM (a1, i));
        #else
            list [i] = (unsigned long)PyInt_AS_LONG (PyList_GET_ITEM (a1, i));
        #endif

        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipNETRootInfo (a0, list, count, a2, a3);
        Py_END_ALLOW_THREADS

        delete list;
        """,
},
"NETWinInfo": #"kdeui/netwm.h"
{
    "NETWinInfo": # NETWinInfo (Display* display, Window window, Window rootWindow, SIP_PYLIST properties, NET::Role role = NET::Client) [(Display*, Window, Window, const unsigned long*, int, Role = Client)];
        """
        int count   = PyList_Size (a3);
        unsigned long *list = new unsigned long [count];

        for (int i = 0; i < count; i++) {
        #if PY_MAJOR_VERSION >= 3
            list [i] = (unsigned long)PyLong_AsLong (PyList_GET_ITEM (a3, i));
        #else
            list [i] = (unsigned long)PyInt_AS_LONG (PyList_GET_ITEM (a3, i));
        #endif
        }

        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipNETWinInfo (a0, a1, a2, list, count, a4);
        Py_END_ALLOW_THREADS

        delete list;
        """,

    "KFontChooser": # explicit KFontChooser (QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::DisplayFrame, const QStringList& fontList = QStringList(), int visibleListSize = 8, Qt::CheckState* sizeIsRelativeState = 0) [(QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::DisplayFrame, const QStringList& = QStringList(), int = 8, Qt::CheckState* = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipKFontChooser (a0, *a1, *a2, a3, &a4);
        Py_END_ALLOW_THREADS
        """,
},
"KFontChooser":
{
    "KFontChooser": # explicit KFontDialog (QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, const QStringList& fontlist = QStringList(), Qt::CheckState* sizeIsRelativeState = 0) [(QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, const QStringList& = QStringList(), Qt::CheckState* = 0)];
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp= new sipKFontDialog (a0, *a1, *a2, &a3);
        Py_END_ALLOW_THREADS
        """,

    "getFont": # static SIP_PYTUPLE getFont (QFont& theFont, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState* sizeIsRelativeState = Qt::Unchecked) [int (QFont&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)];
        """
        int result;
        Py_BEGIN_ALLOW_THREADS
        result = KFontDialog::getFont (*a0, *a1, a2, &a3);
        Py_END_ALLOW_THREADS
        #if PY_MAJOR_VERSION >= 3
        sipRes = PyLong_FromLong (result);
        #else
        sipRes = PyInt_FromLong (result);
        #endif
        """,

    "getFontDiff": # static SIP_PYTUPLE getFontDiff (QFont& theFont, KFontChooser::FontDiffFlags& diffFlags, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked) [int (QFont&, KFontChooser::FontDiffFlags&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)];
        """
        int result;
        Py_BEGIN_ALLOW_THREADS
        result = KFontDialog::getFontDiff (*a0, *a1, *a2, a3, &a4);
        Py_END_ALLOW_THREADS

        #if PY_MAJOR_VERSION >= 3
        sipRes = PyLong_FromLong (result);
        #else
        sipRes = PyInt_FromLong (result);
        #endif
        """,

    "getFontAndText": # static SIP_PYTUPLE getFontAndText (QFont& theFont, QString& theString, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked) [int (QFont&, QString&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)];
        """
        int result;
        Py_BEGIN_ALLOW_THREADS
        result = KFontDialog::getFontAndText (*a0, *a1, *a2, a3, &a4);
        Py_END_ALLOW_THREADS

        #if PY_MAJOR_VERSION >= 3
        sipRes = PyLong_FromLong (result);
        #else
        sipRes = PyInt_FromLong (result);
        #endif
        """,
},
"KXmlGuiWindow":
{
    "createContainer": # virtual SIP_PYTUPLE createContainer (QWidget* parent /Transfer/, int index, const QDomElement& element) [QWidget* (QWidget* parent /Transfer/, int index, const QDomElement& element, QAction*& containerAction)];
        """
        QAction *containerAction;
        QWidget* res;
        Py_BEGIN_ALLOW_THREADS
        res = sipSelfWasArg ? sipCpp->KXMLGUIBuilder::createContainer (a0, a1, *a2, containerAction) : sipCpp->createContainer (a0, a1, *a2, containerAction);
        Py_END_ALLOW_THREADS

        PyObject *pyWidget;
        PyObject *pyContainerAction;

        if ((pyWidget = sipConvertFromNewInstance(res, sipClass_QWidget, NULL)) == NULL)
            return NULL;

        if ((pyContainerAction = sipConvertFromNewInstance(containerAction, sipClass_QAction, NULL)) == NULL)
            return NULL;

        sipRes = Py_BuildValue ("NN", pyWidget, pyContainerAction);
        """,
},
}


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
        self._unexposed_db = rules_engine.UnexposedRuleDb(unexposed_rules)
        self._var_db = rules_engine.VariableRuleDb(variable_rules)
        self._methodcode = rules_engine.MethodCodeDb(PyKF5_methodcode.code)

    def container_rules(self):
        return self._container_db

    def function_rules(self):
        return self._fn_db

    def param_rules(self):
        return self._param_db

    def typedef_rules(self):
        return self._typedef_db

    def unexposed_rules(self):
        return self._unexposed_db

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
            "AkonadiSearch/Debug/Debugmod.sip",
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
            "KDeclarative/CalendarEvents/CalendarEventsmod.sip",
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
            "KPeople/KPeople/Widgets/Widgetsmod.sip",
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
            "NetworkManagerQt/NetworkManagerQt/NetworkManagerQtmod.sip",
            "Plasma/Plasmamod.sip",
            "plasma/scripting/scriptingmod.sip",
            "PRISON/prison/prisonmod.sip",
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

    def methodcode(self, function, name):
        return self._methodcode.get(function, name)
