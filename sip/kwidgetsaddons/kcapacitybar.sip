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

class KCapacityBar : QWidget
{
%TypeHeaderCode
#include <kcapacitybar.h>
%End

public:
    enum DrawTextMode
    {
        DrawTextInline,
        DrawTextOutline
    };
    explicit                KCapacityBar (KCapacityBar::DrawTextMode drawTextMode = KCapacityBar::DrawTextMode::DrawTextOutline, QWidget* parent = 0);
    ~KCapacityBar ();
    void                    setValue (int value);
    int                     value () const;
    void                    setText (const QString& text);
    QString                 text () const;
    void                    setFillFullBlocks (bool fillFullBlocks);
    bool                    fillFullBlocks () const;
    void                    setContinuous (bool continuous);
    bool                    continuous () const;
    void                    setBarHeight (int barHeight);
    int                     barHeight () const;
    void                    setHorizontalTextAlignment (Qt::Alignment textAlignment);
    Qt::Alignment           horizontalTextAlignment () const;
    void                    setDrawTextMode (KCapacityBar::DrawTextMode mode);
    KCapacityBar::DrawTextMode  drawTextMode () const;
    void                    drawCapacityBar (QPainter* p, const QRect& rect) const;
    virtual QSize           minimumSizeHint () const;
protected:
    virtual void            paintEvent (QPaintEvent* event);
};
