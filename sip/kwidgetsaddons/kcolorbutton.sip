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

class KColorButton : QPushButton
{
%TypeHeaderCode
#include <kcolorbutton.h>
%End

public:
    explicit                KColorButton (QWidget* parent = 0);
    explicit                KColorButton (const QColor& c, QWidget* parent = 0);
                            KColorButton (const QColor& c, const QColor& defaultColor, QWidget* parent = 0);
    virtual ~KColorButton ();
    QColor                  color () const;
    void                    setColor (const QColor& c);
    void                    setAlphaChannelEnabled (bool alpha);
    bool                    isAlphaChannelEnabled () const;
    QColor                  defaultColor () const;
    void                    setDefaultColor (const QColor& c);
    QSize                   sizeHint () const;
    QSize                   minimumSizeHint () const;
signals:
    void                    changed (const QColor& newColor);
protected:
    virtual void            paintEvent (QPaintEvent* pe);
    virtual void            dragEnterEvent (QDragEnterEvent*);
    virtual void            dropEvent (QDropEvent*);
    virtual void            mousePressEvent (QMouseEvent* e);
    virtual void            mouseMoveEvent (QMouseEvent* e);
    virtual void            keyPressEvent (QKeyEvent* e);
};
