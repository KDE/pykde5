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

class KXYSelector : QWidget
{
%TypeHeaderCode
#include <kxyselector.h>
%End

public:
    explicit                KXYSelector (QWidget* parent = 0);
    ~KXYSelector ();
    void                    setValues (int xPos, int yPos);
    void                    setXValue (int xPos);
    void                    setYValue (int yPos);
    void                    setRange (int minX, int minY, int maxX, int maxY);
    void                    setMarkerColor (const QColor& col);
    int                     xValue () const;
    int                     yValue () const;
    QRect                   contentsRect () const;
    virtual QSize           minimumSizeHint () const;
signals:
    void                    valueChanged (int x, int y);
protected:
    virtual void            drawContents (QPainter*);
    virtual void            drawMarker (QPainter* p, int xp, int yp);
    virtual void            paintEvent (QPaintEvent* e);
    virtual void            mousePressEvent (QMouseEvent* e);
    virtual void            mouseMoveEvent (QMouseEvent* e);
    virtual void            wheelEvent (QWheelEvent*);
    void                    valuesFromPosition (int x, int y, int& xVal, int& yVal) const;
};
