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

class KMimeTypeChooser : QWidget
{
%TypeHeaderCode
#include <kmimetypechooser.h>
%End

public:
    enum Visuals
    {
        Comments,
        Patterns,
        EditButton
    };
    explicit                KMimeTypeChooser (const QString& text = QString(), const QStringList& selectedMimeTypes = QStringList(), const QString& defaultGroup = QString(), const QStringList& groupsToShow = QStringList(), int visuals = Comments|Patterns|EditButton, QWidget* parent = 0);
    ~KMimeTypeChooser ();
    QStringList             mimeTypes () const;
    QStringList             patterns () const;
};
class KMimeTypeChooserDialog : QDialog
{
%TypeHeaderCode
#include <kmimetypechooser.h>
%End

public:
    explicit                KMimeTypeChooserDialog (const QString& caption = QString(), const QString& text = QString(), const QStringList& selectedMimeTypes = QStringList(), const QString& defaultGroup = QString(), const QStringList& groupsToShow = QStringList(), int visuals = KMimeTypeChooser::Comments|KMimeTypeChooser::Patterns|KMimeTypeChooser::EditButton, QWidget* parent = 0);
                            KMimeTypeChooserDialog (const QString& caption, const QString& text, const QStringList& selectedMimeTypes, const QString& defaultGroup, QWidget* parent = 0);
    ~KMimeTypeChooserDialog ();
    KMimeTypeChooser*       chooser ();
};
