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

namespace Sonnet
{
class Dialog : QDialog
{
%TypeHeaderCode
#include <dialog.h>
%End

public:
    ~Dialog ();
    QString                 originalBuffer () const;
    QString                 buffer () const;
    void                    show ();
    void                    activeAutoCorrect (bool _active);
    void                    showProgressDialog (int timeout = 500);
    void                    showSpellCheckCompletionMessage (bool b = 1);
    void                    setSpellCheckContinuedAfterReplacement (bool b);
    void                    setBuffer (const QString&);
signals:
    void                    done (const QString& newBuffer);
    void                    misspelling (const QString& word, int start);
    void                    replace (const QString& oldWord, int start, const QString& newWord);
    void                    stop ();
    void                    cancel ();
    void                    autoCorrect (const QString& currentWord, const QString& replaceWord);
    void                    spellCheckStatus (const QString&);
    void                    languageChanged (const QString& language);
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Dialog'
    sipType = NULL;

    if (dynamic_cast<Sonnet::Dialog*>(sipCpp))
        sipType = sipType_Sonnet_Dialog;
%End
public:
                            Dialog (Sonnet::BackgroundChecker* checker, QWidget* parent);
};
};
%ModuleHeaderCode
//ctscc
#include <dialog.h>
%End
