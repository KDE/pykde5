// Copyright 2014 Simon Edwards <simon@simonzone.com>

//                 Generated by twine2

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

class KAr : KArchive
{
%TypeHeaderCode
#include <kar.h>
%End

public:
                            KAr (const QString& filename);
                            KAr (QIODevice* dev);
    virtual ~KAr ();
protected:
    bool                    doPrepareWriting (const QString& name, const QString& user, const QString& group, qint64 size, mode_t perm, const QDateTime& atime, const QDateTime& mtime, const QDateTime& ctime);
    bool                    doFinishWriting (qint64 size);
    bool                    doWriteDir (const QString& name, const QString& user, const QString& group, mode_t perm, const QDateTime& atime, const QDateTime& mtime, const QDateTime& ctime);
    bool                    doWriteSymLink (const QString& name, const QString& target, const QString& user, const QString& group, mode_t perm, const QDateTime& atime, const QDateTime& mtime, const QDateTime& ctime);
    bool                    openArchive (QIODevice::OpenMode mode);
    bool                    closeArchive ();
    void                    virtual_hook (int id, void* data);
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KArchive'
    sipType = NULL;

    if (dynamic_cast<K7Zip*>(sipCpp))
        sipType = sipType_K7Zip;
    else if (dynamic_cast<KAr*>(sipCpp))
        sipType = sipType_KAr;
    else if (dynamic_cast<KTar*>(sipCpp))
        sipType = sipType_KTar;
    else if (dynamic_cast<KZip*>(sipCpp))
        sipType = sipType_KZip;
%End
};
%ModuleHeaderCode
//ctscc
#include <k7zip.h>
#include <kar.h>
#include <karchive.h>
#include <ktar.h>
#include <kzip.h>
%End
