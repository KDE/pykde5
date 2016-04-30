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
        "decl": "const KUrl& url, const KParts::OpenUrlArguments& arguments = KParts::OpenUrlArguments(), const KParts::BrowserArguments& browserArguments = KParts::BrowserArguments(), const KParts::WindowArgs& windowArgs = KParts::WindowArgs(), KParts::ReadOnlyPart** part = 0",
        "fn_result": "void",
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
    "operator[]":
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
    "operator[]":
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
    "operator+":
    {
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
    "operator*":
    {
        "code":
        """
        sipRes = new KUrl::List();

        for (int i = 0; i < a0; ++i)
            (*sipRes) += (*sipCpp);
        """
    },
    "operator*=":
    {
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
        "decl": "const QString& _group, const QString& _key, bool reference, bool defaultValue = 1",
        "decl2": "const QString& _group, const QString& _key, bool& reference, bool defaultValue = 1",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, qint32 reference, qint32 defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, qint32& reference, qint32 defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, qint64 reference, qint64 defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, qint64& reference, qint64 defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, qint32 reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice> choices, qint32 defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, qint32& reference, const QList<KCoreConfigSkeleton::ItemEnum::Choice>& choices, qint32 defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, quint32 reference, quint32 defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, quint32& reference, quint32 defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, quint64 reference, quint64 defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, quint64& reference, quint64 defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "const QString& _group, const QString& _key, double reference, double defaultValue = 0",
        "decl2": "const QString& _group, const QString& _key, double& reference, double defaultValue = 0",
        "fn_result2": "void",
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
        "decl": "SIP_PYLIST argv, const QByteArray& appname, const QByteArray& catalog, const KLocalizedString& programName, const QByteArray& version, const KLocalizedString& description = KLocalizedString(), int stdargs = 3",
        "decl2": "int, char**, const QByteArray&, const QByteArray&, const KLocalizedString&, const QByteArray&, const KLocalizedString& = KLocalizedString(), KCmdLineArgs::StdCmdLineArgs = 3",
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
        "decl": "SIP_PYLIST argv, const KAboutData* about, int stdargs = 3",
        "decl2": "int, char**, const KAboutData*, KCmdLineArgs::StdCmdLineArgs = 3",
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
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::version ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionMajor":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionMajor ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionMinor":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
            sipRes = KDE::versionMinor ();
            Py_END_ALLOW_THREADS
        """
    },
    "versionRelease":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionRelease ();
        Py_END_ALLOW_THREADS
        """
    },
    "versionString":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = KDE::versionString ();
        Py_END_ALLOW_THREADS
        """
    },
    "pykde_version":
    {
        "code":
        """
        //version
        sipRes = 0x040002;
        """
    },
    "pykde_versionMajor":
    {
        "code":
        """
        //major
        sipRes = 0x04;
        """
    },
    "pykde_versionMinor":
    {
        "code":
        """
        //minor
        sipRes = 0x00;
        """
    },
    "pykde_versionRelease":
    {
        "code":
        """
        //release
        sipRes = 0x02;
        """
    },
    "pykde_versionString":
    {
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
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = sipCpp -> count();
        Py_END_ALLOW_THREADS
        """
    },
    "__setitem__":
    {
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
        "decl": "const Solid::DeviceInterface::Type ifaceType",
        "decl2": "const Solid::DeviceInterface::Type&",
        "fn_result2": "void",
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
        "code":
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->start();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """
    },
    "end":
    {
        "code":
        """
        // Returning a ref of this class is problematic.
        const KTextEditor::MovingCursor& cursor = sipCpp->end();
        sipRes = const_cast<KTextEditor::MovingCursor *>(&cursor);
        """
    },
    "codeCompletionInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CodeCompletionInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "sessionConfigInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "textHintInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TextHintInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "annotationViewInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationViewInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "configInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "coordinatesToCursorInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CoordinatesToCursorInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "templateInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::TemplateInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "templateInterface2":
    {
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
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::CommandInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "containerInterface":
    {
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
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::AnnotationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "markInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MarkInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "modificationInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ModificationInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "searchInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SearchInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "variableInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::VariableInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "movingInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::MovingInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "highlightInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::HighlightInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "configInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "parameterizedSessionConfigInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::ParameterizedSessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "sessionConfigInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::SessionConfigInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "recoveryInterface":
    {
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipRes = dynamic_cast<KTextEditor::RecoveryInterface*>(sipCpp);
        Py_END_ALLOW_THREADS
        """
    },
    "KApplication":
    {
        "decl": "Display* display, SIP_PYLIST list, const QByteArray& rAppName, bool GUIenabled = 1",
        "decl2": "Display*, int&, char**, const QByteArray&, bool = 1",
        "fn_result2": "void",
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
        "decl": "Display* display, Window supportWindow, const char* wmName, SIP_PYLIST properties, int screen = -1, bool doACtivate = 1",
        "decl2": "Display*, Window, const char*, const unsigned long*, int, int = -1, bool = 1",
        "fn_result2": "void",
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
        "decl": "Display* display, SIP_PYLIST properties, int screen = -1, bool doActivate = 1",
        "decl2": "Display*, const unsigned long*, int, int = -1, bool = 1",
        "fn_result2": "void",
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
        "decl": "Display* display, Window window, Window rootWindow, SIP_PYLIST properties, NET::Role role = NET::Client",
        "decl2": "Display*, Window, Window, const unsigned long*, int, Role = Client",
        "fn_result2": "void",
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
},
"KFontChooser":
{
    "KFontChooser":
    {
        "decl": "QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::DisplayFrame, const QStringList& fontList = QStringList(), int visibleListSize = 8, Qt::CheckState* sizeIsRelativeState = 0",
        "decl2": "QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::DisplayFrame, const QStringList& = QStringList(), int = 8, Qt::CheckState* = 0",
        "fn_result2": "void",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipKFontChooser (a0, *a1, *a2, a3, &a4);
        Py_END_ALLOW_THREADS
        """
    },
    "KFontChooser":
    {
        "decl": "QWidget* parent /TransferThis/ = 0, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, const QStringList& fontlist = QStringList(), Qt::CheckState* sizeIsRelativeState = 0",
        "decl2": "QWidget* = 0, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, const QStringList& = QStringList(), Qt::CheckState* = 0",
        "fn_result2": "void",
        "code":
        """
        Py_BEGIN_ALLOW_THREADS
        sipCpp= new sipKFontDialog (a0, *a1, *a2, &a3);
        Py_END_ALLOW_THREADS
        """
    },
    "getFont":
    {
        "decl": "QFont& theFont, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState* sizeIsRelativeState = Qt::Unchecked",
        "fn_result": "SIP_PYTUPLE",
        "decl2": "QFont&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0",
        "fn_result2": "int",
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
        "decl": "QFont& theFont, KFontChooser::FontDiffFlags& diffFlags, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked",
        "fn_result": "SIP_PYTUPLE",
        "decl2": "QFont&, KFontChooser::FontDiffFlags&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0",
        "fn_result2": "int",
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
        "decl": "QFont& theFont, QString& theString, const KFontChooser::DisplayFlags& flags = KFontChooser::NoDisplayFlags, QWidget* parent /Transfer/ = 0, Qt::CheckState sizeIsRelativeState = Qt::Unchecked",
        "fn_result": "SIP_PYTUPLE",
        "decl2": "QFont&, QString&, const KFontChooser::DisplayFlags& = KFontChooser::NoDisplayFlags, QWidget* = 0, Qt::CheckState* = 0",
        "fn_result2": "int",
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
"KXMLGUIBuilder":
{
    "createContainer":
    {
        "decl": "QWidget* parent /Transfer/, int index, const QDomElement& element",
        "fn_result": "SIP_PYTUPLE",
        "decl2": "QWidget* parent /Transfer/, int index, const QDomElement& element, QAction*& containerAction",
        "fn_result2": "QWidget*",
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
