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
SIP binding custom %MethodCode for PyKF5.

"""

code = {
"KParts::BrowserExtension": #"kparts/browserextension.h"
{
    "createNewWindow":
    {
        "decl": "void createNewWindow (const KUrl& url, const KParts::OpenUrlArguments& arguments = KParts::OpenUrlArguments(), const KParts::BrowserArguments& browserArguments = KParts::BrowserArguments(), const KParts::WindowArgs& windowArgs = KParts::WindowArgs(), KParts::ReadOnlyPart** part = 0)",
        "decl2": "void (const KUrl&, const KParts::OpenUrlArguments& = KParts::OpenUrlArguments(), const KParts::BrowserArguments& = KParts::BrowserArguments(), const KParts::WindowArgs& = KParts::WindowArgs(), KParts::ReadOnlyPart** = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp->KParts::BrowserExtension::createNewWindow (*a0, *a1, *a2, *a3, &a4);
        Py_END_ALLOW_THREADS
        """
    },
},
"klocalizedstring.h": # KLocalizedString
{
    "i18n":
    {
        "decl": "QString i18n (const char* text, ...)",
        "code":
        """
        QString result = klocalizedstring_i18n_template(ki18n(a0),a1,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """
    },
    "i18nc":
    {
        "decl": "QString i18nc (const char* ctxt, const char* text, ...)",
        "code":
        """
        QString result = klocalizedstring_i18n_template(ki18nc(a0,a1),a2,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """
    },
    "i18np":
    {
        "decl": "QString i18np (const char* sing, const char* plur, ...)",
        "code":
        """
        QString result = klocalizedstring_i18n_template(ki18np(a0,a1),a2,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """
    },
    "i18ncp":
    {
        "decl": "QString i18ncp (const char* ctxt, const char* sing, const char* plur, ...)",
        "code":
        """
        QString result = klocalizedstring_i18n_template(ki18ncp(a0,a1,a2),a3,&sipIsErr);
        if (!sipIsErr) {
            sipRes = new QString(result);
        }
        """
    },
},
"kdecore/kurl.h": #"kdecore/kurl.h"
{
    "__len__":
    {
        "decl": "int __len__ ()",
        "code":
        """
        //returns (int)
        Py_BEGIN_ALLOW_THREADS
        sipRes = sipCpp -> count();
        Py_END_ALLOW_THREADS
        """
    },
    "__setitem__":
    {
        "decl": "void __setitem__ (int, const KUrl&)",
        "code":
        """
        //takes index | (int) | value | (KUrl)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            (*sipCpp)[a0] = *a1;
        """
    },
    "__setitem__":
    {
        "decl": "void __setitem__ (SIP_PYSLICE, const KUrl::List&)",
        "code":
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
        """
    },
    "__delitem__":
    {
        "decl": "void __delitem__ (int)",
        "code":
        """
        //takes index | (int)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipCpp -> removeAt(a0);
        """
    },
    "__delitem__":
    {
        "decl": "void __delitem__ (SIP_PYSLICE)",
        "code":
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
        """
    },
    "[]":
    {
        "decl": "KUrl operator",
        "decl2": "[] (int)",
        "code":
        """
        //returns (KUrl)
        //takes index | (int)
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipRes = new KUrl((*sipCpp)[a0]);
        """
    },
    "[]":
    {
        "decl": "KUrl::List operator",
        "decl2": "[] (SIP_PYSLICE)",
        "code":
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
        """
    },
    "+":
    {
        "decl": "KUrl::List operator + (const KUrl::List&)",
        "code":
        """
        //returns (KUrl.List)
        //takes listToAdd | (KUrl.List)
        Py_BEGIN_ALLOW_THREADS
        //    sipRes = new KUrl::List((const KUrl::List&)((*sipCpp) + *a0));
        sipRes = new KUrl::List (*sipCpp);
        (*sipRes) += (*a0);
        Py_END_ALLOW_THREADS
        """
    },
    "*":
    {
        "decl": "KUrl::List operator * (int)",
        "code":
        """
        sipRes = new KUrl::List();

        for (int i = 0; i < a0; ++i)
            (*sipRes) += (*sipCpp);
        """
    },
    "*=":
    {
        "decl": "KUrl::List& operator *= (int)",
        "code":
        """
        //returns (KUrl.List)
        //takes val | (int)
        KUrl::List orig(*sipCpp);

        sipCpp -> clear();

        for (int i = 0; i < a0; ++i)
            (*sipCpp) += orig;
        """
    },
    "__contains__":
    {
        "decl": "int __contains__ (KUrl)",
        "code":
        """
        //returns (bool)
        //takes a0 | (KUrl)
        // It looks like you can't assign QBool to int.
        sipRes = bool(sipCpp->contains(*a0));
        """
    },
},
"KCoreConfigSkeleton::ItemBool": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemBool":
    {
        "decl": "ItemBool (const QString& _group, const QString& _key, bool reference, bool defaultValue = 1)",
        "decl2": "void (const QString& _group, const QString& _key, bool& reference, bool defaultValue = 1)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemBool (PyItemBool (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemBool (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemInt": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemInt":
    {
        "decl": "ItemInt (const QString& _group, const QString& _key, qint32 reference, qint32 defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, qint32& reference, qint32 defaultValue = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemInt (PyItemInt (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemInt (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemLongLong": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemLongLong":
    {
        "decl": "ItemLongLong (const QString& _group, const QString& _key, qint64 reference, qint64 defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, qint64& reference, qint64 defaultValue = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemLongLong (PyItemLongLong (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemLongLong (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemEnum": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemEnum":
    {
        "decl": "ItemEnum (const QString& _group, const QString& _key, qint32 reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice> choices, qint32 defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, qint32& reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice>& choices, qint32 defaultValue = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipKCoreConfigSkeleton_ItemEnum (*a0, *a1, a2, *a3, a4);
        //    sipCpp = new sipKCoreConfigSkeleton_ItemEnum (PyItemEnum (*a0, *a1, a2, *a3, a4));
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemUInt": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemUInt":
    {
        "decl": "ItemUInt (const QString& _group, const QString& _key, quint32 reference, quint32 defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, quint32& reference, quint32 defaultValue = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemUInt (PyItemUInt (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemUInt (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemULongLong": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemULongLong":
    {
        "decl": "ItemULongLong (const QString& _group, const QString& _key, quint64 reference, quint64 defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, quint64& reference, quint64 defaultValue = 0)",
        "code":
        """
            Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemULongLong (PyItemULongLong (*a0, *a1, a2, a3));
            sipCpp = new sipKCoreConfigSkeleton_ItemULongLong (*a0, *a1, a2, a3);
            Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton::ItemDouble": #"kdecore/kcoreconfigskeleton.h"
{
    "ItemDouble":
    {
        "decl": "ItemDouble (const QString& _group, const QString& _key, double reference, double defaultValue = 0)",
        "decl2": "void (const QString& _group, const QString& _key, double& reference, double defaultValue = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        //    sipCpp = new sipKCoreConfigSkeleton_ItemDouble (PyItemDouble (*a0, *a1, a2, a3));
        sipCpp = new sipKCoreConfigSkeleton_ItemDouble (*a0, *a1, a2, a3);
        Py_END_ALLOW_THREADS
        """
    },
},
"KCoreConfigSkeleton": #"kdecore/kcoreconfigskeleton.h"
{
    "addItemBool":
    {
        "decl": "KCoreConfigSkeleton::ItemBool* addItemBool (const QString& name, bool& reference /In/, bool defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemBool (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemInt":
    {
        "decl": "KCoreConfigSkeleton::ItemInt* addItemInt (const QString& name, qint32& reference /In/, qint32 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemInt (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemUInt":
    {
        "decl": "KCoreConfigSkeleton::ItemUInt* addItemUInt (const QString& name, quint32& reference /In/, quint32 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemUInt (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemLongLong":
    {
        "decl": "KCoreConfigSkeleton::ItemLongLong* addItemLongLong (const QString& name, qint64& reference /In/, qint64 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemLongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemInt64":
    {
        "decl": "KCoreConfigSkeleton::ItemLongLong* addItemInt64 (const QString& name, qint64& reference /In/, qint64 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemLongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemULongLong":
    {
        "decl": "KCoreConfigSkeleton::ItemULongLong* addItemULongLong (const QString& name, quint64& reference /In/, quint64 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemULongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemUInt64":
    {
        "decl": "KCoreConfigSkeleton::ItemULongLong* addItemUInt64 (const QString& name, quint64& reference /In/, quint64 defaultValue = 0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemULongLong (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "addItemDouble":
    {
        "decl": "KCoreConfigSkeleton::ItemDouble* addItemDouble (const QString& name, double& reference /In/, double defaultValue = 0.0, const QString& key = QString())",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = new PyItemDouble (sipCpp->currentGroup(), a3->isNull() ? *a0 : *a3, a1, a2);
        sipCpp->addItem(sipRes, *a0);
        Py_END_ALLOW_THREADS
        """
    },
    "init":
    {
        "decl": "static void init (SIP_PYLIST argv, const QByteArray& appname, const QByteArray& catalog, const KLocalizedString& programName, const QByteArray& version, const KLocalizedString& description = KLocalizedString(), int stdargs = 3)",
        "decl2": "void (int, char**, const QByteArray&, const QByteArray&, const KLocalizedString&, const QByteArray&, const KLocalizedString& = KLocalizedString(), KCmdLineArgs::StdCmdLineArgs = 3)",
        "code":
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
        """
    },
    "init":
    {
        "decl": "static void init (SIP_PYLIST argv, const KAboutData* about, int stdargs = 3)",
        "decl2": "void (int, char**, const KAboutData*, KCmdLineArgs::StdCmdLineArgs = 3)",
        "code":
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
        """
    },
    "version":
    {
        "decl": "unsigned int version ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::version ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionMajor":
    {
        "decl": "unsigned int versionMajor ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionMajor ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionMinor":
    {
        "decl": "unsigned int versionMinor ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
            sipRes = KDE::versionMinor ();
            Py_END_ALLOW_THREADS
        """
    },
    "versionRelease":
    {
        "decl": "unsigned int versionRelease ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionRelease ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionString":
    {
        "decl": "const char* versionString ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionString ();
        Py_END_ALLOW_THREADS
        """
    },
    "pykde_version":
    {
        "decl": "unsigned int pykde_version ()",
        "code":
        """
        //version
        sipRes = 0x040002;
        """
    },
    "pykde_versionMajor":
    {
        "decl": "unsigned int pykde_versionMajor ()",
        "code":
        """
        //major
        sipRes = 0x04;
        """
    },
    "pykde_versionMinor":
    {
        "decl": "unsigned int pykde_versionMinor ()",
        "code":
        """
        //minor
        sipRes = 0x00;
        """
    },
    "pykde_versionRelease":
    {
        "decl": "unsigned int pykde_versionRelease ()",
        "code":
        """
        //release
        sipRes = 0x02;
        """
    },
    "pykde_versionString":
    {
        "decl": "const char* pykde_versionString ()",
        "code":
        """
        //string
        sipRes = "4.0.2 Rev 2";
        """
    },
},
"KFileItem": #"kio/kfileitem.h"
{
    "__len__":
    {
        "decl": "int __len__ ()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = sipCpp -> count();
        Py_END_ALLOW_THREADS
        """
    },
    "__setitem__":
    {
        "decl": "void __setitem__ (int, const KFileItem&)",
        "code":
        """
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            (*sipCpp)[a0] = *(KFileItem *)a1;
        """
    },
    "__setitem__":
    {
        "decl": "void __setitem__ (SIP_PYSLICE, const KFileItemList&)",
        "code":
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
        """
    },
    "__delitem__":
    {
        "decl": "void __delitem__ (int)",
        "code":
        """
        int len;

        len = sipCpp -> count();

        if ((a0 = sipConvertFromSequenceIndex(a0,len)) < 0)
            sipIsErr = 1;
        else
            sipCpp -> removeAt ( a0);
        """
    },
    "__delitem__":
    {
        "decl": "void __delitem__ (SIP_PYSLICE)",
        "code":
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
        """
    },
    "[]":
    {
        "decl": "KFileItem operator",
        "decl2": "[] (int)",
        "code":
        """
        int len;

        len = sipCpp->count();

        if ((a0 = (int)sipConvertFromSequenceIndex(a0, len)) < 0)
            sipIsErr = 1;
        else
            sipRes = new KFileItem((*sipCpp)[a0]);
        """
    },
    "[]":
    {
        "decl": "KFileItemList operator",
        "decl2": "[] (SIP_PYSLICE)",
        "code":
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
        """
    },
    "Predicate":
    {
        "decl": "explicit Predicate (const Solid::DeviceInterface::Type ifaceType)",
        "decl2": "void (const Solid::DeviceInterface::Type&)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new Solid::Predicate (a0);
        Py_END_ALLOW_THREADS
        """
    },
},
"KTextEditor::MovingRange": #"ktexteditor/movingrange.h"
{
    "start":
    {
        "decl": "KTextEditor::MovingCursor* start ()",
        "code":
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->start();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """
    },
    "end":
    {
        "decl": "KTextEditor::MovingCursor* end ()",
        "code":
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->end();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """
    },
    "codeCompletionInterface":
    {
        "decl": "KTextEditor::CodeCompletionInterface *codeCompletionInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CodeCompletionInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "sessionConfigInterface":
    {
        "decl": "KTextEditor::SessionConfigInterface *sessionConfigInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "textHintInterface":
    {
        "decl": "KTextEditor::TextHintInterface *textHintInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TextHintInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "annotationViewInterface":
    {
        "decl": "KTextEditor::AnnotationViewInterface *annotationViewInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationViewInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "configInterface":
    {
        "decl": "KTextEditor::ConfigInterface *configInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "coordinatesToCursorInterface":
    {
        "decl": "KTextEditor::CoordinatesToCursorInterface *coordinatesToCursorInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CoordinatesToCursorInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "templateInterface":
    {
        "decl": "KTextEditor::TemplateInterface *templateInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TemplateInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "templateInterface2":
    {
        "decl": "KTextEditor::TemplateInterface2 *templateInterface2()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TemplateInterface2*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
},
"KTextEditor/ktexteditor/editor.h": # "KTextEditor::Editor": #
{
    "commandInterface":
    {
        "decl": "KTextEditor::CommandInterface *commandInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CommandInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "containerInterface":
    {
        "decl": "KTextEditor::ContainerInterface *containerInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ContainerInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
},
"KTextEditor::Document": #"ktexteditor/document.h"
{
    "annotationInterface":
    {
        "decl": "KTextEditor::AnnotationInterface *annotationInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "markInterface":
    {
        "decl": "KTextEditor::MarkInterface *markInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MarkInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "modificationInterface":
    {
        "decl": "KTextEditor::ModificationInterface *modificationInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ModificationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "searchInterface":
    {
        "decl": "KTextEditor::SearchInterface *searchInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SearchInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "variableInterface":
    {
        "decl": "KTextEditor::VariableInterface *variableInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::VariableInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "movingInterface":
    {
        "decl": "KTextEditor::MovingInterface *movingInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MovingInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "highlightInterface":
    {
        "decl": "KTextEditor::HighlightInterface *highlightInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::HighlightInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "configInterface":
    {
        "decl": "KTextEditor::ConfigInterface *configInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "parameterizedSessionConfigInterface":
    {
        "decl": "KTextEditor::ParameterizedSessionConfigInterface *parameterizedSessionConfigInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ParameterizedSessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "sessionConfigInterface":
    {
        "decl": "KTextEditor::SessionConfigInterface *sessionConfigInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "recoveryInterface":
    {
        "decl": "KTextEditor::RecoveryInterface *recoveryInterface()",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::RecoveryInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "KApplication":
    {
        "decl": "KApplication (Display* display, SIP_PYLIST list, const QByteArray& rAppName, bool GUIenabled = 1)",
        "decl2": "void (Display*, int&, char**, const QByteArray&, bool = 1)",
        "code":
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
        """
    },
},
"NETRootInfo": #"kdeui/netwm.h"
{
    "NETRootInfo":
    {
        "decl": "NETRootInfo (Display* display, Window supportWindow, const char* wmName, SIP_PYLIST properties, int screen = -1, bool doACtivate = 1)",
        "decl2": "void (Display*, Window, const char*, const unsigned long*, int, int = -1, bool = 1)",
        "code":
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
        """
    },
    "NETRootInfo":
    {
        "decl": "NETRootInfo (Display* display, SIP_PYLIST properties, int screen = -1, bool doActivate = 1)",
        "decl2": "void (Display*, const unsigned long*, int, int = -1, bool = 1)",
        "code":
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
        """
    },
},
"NETWinInfo": #"kdeui/netwm.h"
{
    "NETWinInfo":
    {
        "decl": "NETWinInfo (Display* display, Window window, Window rootWindow, SIP_PYLIST properties, NET::Role role = NET::Client)",
        "decl2": "void (Display*, Window, Window, const unsigned long*, int, Role = Client)",
        "code":
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
        """
    },
    "KFontChooser":
    {
        "decl": "explicit KFontChooser (QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::DisplayFrame, const QStringList& fontList = QStringList(), int visibleListSize = 8, Qt::CheckState* sizeIsRelativeState = 0)",
        "decl2": "void (QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::DisplayFrame, const QStringList& = QStringList(), int = 8, Qt::CheckState* = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipKFontChooser (a0, *a1, *a2, a3, &a4);
        Py_END_ALLOW_THREADS
        """
    },
},
"KFontChooser":
{
    "KFontChooser":
    {
        "decl": "explicit KFontDialog (QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, const QStringList& fontlist = QStringList(), Qt::CheckState* sizeIsRelativeState = 0)",
        "decl2": "void (QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, const QStringList& = QStringList(), Qt::CheckState* = 0)",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp= new sipKFontDialog (a0, *a1, *a2, &a3);
        Py_END_ALLOW_THREADS
        """
    },
    "getFont":
    {
        "decl": "static SIP_PYTUPLE getFont (QFont& theFont, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState* sizeIsRelativeState = Qt::Unchecked)",
        "decl2": "int (QFont&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)",
        "code":
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
        """
    },
    "getFontDiff":
    {
        "decl": "static SIP_PYTUPLE getFontDiff (QFont& theFont, KFontChooser::FontDiffFlags& diffFlags, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked)",
        "decl2": "int (QFont&, KFontChooser::FontDiffFlags&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)",
        "code":
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
        """
    },
    "getFontAndText":
    {
        "decl": "static SIP_PYTUPLE getFontAndText (QFont& theFont, QString& theString, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked)",
        "decl2": "int (QFont&, QString&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0)",
        "code":
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
        """
    },
},
"KXmlGuiWindow":
{
    "createContainer":
    {
        "decl": "virtual SIP_PYTUPLE createContainer (QWidget* parent /Transfer/, int index, const QDomElement& element)",
        "decl2": "QWidget* (QWidget* parent /Transfer/, int index, const QDomElement& element, QAction*& containerAction)",
        "code":
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
        """
    },
},
}