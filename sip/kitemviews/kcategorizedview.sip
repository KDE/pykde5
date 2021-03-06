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

class KCategorizedView : QListView
{
%TypeHeaderCode
#include <kcategorizedview.h>
%End

public:
                            KCategorizedView (QWidget* parent = 0);
    ~KCategorizedView ();
    virtual void            setModel (QAbstractItemModel* model);
    void                    setGridSize (const QSize& size);
    void                    setGridSizeOwn (const QSize& size);
    virtual QRect           visualRect (const QModelIndex& index) const;
    KCategoryDrawer*        categoryDrawer () const;
    void                    setCategoryDrawer (KCategoryDrawer* categoryDrawer);
    int                     categorySpacing () const;
    void                    setCategorySpacing (int categorySpacing);
    bool                    alternatingBlockColors () const;
    void                    setAlternatingBlockColors (bool enable);
    bool                    collapsibleBlocks () const;
    void                    setCollapsibleBlocks (bool enable);
    QModelIndexList         block (const QString& category);
    QModelIndexList         block (const QModelIndex& representative);
    virtual QModelIndex     indexAt (const QPoint& point) const;
    virtual void            reset ();
protected:
    virtual void            paintEvent (QPaintEvent* event);
    virtual void            resizeEvent (QResizeEvent* event);
    virtual void            setSelection (const QRect& rect, QItemSelectionModel::SelectionFlags flags);
    virtual void            mouseMoveEvent (QMouseEvent* event);
    virtual void            mousePressEvent (QMouseEvent* event);
    virtual void            mouseReleaseEvent (QMouseEvent* event);
    virtual void            leaveEvent (QEvent* event);
    virtual void            startDrag (Qt::DropActions supportedActions);
    virtual void            dragMoveEvent (QDragMoveEvent* event);
    virtual void            dragEnterEvent (QDragEnterEvent* event);
    virtual void            dragLeaveEvent (QDragLeaveEvent* event);
    virtual void            dropEvent (QDropEvent* event);
    virtual QModelIndex     moveCursor (QAbstractItemView::CursorAction cursorAction, Qt::KeyboardModifiers modifiers);
    virtual void            rowsAboutToBeRemoved (const QModelIndex& parent, int start, int end);
    virtual void            updateGeometries ();
    virtual void            currentChanged (const QModelIndex& current, const QModelIndex& previous);
    virtual void            dataChanged (const QModelIndex& topLeft, const QModelIndex& bottomRight, const QVector<int>& roles = QVector<int>());
    virtual void            rowsInserted (const QModelIndex& parent, int start, int end);
    virtual void            slotLayoutChanged ();
};
