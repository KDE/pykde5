// Copyright 2014 Simon Edwards <simon@simonzone.com>

// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU Library General Public License as
// published by the Free Software Foundation; either version 2, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details

// You should have received a copy of the GNU Library General Public
// License along with this program; if not, write to the
// Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

%Module PyKDE5.typedefs

typedef uint mode_t;

typedef long time_t;

typedef ulong size_t;

typedef int ssize_t;

typedef int pid_t;

typedef ulong Window;

typedef bool Bool;

typedef uint WFlags;

typedef long off_t;

typedef uint uid_t;

typedef uint gid_t;

template <TYPE1,int>
%MappedType QMap<TYPE1,int>
{
%TypeHeaderCode
#include <qmap.h>
%End

%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QMap<TYPE1, int>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        TYPE1 *t1 = new TYPE1(i.key());
        int t2 = i.value();

        PyObject *t1obj = sipConvertFromNewType(t1, sipType_TYPE1, sipTransferObj);
#if PY_MAJOR_VERSION >= 3
        PyObject *t2obj = PyLong_FromLong(t2);
#else
        PyObject *t2obj = PyInt_FromLong(t2);
#endif

        if (t1obj == NULL || t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj) {
                Py_DECREF(t1obj);
            } else {
                delete t1;
            } 
            
            if (t2obj) {
                Py_DECREF(t2obj);
            }
            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End

%ConvertToTypeCode
    PyObject *t1obj;
    PyObject *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
        {
            if (!sipCanConvertToType(t1obj, sipType_TYPE1, SIP_NOT_NONE))
                return 0;

#if PY_MAJOR_VERSION >= 3
            if (!PyNumber_Check(t2obj))
#else
            if (!PyInt_Check(t2obj))
#endif
                return 0;
        } 

        return 1;
    }

    QMap<TYPE1, int> *qm = new QMap<TYPE1, int>;
 
    i = 0;
    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1;

        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, sipType_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));

#if PY_MAJOR_VERSION >= 3
        int t2 = PyLong_AsLong (t2obj);
#else
        int t2 = PyInt_AS_LONG (t2obj);
#endif
 
        if (*sipIsErr)
        {
            sipReleaseType(t1, sipType_TYPE1, state1);

            delete qm;
            return 0;
        }

        qm->insert(*t1, t2);

        sipReleaseType(t1, sipType_TYPE1, state1);
    }
 
    *sipCppPtr = qm;
 
    return sipGetState(sipTransferObj);
%End
};
