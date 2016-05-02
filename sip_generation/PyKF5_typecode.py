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
SIP binding custom type-related code for PyKF5.
"""

code = {
# ./akonadi/agentfilterproxymodel.sip
"AgentFilterProxyModel": { #AgentFilterProxyModel : QSortFilterProxyModel
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AgentActionManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentActionManager;
    else if (dynamic_cast<Akonadi::AgentBase*>(sipCpp))
        {
        sipType = sipType_Akonadi_AgentBase;
        if (dynamic_cast<Akonadi::PreprocessorBase*>(sipCpp))
            sipType = sipType_Akonadi_PreprocessorBase;
        else if (dynamic_cast<Akonadi::ResourceBase*>(sipCpp))
            sipType = sipType_Akonadi_ResourceBase;
        }
    else if (dynamic_cast<Akonadi::AgentFactoryBase*>(sipCpp))
        sipType = sipType_Akonadi_AgentFactoryBase;
    else if (dynamic_cast<Akonadi::AgentManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentManager;
    else if (dynamic_cast<Akonadi::Control*>(sipCpp))
        sipType = sipType_Akonadi_Control;
    else if (dynamic_cast<Akonadi::EntityTreeViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeViewStateSaver;
    else if (dynamic_cast<Akonadi::Monitor*>(sipCpp))
        {
        sipType = sipType_Akonadi_Monitor;
        if (dynamic_cast<Akonadi::ChangeRecorder*>(sipCpp))
            sipType = sipType_Akonadi_ChangeRecorder;
        }
    else if (dynamic_cast<Akonadi::ServerManager*>(sipCpp))
        sipType = sipType_Akonadi_ServerManager;
    else if (dynamic_cast<Akonadi::Session*>(sipCpp))
        sipType = sipType_Akonadi_Session;
    else if (dynamic_cast<Akonadi::SpecialCollections*>(sipCpp))
        {
        sipType = sipType_Akonadi_SpecialCollections;
        if (dynamic_cast<Akonadi::SpecialMailCollections*>(sipCpp))
            sipType = sipType_Akonadi_SpecialMailCollections;
        }
    else if (dynamic_cast<Akonadi::StandardActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardActionManager;
    else if (dynamic_cast<Akonadi::StandardMailActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardMailActionManager;
    else if (dynamic_cast<Akonadi::ResourceBaseSettings*>(sipCpp))
        {
        sipType = sipType_Akonadi_ResourceBaseSettings;
        if (dynamic_cast<Akonadi::ResourceSettings*>(sipCpp))
            sipType = sipType_Akonadi_ResourceSettings;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceCreateJob*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceCreateJob;
    else if (dynamic_cast<Akonadi::CollectionAttributesSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_CollectionAttributesSynchronizationJob;
    else if (dynamic_cast<Akonadi::PartFetcher*>(sipCpp))
        sipType = sipType_Akonadi_PartFetcher;
    else if (dynamic_cast<Akonadi::RecursiveItemFetchJob*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveItemFetchJob;
    else if (dynamic_cast<Akonadi::ResourceSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_ResourceSynchronizationJob;
    else if (dynamic_cast<Akonadi::Job*>(sipCpp))
        {
        sipType = sipType_Akonadi_Job;
        if (dynamic_cast<Akonadi::CollectionCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCopyJob;
        else if (dynamic_cast<Akonadi::CollectionCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCreateJob;
        else if (dynamic_cast<Akonadi::CollectionDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionDeleteJob;
        else if (dynamic_cast<Akonadi::CollectionFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionFetchJob;
        else if (dynamic_cast<Akonadi::CollectionModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionModifyJob;
        else if (dynamic_cast<Akonadi::CollectionMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionMoveJob;
        else if (dynamic_cast<Akonadi::CollectionStatisticsJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsJob;
        else if (dynamic_cast<Akonadi::ItemCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCopyJob;
        else if (dynamic_cast<Akonadi::ItemCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCreateJob;
        else if (dynamic_cast<Akonadi::ItemDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemDeleteJob;
        else if (dynamic_cast<Akonadi::ItemFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemFetchJob;
        else if (dynamic_cast<Akonadi::ItemModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemModifyJob;
        else if (dynamic_cast<Akonadi::ItemMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemMoveJob;
        else if (dynamic_cast<Akonadi::ItemSearchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemSearchJob;
        else if (dynamic_cast<Akonadi::ItemSync*>(sipCpp))
            sipType = sipType_Akonadi_ItemSync;
        else if (dynamic_cast<Akonadi::LinkJob*>(sipCpp))
            sipType = sipType_Akonadi_LinkJob;
        else if (dynamic_cast<Akonadi::SearchCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_SearchCreateJob;
        else if (dynamic_cast<Akonadi::TransactionBeginJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionBeginJob;
        else if (dynamic_cast<Akonadi::TransactionCommitJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionCommitJob;
        else if (dynamic_cast<Akonadi::TransactionRollbackJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionRollbackJob;
        else if (dynamic_cast<Akonadi::TransactionSequence*>(sipCpp))
            {
            sipType = sipType_Akonadi_TransactionSequence;
            if (dynamic_cast<Akonadi::SpecialCollectionsRequestJob*>(sipCpp))
                {
                sipType = sipType_Akonadi_SpecialCollectionsRequestJob;
                if (dynamic_cast<Akonadi::SpecialMailCollectionsRequestJob*>(sipCpp))
                    sipType = sipType_Akonadi_SpecialMailCollectionsRequestJob;
                }
            }
        else if (dynamic_cast<Akonadi::UnlinkJob*>(sipCpp))
            sipType = sipType_Akonadi_UnlinkJob;
        }
    else if (dynamic_cast<Akonadi::ETMViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_ETMViewStateSaver;
    else if (dynamic_cast<Akonadi::CollectionStatisticsDelegate*>(sipCpp))
        sipType = sipType_Akonadi_CollectionStatisticsDelegate;
    else if (dynamic_cast<Akonadi::AgentInstanceModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceModel;
    else if (dynamic_cast<Akonadi::AgentTypeModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeModel;
    else if (dynamic_cast<Akonadi::CollectionModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_CollectionModel;
        if (dynamic_cast<Akonadi::CollectionStatisticsModel*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsModel;
        }
            sipType = sipType_Akonadi_CollectionStatisticsModel;
        }
    else if (dynamic_cast<Akonadi::EntityTreeModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeModel;
    else if (dynamic_cast<Akonadi::MessageThreaderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_MessageThreaderProxyModel;
    else if (dynamic_cast<Akonadi::SelectionProxyModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_SelectionProxyModel;
        if (dynamic_cast<Akonadi::FavoriteCollectionsModel*>(sipCpp))
            sipType = sipType_Akonadi_FavoriteCollectionsModel;
        }
    else if (dynamic_cast<Akonadi::AgentFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentFilterProxyModel;
    else if (dynamic_cast<Akonadi::CollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_CollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::EntityMimeTypeFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityMimeTypeFilterModel;
    else if (dynamic_cast<Akonadi::EntityOrderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityOrderProxyModel;
    else if (dynamic_cast<Akonadi::StatisticsProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_StatisticsProxyModel;
    else if (dynamic_cast<Akonadi::EntityRightsFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityRightsFilterModel;
    else if (dynamic_cast<Akonadi::RecursiveCollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveCollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::ItemModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_ItemModel;
        if (dynamic_cast<Akonadi::MessageModel*>(sipCpp))
            sipType = sipType_Akonadi_MessageModel;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceWidget;
    else if (dynamic_cast<Akonadi::AgentTypeWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeWidget;
    else if (dynamic_cast<Akonadi::CollectionPropertiesPage*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesPage;
    else if (dynamic_cast<Akonadi::CollectionComboBox*>(sipCpp))
        sipType = sipType_Akonadi_CollectionComboBox;
    else if (dynamic_cast<Akonadi::AgentTypeDialog*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeDialog;
    else if (dynamic_cast<Akonadi::CollectionDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionDialog;
    else if (dynamic_cast<Akonadi::CollectionPropertiesDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesDialog;
    else if (dynamic_cast<Akonadi::CollectionRequester*>(sipCpp))
        sipType = sipType_Akonadi_CollectionRequester;
    else if (dynamic_cast<Akonadi::EntityListView*>(sipCpp))
        sipType = sipType_Akonadi_EntityListView;
    else if (dynamic_cast<Akonadi::CollectionView*>(sipCpp))
        sipType = sipType_Akonadi_CollectionView;
    else if (dynamic_cast<Akonadi::EntityTreeView*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeView;
    else if (dynamic_cast<Akonadi::ItemView*>(sipCpp))
        sipType = sipType_Akonadi_ItemView;
%End
"""
},
# ./akonadi/itemserializerplugin.sip
"ItemSerializerPlugin": { #ItemSerializerPlugin /Abstract/
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'ItemSerializerPlugin'
    sipType = NULL;

    if (dynamic_cast<Akonadi::ItemSerializerPluginV2*>(sipCpp))
        sipType = sipType_Akonadi_ItemSerializerPluginV2;
%End
"""
},
# ./akonadi/resourcesettings.sip
"ResourceSettings": { #ResourceSettings : Akonadi::ResourceBaseSettings
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AgentActionManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentActionManager;
    else if (dynamic_cast<Akonadi::AgentBase*>(sipCpp))
        {
        sipType = sipType_Akonadi_AgentBase;
        if (dynamic_cast<Akonadi::PreprocessorBase*>(sipCpp))
            sipType = sipType_Akonadi_PreprocessorBase;
        else if (dynamic_cast<Akonadi::ResourceBase*>(sipCpp))
            sipType = sipType_Akonadi_ResourceBase;
        }
    else if (dynamic_cast<Akonadi::AgentFactoryBase*>(sipCpp))
        sipType = sipType_Akonadi_AgentFactoryBase;
    else if (dynamic_cast<Akonadi::AgentManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentManager;
    else if (dynamic_cast<Akonadi::Control*>(sipCpp))
        sipType = sipType_Akonadi_Control;
    else if (dynamic_cast<Akonadi::EntityTreeViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeViewStateSaver;
    else if (dynamic_cast<Akonadi::Monitor*>(sipCpp))
        {
        sipType = sipType_Akonadi_Monitor;
        if (dynamic_cast<Akonadi::ChangeRecorder*>(sipCpp))
            sipType = sipType_Akonadi_ChangeRecorder;
        }
    else if (dynamic_cast<Akonadi::ServerManager*>(sipCpp))
        sipType = sipType_Akonadi_ServerManager;
    else if (dynamic_cast<Akonadi::Session*>(sipCpp))
        sipType = sipType_Akonadi_Session;
    else if (dynamic_cast<Akonadi::SpecialCollections*>(sipCpp))
        {
        sipType = sipType_Akonadi_SpecialCollections;
        if (dynamic_cast<Akonadi::SpecialMailCollections*>(sipCpp))
            sipType = sipType_Akonadi_SpecialMailCollections;
        }
    else if (dynamic_cast<Akonadi::StandardActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardActionManager;
    else if (dynamic_cast<Akonadi::StandardMailActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardMailActionManager;
    else if (dynamic_cast<Akonadi::ResourceBaseSettings*>(sipCpp))
        {
        sipType = sipType_Akonadi_ResourceBaseSettings;
        if (dynamic_cast<Akonadi::ResourceSettings*>(sipCpp))
            sipType = sipType_Akonadi_ResourceSettings;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceCreateJob*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceCreateJob;
    else if (dynamic_cast<Akonadi::CollectionAttributesSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_CollectionAttributesSynchronizationJob;
    else if (dynamic_cast<Akonadi::PartFetcher*>(sipCpp))
        sipType = sipType_Akonadi_PartFetcher;
    else if (dynamic_cast<Akonadi::RecursiveItemFetchJob*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveItemFetchJob;
    else if (dynamic_cast<Akonadi::ResourceSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_ResourceSynchronizationJob;
    else if (dynamic_cast<Akonadi::Job*>(sipCpp))
        {
        sipType = sipType_Akonadi_Job;
        if (dynamic_cast<Akonadi::CollectionCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCopyJob;
        else if (dynamic_cast<Akonadi::CollectionCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCreateJob;
        else if (dynamic_cast<Akonadi::CollectionDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionDeleteJob;
        else if (dynamic_cast<Akonadi::CollectionFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionFetchJob;
        else if (dynamic_cast<Akonadi::CollectionModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionModifyJob;
        else if (dynamic_cast<Akonadi::CollectionMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionMoveJob;
        else if (dynamic_cast<Akonadi::CollectionStatisticsJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsJob;
        else if (dynamic_cast<Akonadi::ItemCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCopyJob;
        else if (dynamic_cast<Akonadi::ItemCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCreateJob;
        else if (dynamic_cast<Akonadi::ItemDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemDeleteJob;
        else if (dynamic_cast<Akonadi::ItemFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemFetchJob;
        else if (dynamic_cast<Akonadi::ItemModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemModifyJob;
        else if (dynamic_cast<Akonadi::ItemMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemMoveJob;
        else if (dynamic_cast<Akonadi::ItemSearchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemSearchJob;
        else if (dynamic_cast<Akonadi::ItemSync*>(sipCpp))
            sipType = sipType_Akonadi_ItemSync;
        else if (dynamic_cast<Akonadi::LinkJob*>(sipCpp))
            sipType = sipType_Akonadi_LinkJob;
        else if (dynamic_cast<Akonadi::SearchCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_SearchCreateJob;
        else if (dynamic_cast<Akonadi::TransactionBeginJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionBeginJob;
        else if (dynamic_cast<Akonadi::TransactionCommitJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionCommitJob;
        else if (dynamic_cast<Akonadi::TransactionRollbackJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionRollbackJob;
        else if (dynamic_cast<Akonadi::TransactionSequence*>(sipCpp))
            {
            sipType = sipType_Akonadi_TransactionSequence;
            if (dynamic_cast<Akonadi::SpecialCollectionsRequestJob*>(sipCpp))
                {
                sipType = sipType_Akonadi_SpecialCollectionsRequestJob;
                if (dynamic_cast<Akonadi::SpecialMailCollectionsRequestJob*>(sipCpp))
                    sipType = sipType_Akonadi_SpecialMailCollectionsRequestJob;
                }
            }
        else if (dynamic_cast<Akonadi::TrashJob*>(sipCpp))
            sipType = sipType_Akonadi_TrashJob;
        else if (dynamic_cast<Akonadi::TrashRestoreJob*>(sipCpp))
            sipType = sipType_Akonadi_TrashRestoreJob;
        else if (dynamic_cast<Akonadi::UnlinkJob*>(sipCpp))
            sipType = sipType_Akonadi_UnlinkJob;
        }
    else if (dynamic_cast<Akonadi::ETMViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_ETMViewStateSaver;
    else if (dynamic_cast<Akonadi::CollectionStatisticsDelegate*>(sipCpp))
        sipType = sipType_Akonadi_CollectionStatisticsDelegate;
    else if (dynamic_cast<Akonadi::AgentInstanceModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceModel;
    else if (dynamic_cast<Akonadi::AgentTypeModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeModel;
    else if (dynamic_cast<Akonadi::CollectionModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_CollectionModel;
        if (dynamic_cast<Akonadi::CollectionStatisticsModel*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsModel;
        }
    else if (dynamic_cast<Akonadi::EntityTreeModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeModel;
    else if (dynamic_cast<Akonadi::MessageThreaderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_MessageThreaderProxyModel;
    else if (dynamic_cast<Akonadi::SelectionProxyModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_SelectionProxyModel;
        if (dynamic_cast<Akonadi::FavoriteCollectionsModel*>(sipCpp))
            sipType = sipType_Akonadi_FavoriteCollectionsModel;
        }
    else if (dynamic_cast<Akonadi::AgentFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentFilterProxyModel;
    else if (dynamic_cast<Akonadi::CollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_CollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::EntityMimeTypeFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityMimeTypeFilterModel;
    else if (dynamic_cast<Akonadi::EntityOrderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityOrderProxyModel;
    else if (dynamic_cast<Akonadi::StatisticsProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_StatisticsProxyModel;
    else if (dynamic_cast<Akonadi::EntityRightsFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityRightsFilterModel;
    else if (dynamic_cast<Akonadi::RecursiveCollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveCollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::TrashFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_TrashFilterProxyModel;
    else if (dynamic_cast<Akonadi::ItemModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_ItemModel;
        if (dynamic_cast<Akonadi::MessageModel*>(sipCpp))
            sipType = sipType_Akonadi_MessageModel;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceWidget;
    else if (dynamic_cast<Akonadi::AgentTypeWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeWidget;
    else if (dynamic_cast<Akonadi::CollectionPropertiesPage*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesPage;
    else if (dynamic_cast<Akonadi::CollectionComboBox*>(sipCpp))
        sipType = sipType_Akonadi_CollectionComboBox;
    else if (dynamic_cast<Akonadi::AgentTypeDialog*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeDialog;
    else if (dynamic_cast<Akonadi::CollectionDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionDialog;
    else if (dynamic_cast<Akonadi::CollectionPropertiesDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesDialog;
    else if (dynamic_cast<Akonadi::CollectionRequester*>(sipCpp))
        sipType = sipType_Akonadi_CollectionRequester;
    else if (dynamic_cast<Akonadi::EntityListView*>(sipCpp))
        sipType = sipType_Akonadi_EntityListView;
    else if (dynamic_cast<Akonadi::CollectionView*>(sipCpp))
        sipType = sipType_Akonadi_CollectionView;
    else if (dynamic_cast<Akonadi::EntityTreeView*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeView;
    else if (dynamic_cast<Akonadi::ItemView*>(sipCpp))
        sipType = sipType_Akonadi_ItemView;
%End
"""
},
# ./akonadi/entity.sip
"QList<Akonadi::Entity::Id>": { #QList<Akonadi::Entity::Id>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        PyObject *pobj;

        if ((pobj = PyLong_FromLongLong (sipCpp->value(i))) == NULL)
        {
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QList<Akonadi::Entity::Id> *ql = new QList<Akonadi::Entity::Id>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
        ql->append((Akonadi::Entity::Id)PyLong_AsLongLong(PyList_GET_ITEM(sipPy, i)));

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
"QVector<Akonadi::Entity::Id>": { #QVector<Akonadi::Entity::Id>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        PyObject *pobj;

        if ((pobj = PyLong_FromLongLong (sipCpp->value(i))) == NULL)
        {
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QVector<Akonadi::Entity::Id> *ql = new QVector<Akonadi::Entity::Id>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
        ql->append((Akonadi::Entity::Id)PyLong_AsLongLong(PyList_GET_ITEM(sipPy, i)));

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./akonadi/agentbase.sip
"AgentBase": { #AgentBase : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Observer'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AgentBase::ObserverV2*>(sipCpp))
        sipType = sipType_Akonadi_AgentBase_ObserverV2;
%End
"""
},
# ./akonadi/selectionproxymodel.sip
"SelectionProxyModel": { #SelectionProxyModel : KSelectionProxyModel
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AgentActionManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentActionManager;
    else if (dynamic_cast<Akonadi::AgentBase*>(sipCpp))
        {
        sipType = sipType_Akonadi_AgentBase;
        if (dynamic_cast<Akonadi::PreprocessorBase*>(sipCpp))
            sipType = sipType_Akonadi_PreprocessorBase;
        else if (dynamic_cast<Akonadi::ResourceBase*>(sipCpp))
            sipType = sipType_Akonadi_ResourceBase;
        }
    else if (dynamic_cast<Akonadi::AgentFactoryBase*>(sipCpp))
        sipType = sipType_Akonadi_AgentFactoryBase;
    else if (dynamic_cast<Akonadi::AgentManager*>(sipCpp))
        sipType = sipType_Akonadi_AgentManager;
    else if (dynamic_cast<Akonadi::Control*>(sipCpp))
        sipType = sipType_Akonadi_Control;
    else if (dynamic_cast<Akonadi::EntityTreeViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeViewStateSaver;
    else if (dynamic_cast<Akonadi::Monitor*>(sipCpp))
        {
        sipType = sipType_Akonadi_Monitor;
        if (dynamic_cast<Akonadi::ChangeRecorder*>(sipCpp))
            sipType = sipType_Akonadi_ChangeRecorder;
        }
    else if (dynamic_cast<Akonadi::ServerManager*>(sipCpp))
        sipType = sipType_Akonadi_ServerManager;
    else if (dynamic_cast<Akonadi::Session*>(sipCpp))
        sipType = sipType_Akonadi_Session;
    else if (dynamic_cast<Akonadi::SpecialCollections*>(sipCpp))
        {
        sipType = sipType_Akonadi_SpecialCollections;
        if (dynamic_cast<Akonadi::SpecialMailCollections*>(sipCpp))
            sipType = sipType_Akonadi_SpecialMailCollections;
        }
    else if (dynamic_cast<Akonadi::StandardActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardActionManager;
    else if (dynamic_cast<Akonadi::StandardMailActionManager*>(sipCpp))
        sipType = sipType_Akonadi_StandardMailActionManager;
    else if (dynamic_cast<Akonadi::ResourceBaseSettings*>(sipCpp))
        {
        sipType = sipType_Akonadi_ResourceBaseSettings;
        if (dynamic_cast<Akonadi::ResourceSettings*>(sipCpp))
            sipType = sipType_Akonadi_ResourceSettings;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceCreateJob*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceCreateJob;
    else if (dynamic_cast<Akonadi::CollectionAttributesSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_CollectionAttributesSynchronizationJob;
    else if (dynamic_cast<Akonadi::PartFetcher*>(sipCpp))
        sipType = sipType_Akonadi_PartFetcher;
    else if (dynamic_cast<Akonadi::RecursiveItemFetchJob*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveItemFetchJob;
    else if (dynamic_cast<Akonadi::ResourceSynchronizationJob*>(sipCpp))
        sipType = sipType_Akonadi_ResourceSynchronizationJob;
    else if (dynamic_cast<Akonadi::Job*>(sipCpp))
        {
        sipType = sipType_Akonadi_Job;
        if (dynamic_cast<Akonadi::CollectionCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCopyJob;
        else if (dynamic_cast<Akonadi::CollectionCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionCreateJob;
        else if (dynamic_cast<Akonadi::CollectionDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionDeleteJob;
        else if (dynamic_cast<Akonadi::CollectionFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionFetchJob;
        else if (dynamic_cast<Akonadi::CollectionModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionModifyJob;
        else if (dynamic_cast<Akonadi::CollectionMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionMoveJob;
        else if (dynamic_cast<Akonadi::CollectionStatisticsJob*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsJob;
        else if (dynamic_cast<Akonadi::ItemCopyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCopyJob;
        else if (dynamic_cast<Akonadi::ItemCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemCreateJob;
        else if (dynamic_cast<Akonadi::ItemDeleteJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemDeleteJob;
        else if (dynamic_cast<Akonadi::ItemFetchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemFetchJob;
        else if (dynamic_cast<Akonadi::ItemModifyJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemModifyJob;
        else if (dynamic_cast<Akonadi::ItemMoveJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemMoveJob;
        else if (dynamic_cast<Akonadi::ItemSearchJob*>(sipCpp))
            sipType = sipType_Akonadi_ItemSearchJob;
        else if (dynamic_cast<Akonadi::ItemSync*>(sipCpp))
            sipType = sipType_Akonadi_ItemSync;
        else if (dynamic_cast<Akonadi::LinkJob*>(sipCpp))
            sipType = sipType_Akonadi_LinkJob;
        else if (dynamic_cast<Akonadi::SearchCreateJob*>(sipCpp))
            sipType = sipType_Akonadi_SearchCreateJob;
        else if (dynamic_cast<Akonadi::TransactionBeginJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionBeginJob;
        else if (dynamic_cast<Akonadi::TransactionCommitJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionCommitJob;
        else if (dynamic_cast<Akonadi::TransactionRollbackJob*>(sipCpp))
            sipType = sipType_Akonadi_TransactionRollbackJob;
        else if (dynamic_cast<Akonadi::TransactionSequence*>(sipCpp))
            {
            sipType = sipType_Akonadi_TransactionSequence;
            if (dynamic_cast<Akonadi::SpecialCollectionsRequestJob*>(sipCpp))
                {
                sipType = sipType_Akonadi_SpecialCollectionsRequestJob;
                if (dynamic_cast<Akonadi::SpecialMailCollectionsRequestJob*>(sipCpp))
                    sipType = sipType_Akonadi_SpecialMailCollectionsRequestJob;
                }
            }
        else if (dynamic_cast<Akonadi::UnlinkJob*>(sipCpp))
            sipType = sipType_Akonadi_UnlinkJob;
        }
    else if (dynamic_cast<Akonadi::ETMViewStateSaver*>(sipCpp))
        sipType = sipType_Akonadi_ETMViewStateSaver;
    else if (dynamic_cast<Akonadi::CollectionStatisticsDelegate*>(sipCpp))
        sipType = sipType_Akonadi_CollectionStatisticsDelegate;
    else if (dynamic_cast<Akonadi::AgentInstanceModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceModel;
    else if (dynamic_cast<Akonadi::AgentTypeModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeModel;
    else if (dynamic_cast<Akonadi::CollectionModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_CollectionModel;
        if (dynamic_cast<Akonadi::CollectionStatisticsModel*>(sipCpp))
            sipType = sipType_Akonadi_CollectionStatisticsModel;
        }
    else if (dynamic_cast<Akonadi::EntityTreeModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeModel;
    else if (dynamic_cast<Akonadi::MessageThreaderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_MessageThreaderProxyModel;
    else if (dynamic_cast<Akonadi::SelectionProxyModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_SelectionProxyModel;
        if (dynamic_cast<Akonadi::FavoriteCollectionsModel*>(sipCpp))
            sipType = sipType_Akonadi_FavoriteCollectionsModel;
        }
    else if (dynamic_cast<Akonadi::AgentFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_AgentFilterProxyModel;
    else if (dynamic_cast<Akonadi::CollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_CollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::EntityMimeTypeFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityMimeTypeFilterModel;
    else if (dynamic_cast<Akonadi::EntityOrderProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityOrderProxyModel;
    else if (dynamic_cast<Akonadi::StatisticsProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_StatisticsProxyModel;
    else if (dynamic_cast<Akonadi::EntityRightsFilterModel*>(sipCpp))
        sipType = sipType_Akonadi_EntityRightsFilterModel;
    else if (dynamic_cast<Akonadi::RecursiveCollectionFilterProxyModel*>(sipCpp))
        sipType = sipType_Akonadi_RecursiveCollectionFilterProxyModel;
    else if (dynamic_cast<Akonadi::ItemModel*>(sipCpp))
        {
        sipType = sipType_Akonadi_ItemModel;
        if (dynamic_cast<Akonadi::MessageModel*>(sipCpp))
            sipType = sipType_Akonadi_MessageModel;
        }
    else if (dynamic_cast<Akonadi::AgentInstanceWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentInstanceWidget;
    else if (dynamic_cast<Akonadi::AgentTypeWidget*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeWidget;
    else if (dynamic_cast<Akonadi::CollectionPropertiesPage*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesPage;
    else if (dynamic_cast<Akonadi::CollectionComboBox*>(sipCpp))
        sipType = sipType_Akonadi_CollectionComboBox;
    else if (dynamic_cast<Akonadi::AgentTypeDialog*>(sipCpp))
        sipType = sipType_Akonadi_AgentTypeDialog;
    else if (dynamic_cast<Akonadi::CollectionDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionDialog;
    else if (dynamic_cast<Akonadi::CollectionPropertiesDialog*>(sipCpp))
        sipType = sipType_Akonadi_CollectionPropertiesDialog;
    else if (dynamic_cast<Akonadi::CollectionRequester*>(sipCpp))
        sipType = sipType_Akonadi_CollectionRequester;
    else if (dynamic_cast<Akonadi::EntityListView*>(sipCpp))
        sipType = sipType_Akonadi_EntityListView;
    else if (dynamic_cast<Akonadi::CollectionView*>(sipCpp))
        sipType = sipType_Akonadi_CollectionView;
    else if (dynamic_cast<Akonadi::EntityTreeView*>(sipCpp))
        sipType = sipType_Akonadi_EntityTreeView;
    else if (dynamic_cast<Akonadi::ItemView*>(sipCpp))
        sipType = sipType_Akonadi_ItemView;
%End
"""
},
# ./akonadi/addressattribute.sip
"AddressAttribute": { #AddressAttribute : Akonadi::Attribute
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Attribute'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AddressAttribute*>(sipCpp))
        sipType = sipType_Akonadi_AddressAttribute;
    else if (dynamic_cast<Akonadi::CollectionQuotaAttribute*>(sipCpp))
        sipType = sipType_Akonadi_CollectionQuotaAttribute;
    else if (dynamic_cast<Akonadi::EntityDeletedAttribute*>(sipCpp))
        sipType = sipType_Akonadi_EntityDeletedAttribute;
    else if (dynamic_cast<Akonadi::EntityDisplayAttribute*>(sipCpp))
        sipType = sipType_Akonadi_EntityDisplayAttribute;
    else if (dynamic_cast<Akonadi::EntityHiddenAttribute*>(sipCpp))
        sipType = sipType_Akonadi_EntityHiddenAttribute;
    else if (dynamic_cast<Akonadi::IndexPolicyAttribute*>(sipCpp))
        sipType = sipType_Akonadi_IndexPolicyAttribute;
    else if (dynamic_cast<Akonadi::MessageFolderAttribute*>(sipCpp))
        sipType = sipType_Akonadi_MessageFolderAttribute;
    else if (dynamic_cast<Akonadi::MessageThreadingAttribute*>(sipCpp))
        sipType = sipType_Akonadi_MessageThreadingAttribute;
    else if (dynamic_cast<Akonadi::PersistentSearchAttribute*>(sipCpp))
        sipType = sipType_Akonadi_PersistentSearchAttribute;
%End
"""
},
# ./akonadi/attribute.sip
"Attribute": { #Attribute /Abstract/
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Attribute'
    sipType = NULL;

    if (dynamic_cast<Akonadi::AddressAttribute*>(sipCpp))
        sipType = sipType_Akonadi_AddressAttribute;
    else if (dynamic_cast<Akonadi::CollectionQuotaAttribute*>(sipCpp))
        sipType = sipType_Akonadi_CollectionQuotaAttribute;
    else if (dynamic_cast<Akonadi::EntityDisplayAttribute*>(sipCpp))
        sipType = sipType_Akonadi_EntityDisplayAttribute;
    else if (dynamic_cast<Akonadi::EntityHiddenAttribute*>(sipCpp))
        sipType = sipType_Akonadi_EntityHiddenAttribute;
    else if (dynamic_cast<Akonadi::MessageFolderAttribute*>(sipCpp))
        sipType = sipType_Akonadi_MessageFolderAttribute;
    else if (dynamic_cast<Akonadi::MessageThreadingAttribute*>(sipCpp))
        sipType = sipType_Akonadi_MessageThreadingAttribute;
%End
"""
},
# ./khtml/dom_misc.sip
"DomShared": { #DomShared
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'DomShared'
    sipType = NULL;

    if (dynamic_cast<DOM::CustomNodeFilter*>(sipCpp))
        sipType = sipType_DOM_CustomNodeFilter;
    else if (dynamic_cast<DOM::EventListener*>(sipCpp))
        sipType = sipType_DOM_EventListener;
%End
"""
},
# ./khtml/khtml_part.sip
"KHTMLPart": { #KHTMLPart : KParts::ReadOnlyPart
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KHTMLPart*>(sipCpp))
        sipType = sipType_KHTMLPart;
    else if (dynamic_cast<KHTMLView*>(sipCpp))
        sipType = sipType_KHTMLView;
%End
"""
},
# ./khtml/dom_element.sip
"Attr": { #Attr : DOM::Node
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Node'
    sipType = NULL;

    if (dynamic_cast<DOM::Attr*>(sipCpp))
        sipType = sipType_DOM_Attr;
    else if (dynamic_cast<DOM::CharacterData*>(sipCpp))
        {
        sipType = sipType_DOM_CharacterData;
        if (dynamic_cast<DOM::Comment*>(sipCpp))
            sipType = sipType_DOM_Comment;
        else if (dynamic_cast<DOM::Text*>(sipCpp))
            {
            sipType = sipType_DOM_Text;
            if (dynamic_cast<DOM::CDATASection*>(sipCpp))
                sipType = sipType_DOM_CDATASection;
            }
        }
    else if (dynamic_cast<DOM::Document*>(sipCpp))
        {
        sipType = sipType_DOM_Document;
        if (dynamic_cast<DOM::HTMLDocument*>(sipCpp))
            sipType = sipType_DOM_HTMLDocument;
        }
    else if (dynamic_cast<DOM::DocumentFragment*>(sipCpp))
        sipType = sipType_DOM_DocumentFragment;
    else if (dynamic_cast<DOM::DocumentType*>(sipCpp))
        sipType = sipType_DOM_DocumentType;
    else if (dynamic_cast<DOM::Element*>(sipCpp))
        {
        sipType = sipType_DOM_Element;
        if (dynamic_cast<DOM::HTMLElement*>(sipCpp))
            {
            sipType = sipType_DOM_HTMLElement;
            if (dynamic_cast<DOM::HTMLAnchorElement*>(sipCpp))
                sipType = sipType_DOM_HTMLAnchorElement;
            else if (dynamic_cast<DOM::HTMLAppletElement*>(sipCpp))
                sipType = sipType_DOM_HTMLAppletElement;
            else if (dynamic_cast<DOM::HTMLAreaElement*>(sipCpp))
                sipType = sipType_DOM_HTMLAreaElement;
            else if (dynamic_cast<DOM::HTMLBRElement*>(sipCpp))
                sipType = sipType_DOM_HTMLBRElement;
            else if (dynamic_cast<DOM::HTMLBaseElement*>(sipCpp))
                sipType = sipType_DOM_HTMLBaseElement;
            else if (dynamic_cast<DOM::HTMLBaseFontElement*>(sipCpp))
                sipType = sipType_DOM_HTMLBaseFontElement;
            else if (dynamic_cast<DOM::HTMLBlockquoteElement*>(sipCpp))
                sipType = sipType_DOM_HTMLBlockquoteElement;
            else if (dynamic_cast<DOM::HTMLBodyElement*>(sipCpp))
                sipType = sipType_DOM_HTMLBodyElement;
            else if (dynamic_cast<DOM::HTMLButtonElement*>(sipCpp))
                sipType = sipType_DOM_HTMLButtonElement;
            else if (dynamic_cast<DOM::HTMLDListElement*>(sipCpp))
                sipType = sipType_DOM_HTMLDListElement;
            else if (dynamic_cast<DOM::HTMLDirectoryElement*>(sipCpp))
                sipType = sipType_DOM_HTMLDirectoryElement;
            else if (dynamic_cast<DOM::HTMLDivElement*>(sipCpp))
                sipType = sipType_DOM_HTMLDivElement;
            else if (dynamic_cast<DOM::HTMLFieldSetElement*>(sipCpp))
                sipType = sipType_DOM_HTMLFieldSetElement;
            else if (dynamic_cast<DOM::HTMLFontElement*>(sipCpp))
                sipType = sipType_DOM_HTMLFontElement;
            else if (dynamic_cast<DOM::HTMLFormElement*>(sipCpp))
                sipType = sipType_DOM_HTMLFormElement;
            else if (dynamic_cast<DOM::HTMLFrameElement*>(sipCpp))
                sipType = sipType_DOM_HTMLFrameElement;
            else if (dynamic_cast<DOM::HTMLFrameSetElement*>(sipCpp))
                sipType = sipType_DOM_HTMLFrameSetElement;
            else if (dynamic_cast<DOM::HTMLHRElement*>(sipCpp))
                sipType = sipType_DOM_HTMLHRElement;
            else if (dynamic_cast<DOM::HTMLHeadElement*>(sipCpp))
                sipType = sipType_DOM_HTMLHeadElement;
            else if (dynamic_cast<DOM::HTMLHeadingElement*>(sipCpp))
                sipType = sipType_DOM_HTMLHeadingElement;
            else if (dynamic_cast<DOM::HTMLHtmlElement*>(sipCpp))
                sipType = sipType_DOM_HTMLHtmlElement;
            else if (dynamic_cast<DOM::HTMLIFrameElement*>(sipCpp))
                sipType = sipType_DOM_HTMLIFrameElement;
            else if (dynamic_cast<DOM::HTMLImageElement*>(sipCpp))
                sipType = sipType_DOM_HTMLImageElement;
            else if (dynamic_cast<DOM::HTMLInputElement*>(sipCpp))
                sipType = sipType_DOM_HTMLInputElement;
            else if (dynamic_cast<DOM::HTMLIsIndexElement*>(sipCpp))
                sipType = sipType_DOM_HTMLIsIndexElement;
            else if (dynamic_cast<DOM::HTMLLIElement*>(sipCpp))
                sipType = sipType_DOM_HTMLLIElement;
            else if (dynamic_cast<DOM::HTMLLabelElement*>(sipCpp))
                sipType = sipType_DOM_HTMLLabelElement;
            else if (dynamic_cast<DOM::HTMLLayerElement*>(sipCpp))
                sipType = sipType_DOM_HTMLLayerElement;
            else if (dynamic_cast<DOM::HTMLLegendElement*>(sipCpp))
                sipType = sipType_DOM_HTMLLegendElement;
            else if (dynamic_cast<DOM::HTMLLinkElement*>(sipCpp))
                sipType = sipType_DOM_HTMLLinkElement;
            else if (dynamic_cast<DOM::HTMLMapElement*>(sipCpp))
                sipType = sipType_DOM_HTMLMapElement;
            else if (dynamic_cast<DOM::HTMLMenuElement*>(sipCpp))
                sipType = sipType_DOM_HTMLMenuElement;
            else if (dynamic_cast<DOM::HTMLMetaElement*>(sipCpp))
                sipType = sipType_DOM_HTMLMetaElement;
            else if (dynamic_cast<DOM::HTMLModElement*>(sipCpp))
                sipType = sipType_DOM_HTMLModElement;
            else if (dynamic_cast<DOM::HTMLOListElement*>(sipCpp))
                sipType = sipType_DOM_HTMLOListElement;
            else if (dynamic_cast<DOM::HTMLObjectElement*>(sipCpp))
                sipType = sipType_DOM_HTMLObjectElement;
            else if (dynamic_cast<DOM::HTMLOptGroupElement*>(sipCpp))
                sipType = sipType_DOM_HTMLOptGroupElement;
            else if (dynamic_cast<DOM::HTMLOptionElement*>(sipCpp))
                sipType = sipType_DOM_HTMLOptionElement;
            else if (dynamic_cast<DOM::HTMLParagraphElement*>(sipCpp))
                sipType = sipType_DOM_HTMLParagraphElement;
            else if (dynamic_cast<DOM::HTMLParamElement*>(sipCpp))
                sipType = sipType_DOM_HTMLParamElement;
            else if (dynamic_cast<DOM::HTMLPreElement*>(sipCpp))
                sipType = sipType_DOM_HTMLPreElement;
            else if (dynamic_cast<DOM::HTMLQuoteElement*>(sipCpp))
                sipType = sipType_DOM_HTMLQuoteElement;
            else if (dynamic_cast<DOM::HTMLScriptElement*>(sipCpp))
                sipType = sipType_DOM_HTMLScriptElement;
            else if (dynamic_cast<DOM::HTMLSelectElement*>(sipCpp))
                sipType = sipType_DOM_HTMLSelectElement;
            else if (dynamic_cast<DOM::HTMLStyleElement*>(sipCpp))
                sipType = sipType_DOM_HTMLStyleElement;
            else if (dynamic_cast<DOM::HTMLTableCaptionElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableCaptionElement;
            else if (dynamic_cast<DOM::HTMLTableCellElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableCellElement;
            else if (dynamic_cast<DOM::HTMLTableColElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableColElement;
            else if (dynamic_cast<DOM::HTMLTableElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableElement;
            else if (dynamic_cast<DOM::HTMLTableRowElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableRowElement;
            else if (dynamic_cast<DOM::HTMLTableSectionElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTableSectionElement;
            else if (dynamic_cast<DOM::HTMLTextAreaElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTextAreaElement;
            else if (dynamic_cast<DOM::HTMLTitleElement*>(sipCpp))
                sipType = sipType_DOM_HTMLTitleElement;
            else if (dynamic_cast<DOM::HTMLUListElement*>(sipCpp))
                sipType = sipType_DOM_HTMLUListElement;
            }
        }
    else if (dynamic_cast<DOM::Entity*>(sipCpp))
        sipType = sipType_DOM_Entity;
    else if (dynamic_cast<DOM::EntityReference*>(sipCpp))
        sipType = sipType_DOM_EntityReference;
    else if (dynamic_cast<DOM::Notation*>(sipCpp))
        sipType = sipType_DOM_Notation;
    else if (dynamic_cast<DOM::ProcessingInstruction*>(sipCpp))
        sipType = sipType_DOM_ProcessingInstruction;
%End
"""
},
# ./khtml/dom2_events.sip
"MutationEvent": { #MutationEvent : DOM::Event
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Event'
    sipType = NULL;

    if (dynamic_cast<DOM::MutationEvent*>(sipCpp))
        sipType = sipType_DOM_MutationEvent;
    else if (dynamic_cast<DOM::UIEvent*>(sipCpp))
        {
        sipType = sipType_DOM_UIEvent;
        if (dynamic_cast<DOM::KeyboardEvent*>(sipCpp))
            sipType = sipType_DOM_KeyboardEvent;
        else if (dynamic_cast<DOM::MouseEvent*>(sipCpp))
            sipType = sipType_DOM_MouseEvent;
        else if (dynamic_cast<DOM::TextEvent*>(sipCpp))
            sipType = sipType_DOM_TextEvent;
        }
%End
"""
},
# ./kparts/event.sip
"Event": { #Event : QEvent
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QEvent'
    sipType = NULL;

    if (dynamic_cast<KParts::Event*>(sipCpp))
        {
        sipType = sipType_KParts_Event;
        if (dynamic_cast<KParts::GUIActivateEvent*>(sipCpp))
            sipType = sipType_KParts_GUIActivateEvent;
        else if (dynamic_cast<KParts::OpenUrlEvent*>(sipCpp))
            sipType = sipType_KParts_OpenUrlEvent;
        else if (dynamic_cast<KParts::PartActivateEvent*>(sipCpp))
            sipType = sipType_KParts_PartActivateEvent;
        else if (dynamic_cast<KParts::PartSelectEvent*>(sipCpp))
            sipType = sipType_KParts_PartSelectEvent;
        }
%End
"""
},
# ./kparts/browserextension.sip
"BrowserExtension": { #BrowserExtension : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KParts::BrowserExtension*>(sipCpp))
        sipType = sipType_KParts_BrowserExtension;
    else if (dynamic_cast<KParts::BrowserHostExtension*>(sipCpp))
        sipType = sipType_KParts_BrowserHostExtension;
    else if (dynamic_cast<KParts::BrowserInterface*>(sipCpp))
        sipType = sipType_KParts_BrowserInterface;
    else if (dynamic_cast<KParts::FileInfoExtension*>(sipCpp))
        sipType = sipType_KParts_FileInfoExtension;
    else if (dynamic_cast<KParts::HistoryProvider*>(sipCpp))
        sipType = sipType_KParts_HistoryProvider;
    else if (dynamic_cast<KParts::HtmlExtension*>(sipCpp))
        sipType = sipType_KParts_HtmlExtension;
    else if (dynamic_cast<KParts::LiveConnectExtension*>(sipCpp))
        sipType = sipType_KParts_LiveConnectExtension;
    else if (dynamic_cast<KParts::Part*>(sipCpp))
        {
        sipType = sipType_KParts_Part;
        if (dynamic_cast<KParts::ReadOnlyPart*>(sipCpp))
            {
            sipType = sipType_KParts_ReadOnlyPart;
            if (dynamic_cast<KParts::ReadWritePart*>(sipCpp))
                sipType = sipType_KParts_ReadWritePart;
            }
        }
    else if (dynamic_cast<KParts::PartManager*>(sipCpp))
        sipType = sipType_KParts_PartManager;
    else if (dynamic_cast<KParts::Plugin*>(sipCpp))
        sipType = sipType_KParts_Plugin;
    else if (dynamic_cast<KParts::ScriptableExtension*>(sipCpp))
        sipType = sipType_KParts_ScriptableExtension;
    else if (dynamic_cast<KParts::StatusBarExtension*>(sipCpp))
        sipType = sipType_KParts_StatusBarExtension;
    else if (dynamic_cast<KParts::TextExtension*>(sipCpp))
        sipType = sipType_KParts_TextExtension;
    else if (dynamic_cast<KParts::BrowserRun*>(sipCpp))
        sipType = sipType_KParts_BrowserRun;
    else if (dynamic_cast<KParts::MainWindow*>(sipCpp))
        sipType = sipType_KParts_MainWindow;
%End
"""
},
# ./kparts/factory.sip
"Factory": { #Factory : KLibFactory
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Factory'
    sipType = NULL;

    if (dynamic_cast<KParts::Factory*>(sipCpp))
        sipType = sipType_KParts_Factory;
%End
"""
},
# ./phonon/medianode.sip
"MediaNode": { #MediaNode /NoDefaultCtors/
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'MediaNode'
    sipType = NULL;

    if (dynamic_cast<Phonon::AbstractAudioOutput*>(sipCpp))
        {
        sipType = sipType_Phonon_AbstractAudioOutput;
        if (dynamic_cast<Phonon::AudioDataOutput*>(sipCpp))
            sipType = sipType_Phonon_AudioDataOutput;
        }
    else if (dynamic_cast<Phonon::AbstractVideoOutput*>(sipCpp))
        {
        sipType = sipType_Phonon_AbstractVideoOutput;
        if (dynamic_cast<Phonon::VideoWidget*>(sipCpp))
            sipType = sipType_Phonon_VideoWidget;
        }
    else if (dynamic_cast<Phonon::AudioOutput*>(sipCpp))
        sipType = sipType_Phonon_AudioOutput;
    else if (dynamic_cast<Phonon::Effect*>(sipCpp))
        {
        sipType = sipType_Phonon_Effect;
        if (dynamic_cast<Phonon::VolumeFaderEffect*>(sipCpp))
            sipType = sipType_Phonon_VolumeFaderEffect;
        }
    else if (dynamic_cast<Phonon::MediaObject*>(sipCpp))
        sipType = sipType_Phonon_MediaObject;
%End
"""
},
# ./phonon/abstractvideodataoutput.sip
"QSet<Phonon::Experimental::VideoFrame2::Format>": { #QSet<Phonon::Experimental::VideoFrame2::Format>
"code":
"""
%TypeHeaderCode
#include <qset.h>
#include <phonon/experimental/abstractvideodataoutput.h>
%End
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    QSet<Phonon::Experimental::VideoFrame2::Format> set = *sipCpp;
    int i = 0;
    foreach (Phonon::Experimental::VideoFrame2::Format value, set)
    {
        PyObject *obj = PyInt_FromLong ((long) value);
        if (obj == NULL || PyList_SET_ITEM (l, i, obj) < 0)
        {
            Py_DECREF(l);

            if (obj)
                Py_DECREF(obj);

            return NULL;
        }

        Py_DECREF(obj);
        i++;
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    QSet<Phonon::Experimental::VideoFrame2::Format> *qs = new QSet<Phonon::Experimental::VideoFrame2::Format>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        Phonon::Experimental::VideoFrame2::Format t = (Phonon::Experimental::VideoFrame2::Format)PyInt_AS_LONG (PyList_GET_ITEM (sipPy, i));
        *qs << t;

    }

    *sipCppPtr = qs;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./phonon/pulsesupport.sip
"PulseSupport": { #PulseSupport : QObject
"code":
"""
%TypeHeaderCode
#include <phonon/pulsesupport.h>
#include <phonon/phononnamespace.h>
%End
"""
},
# ./phonon/mrl.sip
"Mrl": { #Mrl : QUrl
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QUrl'
    sipType = NULL;

    if (dynamic_cast<Phonon::Mrl*>(sipCpp))
        sipType = sipType_Phonon_Mrl;
%End
"""
},
# ./phonon/abstractaudiodataoutput.sip
"QSet<Phonon::Experimental::AudioFormat>": { #QSet<Phonon::Experimental::AudioFormat>
"code":
"""
%TypeHeaderCode
#include <qset.h>
#include <phonon/experimental/abstractaudiodataoutput.h>
%End
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    QSet<Phonon::Experimental::AudioFormat> set = *sipCpp;
    int i = 0;
    foreach (Phonon::Experimental::AudioFormat value, set)
    {
        PyObject *obj = PyInt_FromLong ((long) value);
        if (obj == NULL || PyList_SET_ITEM (l, i, obj) < 0)
        {
            Py_DECREF(l);

            if (obj)
                Py_DECREF(obj);

            return NULL;
        }

        Py_DECREF(obj);
        i++;
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    QSet<Phonon::Experimental::AudioFormat> *qs = new QSet<Phonon::Experimental::AudioFormat>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        Phonon::Experimental::AudioFormat t = (Phonon::Experimental::AudioFormat)PyInt_AS_LONG (PyList_GET_ITEM (sipPy, i));
        *qs << t;

    }

    *sipCppPtr = qs;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./phonon/videowidget.sip
"VideoWidget": { #VideoWidget : QWidget, Phonon::AbstractVideoOutput
"code":
"""
%TypeHeaderCode
#include <phonon/videowidget.h>
#include <phonon/abstractvideooutput.h>
%End
"""
},
# ./phonon/objectdescription.sip
"QList<Phonon::ObjectDescription>": { #QList<Phonon::ObjectDescription>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        DNSSD::RemoteService::Ptr *t = new Phonon::ObjectDescription (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t->data(), sipClass_DNSSD_RemoteService, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_DNSSD_RemoteService, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<DNSSD::RemoteService::Ptr> *ql = new QList<DNSSD::RemoteService::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        DNSSD::RemoteService *t = reinterpret_cast<DNSSD::RemoteService *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_DNSSD_RemoteService, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_DNSSD_RemoteService, state);

            delete ql;
            return 0;
        }

        DNSSD::RemoteService::Ptr *tptr = new DNSSD::RemoteService::Ptr (t);

        ql->append(*tptr);

        sipReleaseInstance(t, sipClass_DNSSD_RemoteService, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./nepomuk/ktagcloudwidget.sip
"KTagCloudWidget": { #KTagCloudWidget : QWidget
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QWidget'
    sipType = NULL;

    if (dynamic_cast<KTagCloudWidget*>(sipCpp))
        {
        sipType = sipType_KTagCloudWidget;
        if (dynamic_cast<Nepomuk::TagCloud*>(sipCpp))
            sipType = sipType_Nepomuk_TagCloud;
        }
    else if (dynamic_cast<KTagDisplayWidget*>(sipCpp))
        sipType = sipType_KTagDisplayWidget;
    else if (dynamic_cast<Nepomuk::TagWidget*>(sipCpp))
        sipType = sipType_Nepomuk_TagWidget;
%End
"""
},
# ./nepomuk/entity.sip
"Entity": { #Entity
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Entity'
    sipType = NULL;

    if (dynamic_cast<Nepomuk::Types::Class*>(sipCpp))
        sipType = sipType_Nepomuk_Types_Class;
    else if (dynamic_cast<Nepomuk::Types::Ontology*>(sipCpp))
        sipType = sipType_Nepomuk_Types_Ontology;
    else if (dynamic_cast<Nepomuk::Types::Property*>(sipCpp))
        sipType = sipType_Nepomuk_Types_Property;
%End
"""
},
# ./nepomuk/resource.sip
"Resource": { #Resource
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Resource'
    sipType = NULL;

    if (dynamic_cast<Nepomuk::File*>(sipCpp))
        sipType = sipType_Nepomuk_File;
    else if (dynamic_cast<Nepomuk::Tag*>(sipCpp))
        sipType = sipType_Nepomuk_Tag;
    else if (dynamic_cast<Nepomuk::Thing*>(sipCpp))
        sipType = sipType_Nepomuk_Thing;
%End
"""
},
# ./soprano/queryresultiterator.sip
"QueryResultIterator": { #QueryResultIterator
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QueryResultIterator'
    sipType = NULL;

    if (dynamic_cast<Soprano::Client::DBusQueryResultIterator*>(sipCpp))
        sipType = sipType_Soprano_Client_DBusQueryResultIterator;
%End
"""
},
# ./soprano/statementiterator.sip
"StatementIterator": { #StatementIterator
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'StatementIterator'
    sipType = NULL;

    if (dynamic_cast<Soprano::Client::DBusStatementIterator*>(sipCpp))
        sipType = sipType_Soprano_Client_DBusStatementIterator;
    else if (dynamic_cast<Soprano::Util::SimpleStatementIterator*>(sipCpp))
        sipType = sipType_Soprano_Util_SimpleStatementIterator;
%End
"""
},
# ./soprano/plugin.sip
"Plugin": { #Plugin
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Plugin'
    sipType = NULL;

    if (dynamic_cast<Soprano::Backend*>(sipCpp))
        sipType = sipType_Soprano_Backend;
    else if (dynamic_cast<Soprano::Parser*>(sipCpp))
        sipType = sipType_Soprano_Parser;
    else if (dynamic_cast<Soprano::Serializer*>(sipCpp))
        sipType = sipType_Soprano_Serializer;
%End
"""
},
# ./soprano/error.sip
"Error": { #Error
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'Error'
    sipType = NULL;

    if (dynamic_cast<Soprano::Error::ParserError*>(sipCpp))
        sipType = sipType_Soprano_Error_ParserError;
%End
"""
},
# ./soprano/pluginmanager.sip
"QList<const": { #QList<const Soprano::Backend*>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        Soprano::Backend* t = const_cast<Soprano::Backend*>(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromInstance(t, sipClass_Soprano_Backend, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Backend, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<const Soprano::Backend*> *ql = new QList<const Soprano::Backend*>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        const Soprano::Backend*t = reinterpret_cast<const Soprano::Backend*>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Backend, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(const_cast<Soprano::Backend*>(t), sipClass_Soprano_Backend, state);

            delete ql;
            return 0;
        }
        ql->append(t);

        sipReleaseInstance(const_cast<Soprano::Backend*>(t), sipClass_Soprano_Backend, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
"QList<const": { #QList<const Soprano::Parser*>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        Soprano::Parser* t = const_cast<Soprano::Parser*>(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromInstance(t, sipClass_Soprano_Parser, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Parser, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<const Soprano::Parser*> *ql = new QList<const Soprano::Parser*>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        const Soprano::Parser*t = reinterpret_cast<const Soprano::Parser*>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Parser, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(const_cast<Soprano::Parser*>(t), sipClass_Soprano_Parser, state);

            delete ql;
            return 0;
        }
        ql->append(t);

        sipReleaseInstance(const_cast<Soprano::Parser*>(t), sipClass_Soprano_Parser, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
"QList<const": { #QList<const Soprano::Serializer*>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        Soprano::Serializer* t = const_cast<Soprano::Serializer*>(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromInstance(t, sipClass_Soprano_Serializer, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Serializer, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<const Soprano::Serializer*> *ql = new QList<const Soprano::Serializer*>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        const Soprano::Serializer*t = reinterpret_cast<const Soprano::Serializer*>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_Soprano_Serializer, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(const_cast<Soprano::Serializer*>(t), sipClass_Soprano_Serializer, state);

            delete ql;
            return 0;
        }
        ql->append(t);

        sipReleaseInstance(const_cast<Soprano::Serializer*>(t), sipClass_Soprano_Serializer, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./soprano/model.sip
"Model": { #Model : QObject, Soprano::Error::ErrorCache
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Soprano::Client::DBusClient*>(sipCpp))
        sipType = sipType_Soprano_Client_DBusClient;
    else if (dynamic_cast<Soprano::Client::LocalSocketClient*>(sipCpp))
        sipType = sipType_Soprano_Client_LocalSocketClient;
    else if (dynamic_cast<Soprano::Client::TcpClient*>(sipCpp))
        sipType = sipType_Soprano_Client_TcpClient;
    else if (dynamic_cast<Soprano::Model*>(sipCpp))
        {
        sipType = sipType_Soprano_Model;
        if (dynamic_cast<Soprano::Client::SparqlModel*>(sipCpp))
            sipType = sipType_Soprano_Client_SparqlModel;
        else if (dynamic_cast<Soprano::FilterModel*>(sipCpp))
            {
            sipType = sipType_Soprano_FilterModel;
            if (dynamic_cast<Soprano::Inference::InferenceModel*>(sipCpp))
                sipType = sipType_Soprano_Inference_InferenceModel;
            else if (dynamic_cast<Soprano::NRLModel*>(sipCpp))
                sipType = sipType_Soprano_NRLModel;
            else if (dynamic_cast<Soprano::Server::DBusExportModel*>(sipCpp))
                sipType = sipType_Soprano_Server_DBusExportModel;
            else if (dynamic_cast<Soprano::Util::AsyncModel*>(sipCpp))
                sipType = sipType_Soprano_Util_AsyncModel;
            else if (dynamic_cast<Soprano::Util::MutexModel*>(sipCpp))
                sipType = sipType_Soprano_Util_MutexModel;
            else if (dynamic_cast<Soprano::Util::SignalCacheModel*>(sipCpp))
                sipType = sipType_Soprano_Util_SignalCacheModel;
            }
        else if (dynamic_cast<Soprano::StorageModel*>(sipCpp))
            {
            sipType = sipType_Soprano_StorageModel;
            if (dynamic_cast<Soprano::Client::DBusModel*>(sipCpp))
                sipType = sipType_Soprano_Client_DBusModel;
            }
        else if (dynamic_cast<Soprano::Util::DummyModel*>(sipCpp))
            sipType = sipType_Soprano_Util_DummyModel;
        }
    else if (dynamic_cast<Soprano::PluginManager*>(sipCpp))
        sipType = sipType_Soprano_PluginManager;
    else if (dynamic_cast<Soprano::Server::DBusExportIterator*>(sipCpp))
        sipType = sipType_Soprano_Server_DBusExportIterator;
    else if (dynamic_cast<Soprano::Server::ServerCore*>(sipCpp))
        sipType = sipType_Soprano_Server_ServerCore;
    else if (dynamic_cast<Soprano::Util::AsyncQuery*>(sipCpp))
        sipType = sipType_Soprano_Util_AsyncQuery;
    else if (dynamic_cast<Soprano::Util::AsyncResult*>(sipCpp))
        sipType = sipType_Soprano_Util_AsyncResult;
%End
"""
},
# ./soprano/tcpclient.sip
"TcpClient": { #TcpClient : QObject, Soprano::Error::ErrorCache
"code":
"""
%TypeHeaderCode
#include <soprano/tcpclient.h>
#include <soprano/servercore.h>
%End
"""
},
# ./soprano/nodeiterator.sip
"NodeIterator": { #NodeIterator
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'NodeIterator'
    sipType = NULL;

    if (dynamic_cast<Soprano::Client::DBusNodeIterator*>(sipCpp))
        sipType = sipType_Soprano_Client_DBusNodeIterator;
    else if (dynamic_cast<Soprano::Util::SimpleNodeIterator*>(sipCpp))
        sipType = sipType_Soprano_Util_SimpleNodeIterator;
%End
"""
},
# ./plasma/animation.sip
"Animation": { #Animation : QAbstractAnimation
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Plasma::ConfigLoader*>(sipCpp))
        sipType = sipType_Plasma_ConfigLoader;
    else if (dynamic_cast<Plasma::AccessAppletJob*>(sipCpp))
        sipType = sipType_Plasma_AccessAppletJob;
    else if (dynamic_cast<Plasma::ServiceAccessJob*>(sipCpp))
        sipType = sipType_Plasma_ServiceAccessJob;
    else if (dynamic_cast<Plasma::ServiceJob*>(sipCpp))
        sipType = sipType_Plasma_ServiceJob;
    else if (dynamic_cast<Plasma::AbstractDialogManager*>(sipCpp))
        sipType = sipType_Plasma_AbstractDialogManager;
    else if (dynamic_cast<Plasma::AbstractRunner*>(sipCpp))
        sipType = sipType_Plasma_AbstractRunner;
    else if (dynamic_cast<Plasma::AccessManager*>(sipCpp))
        sipType = sipType_Plasma_AccessManager;
    else if (dynamic_cast<Plasma::AnimationDriver*>(sipCpp))
        sipType = sipType_Plasma_AnimationDriver;
    else if (dynamic_cast<Plasma::Animator*>(sipCpp))
        sipType = sipType_Plasma_Animator;
    else if (dynamic_cast<Plasma::AuthorizationManager*>(sipCpp))
        sipType = sipType_Plasma_AuthorizationManager;
    else if (dynamic_cast<Plasma::AuthorizationRule*>(sipCpp))
        sipType = sipType_Plasma_AuthorizationRule;
    else if (dynamic_cast<Plasma::ClientPinRequest*>(sipCpp))
        sipType = sipType_Plasma_ClientPinRequest;
    else if (dynamic_cast<Plasma::ContainmentActions*>(sipCpp))
        sipType = sipType_Plasma_ContainmentActions;
    else if (dynamic_cast<Plasma::Context*>(sipCpp))
        sipType = sipType_Plasma_Context;
    else if (dynamic_cast<Plasma::DataContainer*>(sipCpp))
        sipType = sipType_Plasma_DataContainer;
    else if (dynamic_cast<Plasma::DataEngine*>(sipCpp))
        sipType = sipType_Plasma_DataEngine;
    else if (dynamic_cast<Plasma::DataEngineManager*>(sipCpp))
        sipType = sipType_Plasma_DataEngineManager;
    else if (dynamic_cast<Plasma::PackageStructure*>(sipCpp))
        sipType = sipType_Plasma_PackageStructure;
    else if (dynamic_cast<Plasma::RunnerContext*>(sipCpp))
        sipType = sipType_Plasma_RunnerContext;
    else if (dynamic_cast<Plasma::RunnerManager*>(sipCpp))
        sipType = sipType_Plasma_RunnerManager;
    else if (dynamic_cast<Plasma::ScriptEngine*>(sipCpp))
        {
        sipType = sipType_Plasma_ScriptEngine;
        if (dynamic_cast<Plasma::AppletScript*>(sipCpp))
            sipType = sipType_Plasma_AppletScript;
        else if (dynamic_cast<Plasma::DataEngineScript*>(sipCpp))
            sipType = sipType_Plasma_DataEngineScript;
        else if (dynamic_cast<Plasma::RunnerScript*>(sipCpp))
            sipType = sipType_Plasma_RunnerScript;
        else if (dynamic_cast<Plasma::WallpaperScript*>(sipCpp))
            sipType = sipType_Plasma_WallpaperScript;
        }
    else if (dynamic_cast<Plasma::Service*>(sipCpp))
        sipType = sipType_Plasma_Service;
    else if (dynamic_cast<Plasma::Svg*>(sipCpp))
        {
        sipType = sipType_Plasma_Svg;
        if (dynamic_cast<Plasma::FrameSvg*>(sipCpp))
            sipType = sipType_Plasma_FrameSvg;
        }
    else if (dynamic_cast<Plasma::Theme*>(sipCpp))
        sipType = sipType_Plasma_Theme;
    else if (dynamic_cast<Plasma::ToolTipManager*>(sipCpp))
        sipType = sipType_Plasma_ToolTipManager;
    else if (dynamic_cast<Plasma::Wallpaper*>(sipCpp))
        sipType = sipType_Plasma_Wallpaper;
    else if (dynamic_cast<Plasma::Animation*>(sipCpp))
        sipType = sipType_Plasma_Animation;
    else if (dynamic_cast<Plasma::Delegate*>(sipCpp))
        sipType = sipType_Plasma_Delegate;
    else if (dynamic_cast<Plasma::Corona*>(sipCpp))
        sipType = sipType_Plasma_Corona;
    else if (dynamic_cast<Plasma::AbstractToolBox*>(sipCpp))
        sipType = sipType_Plasma_AbstractToolBox;
    else if (dynamic_cast<Plasma::Applet*>(sipCpp))
        {
        sipType = sipType_Plasma_Applet;
        if (dynamic_cast<Plasma::AppletProtectedThunk*>(sipCpp))
            sipType = sipType_Plasma_AppletProtectedThunk;
        else if (dynamic_cast<Plasma::Containment*>(sipCpp))
            sipType = sipType_Plasma_Containment;
        else if (dynamic_cast<Plasma::GLApplet*>(sipCpp))
            sipType = sipType_Plasma_GLApplet;
        else if (dynamic_cast<Plasma::PopupApplet*>(sipCpp))
            sipType = sipType_Plasma_PopupApplet;
        }
    else if (dynamic_cast<Plasma::BusyWidget*>(sipCpp))
        sipType = sipType_Plasma_BusyWidget;
    else if (dynamic_cast<Plasma::DeclarativeWidget*>(sipCpp))
        sipType = sipType_Plasma_DeclarativeWidget;
    else if (dynamic_cast<Plasma::Extender*>(sipCpp))
        sipType = sipType_Plasma_Extender;
    else if (dynamic_cast<Plasma::ExtenderItem*>(sipCpp))
        {
        sipType = sipType_Plasma_ExtenderItem;
        if (dynamic_cast<Plasma::ExtenderGroup*>(sipCpp))
            sipType = sipType_Plasma_ExtenderGroup;
        }
    else if (dynamic_cast<Plasma::FlashingLabel*>(sipCpp))
        sipType = sipType_Plasma_FlashingLabel;
    else if (dynamic_cast<Plasma::Frame*>(sipCpp))
        sipType = sipType_Plasma_Frame;
    else if (dynamic_cast<Plasma::IconWidget*>(sipCpp))
        sipType = sipType_Plasma_IconWidget;
    else if (dynamic_cast<Plasma::ItemBackground*>(sipCpp))
        sipType = sipType_Plasma_ItemBackground;
    else if (dynamic_cast<Plasma::Meter*>(sipCpp))
        sipType = sipType_Plasma_Meter;
    else if (dynamic_cast<Plasma::ScrollWidget*>(sipCpp))
        sipType = sipType_Plasma_ScrollWidget;
    else if (dynamic_cast<Plasma::Separator*>(sipCpp))
        sipType = sipType_Plasma_Separator;
    else if (dynamic_cast<Plasma::SignalPlotter*>(sipCpp))
        sipType = sipType_Plasma_SignalPlotter;
    else if (dynamic_cast<Plasma::SvgWidget*>(sipCpp))
        sipType = sipType_Plasma_SvgWidget;
    else if (dynamic_cast<Plasma::TabBar*>(sipCpp))
        sipType = sipType_Plasma_TabBar;
    else if (dynamic_cast<Plasma::WebView*>(sipCpp))
        sipType = sipType_Plasma_WebView;
    else if (dynamic_cast<Plasma::CheckBox*>(sipCpp))
        sipType = sipType_Plasma_CheckBox;
    else if (dynamic_cast<Plasma::ComboBox*>(sipCpp))
        sipType = sipType_Plasma_ComboBox;
    else if (dynamic_cast<Plasma::GroupBox*>(sipCpp))
        sipType = sipType_Plasma_GroupBox;
    else if (dynamic_cast<Plasma::Label*>(sipCpp))
        sipType = sipType_Plasma_Label;
    else if (dynamic_cast<Plasma::LineEdit*>(sipCpp))
        sipType = sipType_Plasma_LineEdit;
    else if (dynamic_cast<Plasma::PushButton*>(sipCpp))
        sipType = sipType_Plasma_PushButton;
    else if (dynamic_cast<Plasma::RadioButton*>(sipCpp))
        sipType = sipType_Plasma_RadioButton;
    else if (dynamic_cast<Plasma::ScrollBar*>(sipCpp))
        sipType = sipType_Plasma_ScrollBar;
    else if (dynamic_cast<Plasma::Slider*>(sipCpp))
        sipType = sipType_Plasma_Slider;
    else if (dynamic_cast<Plasma::SpinBox*>(sipCpp))
        sipType = sipType_Plasma_SpinBox;
    else if (dynamic_cast<Plasma::TextBrowser*>(sipCpp))
        sipType = sipType_Plasma_TextBrowser;
    else if (dynamic_cast<Plasma::TextEdit*>(sipCpp))
        sipType = sipType_Plasma_TextEdit;
    else if (dynamic_cast<Plasma::ToolButton*>(sipCpp))
        sipType = sipType_Plasma_ToolButton;
    else if (dynamic_cast<Plasma::TreeView*>(sipCpp))
        sipType = sipType_Plasma_TreeView;
    else if (dynamic_cast<Plasma::VideoWidget*>(sipCpp))
        sipType = sipType_Plasma_VideoWidget;
    else if (dynamic_cast<Plasma::Dialog*>(sipCpp))
        sipType = sipType_Plasma_Dialog;
    else if (dynamic_cast<Plasma::View*>(sipCpp))
        sipType = sipType_Plasma_View;
%End
"""
},
# ./plasma/packagestructure.sip
"QList<const": { #QList<const char*>
"code":
"""
%ConvertToTypeCode
    return NULL;
%End
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        PyObject *pobj;
        int iserr;

        if ((pobj = sipBuildResult(&iserr,"s",sipCpp->value(i))) == NULL)
        {
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
"""
},
# ./plasma/abstractrunner.sip
"AbstractRunner": { #AbstractRunner : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Plasma::ConfigLoader*>(sipCpp))
        sipType = sipType_Plasma_ConfigLoader;
    else if (dynamic_cast<Plasma::AccessAppletJob*>(sipCpp))
        sipType = sipType_Plasma_AccessAppletJob;
    else if (dynamic_cast<Plasma::ServiceAccessJob*>(sipCpp))
        sipType = sipType_Plasma_ServiceAccessJob;
    else if (dynamic_cast<Plasma::ServiceJob*>(sipCpp))
        sipType = sipType_Plasma_ServiceJob;
    else if (dynamic_cast<Plasma::AbstractDialogManager*>(sipCpp))
        sipType = sipType_Plasma_AbstractDialogManager;
    else if (dynamic_cast<Plasma::AbstractRunner*>(sipCpp))
        sipType = sipType_Plasma_AbstractRunner;
    else if (dynamic_cast<Plasma::AccessManager*>(sipCpp))
        sipType = sipType_Plasma_AccessManager;
    else if (dynamic_cast<Plasma::AnimationDriver*>(sipCpp))
        sipType = sipType_Plasma_AnimationDriver;
    else if (dynamic_cast<Plasma::Animator*>(sipCpp))
        sipType = sipType_Plasma_Animator;
    else if (dynamic_cast<Plasma::AuthorizationManager*>(sipCpp))
        sipType = sipType_Plasma_AuthorizationManager;
    else if (dynamic_cast<Plasma::AuthorizationRule*>(sipCpp))
        sipType = sipType_Plasma_AuthorizationRule;
    else if (dynamic_cast<Plasma::ClientPinRequest*>(sipCpp))
        sipType = sipType_Plasma_ClientPinRequest;
    else if (dynamic_cast<Plasma::ContainmentActions*>(sipCpp))
        sipType = sipType_Plasma_ContainmentActions;
    else if (dynamic_cast<Plasma::Context*>(sipCpp))
        sipType = sipType_Plasma_Context;
    else if (dynamic_cast<Plasma::DataContainer*>(sipCpp))
        sipType = sipType_Plasma_DataContainer;
    else if (dynamic_cast<Plasma::DataEngine*>(sipCpp))
        sipType = sipType_Plasma_DataEngine;
    else if (dynamic_cast<Plasma::DataEngineManager*>(sipCpp))
        sipType = sipType_Plasma_DataEngineManager;
    else if (dynamic_cast<Plasma::PackageStructure*>(sipCpp))
        sipType = sipType_Plasma_PackageStructure;
    else if (dynamic_cast<Plasma::RunnerContext*>(sipCpp))
        sipType = sipType_Plasma_RunnerContext;
    else if (dynamic_cast<Plasma::RunnerManager*>(sipCpp))
        sipType = sipType_Plasma_RunnerManager;
    else if (dynamic_cast<Plasma::ScriptEngine*>(sipCpp))
        {
        sipType = sipType_Plasma_ScriptEngine;
        if (dynamic_cast<Plasma::AppletScript*>(sipCpp))
            sipType = sipType_Plasma_AppletScript;
        else if (dynamic_cast<Plasma::DataEngineScript*>(sipCpp))
            sipType = sipType_Plasma_DataEngineScript;
        else if (dynamic_cast<Plasma::RunnerScript*>(sipCpp))
            sipType = sipType_Plasma_RunnerScript;
        else if (dynamic_cast<Plasma::WallpaperScript*>(sipCpp))
            sipType = sipType_Plasma_WallpaperScript;
        }
    else if (dynamic_cast<Plasma::Service*>(sipCpp))
        sipType = sipType_Plasma_Service;
    else if (dynamic_cast<Plasma::Svg*>(sipCpp))
        {
        sipType = sipType_Plasma_Svg;
        if (dynamic_cast<Plasma::FrameSvg*>(sipCpp))
            sipType = sipType_Plasma_FrameSvg;
        }
    else if (dynamic_cast<Plasma::Theme*>(sipCpp))
        sipType = sipType_Plasma_Theme;
    else if (dynamic_cast<Plasma::ToolTipManager*>(sipCpp))
        sipType = sipType_Plasma_ToolTipManager;
    else if (dynamic_cast<Plasma::Wallpaper*>(sipCpp))
        sipType = sipType_Plasma_Wallpaper;
    else if (dynamic_cast<Plasma::Animation*>(sipCpp))
        sipType = sipType_Plasma_Animation;
    else if (dynamic_cast<Plasma::Delegate*>(sipCpp))
        sipType = sipType_Plasma_Delegate;
    else if (dynamic_cast<Plasma::Corona*>(sipCpp))
        sipType = sipType_Plasma_Corona;
    else if (dynamic_cast<Plasma::AbstractToolBox*>(sipCpp))
        sipType = sipType_Plasma_AbstractToolBox;
    else if (dynamic_cast<Plasma::Applet*>(sipCpp))
        {
        sipType = sipType_Plasma_Applet;
        if (dynamic_cast<Plasma::AppletProtectedThunk*>(sipCpp))
            sipType = sipType_Plasma_AppletProtectedThunk;
        else if (dynamic_cast<Plasma::Containment*>(sipCpp))
            sipType = sipType_Plasma_Containment;
        else if (dynamic_cast<Plasma::GLApplet*>(sipCpp))
            sipType = sipType_Plasma_GLApplet;
        else if (dynamic_cast<Plasma::PopupApplet*>(sipCpp))
            sipType = sipType_Plasma_PopupApplet;
        }
    else if (dynamic_cast<Plasma::BusyWidget*>(sipCpp))
        sipType = sipType_Plasma_BusyWidget;
    else if (dynamic_cast<Plasma::DeclarativeWidget*>(sipCpp))
        sipType = sipType_Plasma_DeclarativeWidget;
    else if (dynamic_cast<Plasma::Extender*>(sipCpp))
        sipType = sipType_Plasma_Extender;
    else if (dynamic_cast<Plasma::ExtenderItem*>(sipCpp))
        {
        sipType = sipType_Plasma_ExtenderItem;
        if (dynamic_cast<Plasma::ExtenderGroup*>(sipCpp))
            sipType = sipType_Plasma_ExtenderGroup;
        }
    else if (dynamic_cast<Plasma::FlashingLabel*>(sipCpp))
        sipType = sipType_Plasma_FlashingLabel;
    else if (dynamic_cast<Plasma::Frame*>(sipCpp))
        sipType = sipType_Plasma_Frame;
    else if (dynamic_cast<Plasma::IconWidget*>(sipCpp))
        sipType = sipType_Plasma_IconWidget;
    else if (dynamic_cast<Plasma::ItemBackground*>(sipCpp))
        sipType = sipType_Plasma_ItemBackground;
    else if (dynamic_cast<Plasma::Meter*>(sipCpp))
        sipType = sipType_Plasma_Meter;
    else if (dynamic_cast<Plasma::ScrollWidget*>(sipCpp))
        sipType = sipType_Plasma_ScrollWidget;
    else if (dynamic_cast<Plasma::Separator*>(sipCpp))
        sipType = sipType_Plasma_Separator;
    else if (dynamic_cast<Plasma::SignalPlotter*>(sipCpp))
        sipType = sipType_Plasma_SignalPlotter;
    else if (dynamic_cast<Plasma::SvgWidget*>(sipCpp))
        sipType = sipType_Plasma_SvgWidget;
    else if (dynamic_cast<Plasma::TabBar*>(sipCpp))
        sipType = sipType_Plasma_TabBar;
    else if (dynamic_cast<Plasma::WebView*>(sipCpp))
        sipType = sipType_Plasma_WebView;
    else if (dynamic_cast<Plasma::CheckBox*>(sipCpp))
        sipType = sipType_Plasma_CheckBox;
    else if (dynamic_cast<Plasma::ComboBox*>(sipCpp))
        sipType = sipType_Plasma_ComboBox;
    else if (dynamic_cast<Plasma::GroupBox*>(sipCpp))
        sipType = sipType_Plasma_GroupBox;
    else if (dynamic_cast<Plasma::Label*>(sipCpp))
        sipType = sipType_Plasma_Label;
    else if (dynamic_cast<Plasma::LineEdit*>(sipCpp))
        sipType = sipType_Plasma_LineEdit;
    else if (dynamic_cast<Plasma::PushButton*>(sipCpp))
        sipType = sipType_Plasma_PushButton;
    else if (dynamic_cast<Plasma::RadioButton*>(sipCpp))
        sipType = sipType_Plasma_RadioButton;
    else if (dynamic_cast<Plasma::ScrollBar*>(sipCpp))
        sipType = sipType_Plasma_ScrollBar;
    else if (dynamic_cast<Plasma::Slider*>(sipCpp))
        sipType = sipType_Plasma_Slider;
    else if (dynamic_cast<Plasma::SpinBox*>(sipCpp))
        sipType = sipType_Plasma_SpinBox;
    else if (dynamic_cast<Plasma::TextBrowser*>(sipCpp))
        sipType = sipType_Plasma_TextBrowser;
    else if (dynamic_cast<Plasma::TextEdit*>(sipCpp))
        sipType = sipType_Plasma_TextEdit;
    else if (dynamic_cast<Plasma::ToolButton*>(sipCpp))
        sipType = sipType_Plasma_ToolButton;
    else if (dynamic_cast<Plasma::TreeView*>(sipCpp))
        sipType = sipType_Plasma_TreeView;
    else if (dynamic_cast<Plasma::VideoWidget*>(sipCpp))
        sipType = sipType_Plasma_VideoWidget;
    else if (dynamic_cast<Plasma::Dialog*>(sipCpp))
        sipType = sipType_Plasma_Dialog;
    else if (dynamic_cast<Plasma::View*>(sipCpp))
        sipType = sipType_Plasma_View;
%End
"""
},
# ./kdecore/ksycocaentry.sip
"QList<KSycocaEntry::Ptr>": { #QList<KSycocaEntry::Ptr>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        KSycocaEntry::Ptr *t = new KSycocaEntry::Ptr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t->data(), sipClass_KSycocaEntry, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KSycocaEntry, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<KSycocaEntry::Ptr> *ql = new QList<KSycocaEntry::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        KSycocaEntry *t = reinterpret_cast<KSycocaEntry *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KSycocaEntry, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_KSycocaEntry, state);

            delete ql;
            return 0;
        }

        KSharedPtr<KSycocaEntry> *tptr = new KSharedPtr<KSycocaEntry> (t);

        ql->append(*tptr);

        sipReleaseInstance(t, sipClass_KSycocaEntry, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/kservicetype.sip
"QList<KServiceType::Ptr>": { #QList<KServiceType::Ptr>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        KServiceType::Ptr *t = new KServiceType::Ptr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewType(t->data(), sipType_KServiceType, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToType(PyList_GET_ITEM(sipPy, i), sipType_KServiceType, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<KServiceType::Ptr> *ql = new QList<KServiceType::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        KServiceType *t = reinterpret_cast<KServiceType *>(sipConvertToType(PyList_GET_ITEM(sipPy, i), sipType_KServiceType, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseType(t, sipType_KServiceType, state);

            delete ql;
            return 0;
        }

        KSharedPtr<KServiceType> *tptr = new KSharedPtr<KServiceType> (t);

        ql->append(*tptr);

        sipReleaseType(t, sipType_KServiceType, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
"QMap<QString,QVariant::Type>": { #QMap<QString,QVariant::Type>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QMap<QString, QVariant::Type>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        QString *t1 = new QString (i.key());
        QVariant::Type t2 =  (QVariant::Type) (i.value());

        PyObject *t1obj = sipConvertFromNewType(t1, sipType_QString, sipTransferObj);
#if PY_MAJOR_VERSION >= 3
        PyObject *t2obj = PyLong_FromLong ((long) t2);
#else
        PyObject *t2obj = PyInt_FromLong ((long) t2);
#endif

        if (t1obj == NULL || t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);
            else
                delete t1;

            if (t2obj)
                Py_DECREF(t2obj);

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
        {
            if (!sipCanConvertToType(t1obj, sipType_QString, SIP_NOT_NONE))
                return 0;

#if PY_MAJOR_VERSION >= 3
            if (!PyLong_Check (t2obj)) {
                return 0;
            }
#else
            if (!PyInt_Check (t2obj)) {
                return 0;
            }
#endif
        }

        return 1;
    }

    QMap<QString, QVariant::Type> *qm = new QMap<QString, QVariant::Type>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1;

        QString *t1 = reinterpret_cast<QString *>(sipConvertToType(t1obj, sipType_QString, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
#if PY_MAJOR_VERSION >= 3
        QVariant::Type t2 = (QVariant::Type)PyLong_AsLong (t2obj);
#else
        QVariant::Type t2 = (QVariant::Type)PyInt_AS_LONG (t2obj);
#endif

        if (*sipIsErr)
        {
            sipReleaseType(t1, sipType_QString, state1);

            delete qm;
            return 0;
        }

        qm->insert(*t1, t2);

        sipReleaseType(t1, sipType_QString, state1);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/kautosavefile.sip
"KAutoSaveFile": { #KAutoSaveFile : QFile
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KAuth::ActionWatcher*>(sipCpp))
        sipType = sipType_KAuth_ActionWatcher;
    else if (dynamic_cast<KAutostart*>(sipCpp))
        sipType = sipType_KAutostart;
    else if (dynamic_cast<KCoreConfigSkeleton*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton;
    else if (dynamic_cast<KDEDModule*>(sipCpp))
        sipType = sipType_KDEDModule;
    else if (dynamic_cast<KJob*>(sipCpp))
        {
        sipType = sipType_KJob;
        if (dynamic_cast<KCompositeJob*>(sipCpp))
            sipType = sipType_KCompositeJob;
        }
    else if (dynamic_cast<KJobTrackerInterface*>(sipCpp))
        sipType = sipType_KJobTrackerInterface;
    else if (dynamic_cast<KJobUiDelegate*>(sipCpp))
        sipType = sipType_KJobUiDelegate;
    else if (dynamic_cast<KLibLoader*>(sipCpp))
        sipType = sipType_KLibLoader;
    else if (dynamic_cast<KLocalSocketServer*>(sipCpp))
        sipType = sipType_KLocalSocketServer;
    else if (dynamic_cast<KPluginFactory*>(sipCpp))
        sipType = sipType_KPluginFactory;
    else if (dynamic_cast<KSycoca*>(sipCpp))
        sipType = sipType_KSycoca;
    else if (dynamic_cast<KSystemTimeZones*>(sipCpp))
        sipType = sipType_KSystemTimeZones;
    else if (dynamic_cast<KToolInvocation*>(sipCpp))
        sipType = sipType_KToolInvocation;
    else if (dynamic_cast<KFilterDev*>(sipCpp))
        sipType = sipType_KFilterDev;
    else if (dynamic_cast<KPtyDevice*>(sipCpp))
        sipType = sipType_KPtyDevice;
    else if (dynamic_cast<KTcpSocket*>(sipCpp))
        sipType = sipType_KTcpSocket;
    else if (dynamic_cast<KLocalSocket*>(sipCpp))
        sipType = sipType_KLocalSocket;
    else if (dynamic_cast<KAutoSaveFile*>(sipCpp))
        sipType = sipType_KAutoSaveFile;
    else if (dynamic_cast<KSaveFile*>(sipCpp))
        sipType = sipType_KSaveFile;
    else if (dynamic_cast<KTemporaryFile*>(sipCpp))
        sipType = sipType_KTemporaryFile;
    else if (dynamic_cast<KProcess*>(sipCpp))
        {
        sipType = sipType_KProcess;
        if (dynamic_cast<KPtyProcess*>(sipCpp))
            sipType = sipType_KPtyProcess;
        }
    else if (dynamic_cast<KLibrary*>(sipCpp))
        sipType = sipType_KLibrary;
    else if (dynamic_cast<KPluginLoader*>(sipCpp))
        sipType = sipType_KPluginLoader;
    else if (dynamic_cast<Sonnet::BackgroundChecker*>(sipCpp))
        sipType = sipType_Sonnet_BackgroundChecker;
%End
"""
},
# ./kdecore/kmimetype.sip
"QList<KMimeType::Ptr>": { #QList<KMimeType::Ptr>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        KMimeType::Ptr *t = new KMimeType::Ptr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t->data(), sipClass_KMimeType, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KMimeType, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<KMimeType::Ptr> *ql = new QList<KMimeType::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        KMimeType *t = reinterpret_cast<KMimeType *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KMimeType, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_KMimeType, state);

            delete ql;
            return 0;
        }

        KSharedPtr<KMimeType> *tptr = new KSharedPtr<KMimeType> (t);

        ql->append(*tptr);

        sipReleaseInstance(t, sipClass_KMimeType, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/kurl.sip
"KUrl": { #KUrl : QUrl
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QUrl'
    sipType = NULL;

    if (dynamic_cast<KUrl*>(sipCpp))
        sipType = sipType_KUrl;
%End
"""
},
# ./kdecore/kprotocolinfo.sip
"KProtocolInfo": { #KProtocolInfo : KSycocaEntry
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KSycocaEntry'
    sipType = NULL;

    if (dynamic_cast<KProtocolInfo*>(sipCpp))
        sipType = sipType_KProtocolInfo;
    else if (dynamic_cast<KService*>(sipCpp))
        sipType = sipType_KService;
    else if (dynamic_cast<KServiceGroup*>(sipCpp))
        sipType = sipType_KServiceGroup;
    else if (dynamic_cast<KServiceType*>(sipCpp))
        {
        sipType = sipType_KServiceType;
        if (dynamic_cast<KMimeType*>(sipCpp))
            sipType = sipType_KMimeType;
        }
%End
"""
},
# ./kdecore/kcoreconfigskeleton.sip
"KCoreConfigSkeleton": { #KCoreConfigSkeleton : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KConfigSkeletonItem'
    sipType = NULL;

    if (dynamic_cast<KCoreConfigSkeleton::ItemBool*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemBool;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemDateTime*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemDateTime;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemDouble*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemDouble;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemInt*>(sipCpp))
        {
        sipType = sipType_KCoreConfigSkeleton_ItemInt;
        if (dynamic_cast<KCoreConfigSkeleton::ItemEnum*>(sipCpp))
            sipType = sipType_KCoreConfigSkeleton_ItemEnum;
        }
    else if (dynamic_cast<KCoreConfigSkeleton::ItemIntList*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemIntList;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemLongLong*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemLongLong;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemPoint*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemPoint;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemProperty*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemProperty;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemRect*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemRect;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemSize*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemSize;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemString*>(sipCpp))
        {
        sipType = sipType_KCoreConfigSkeleton_ItemString;
        if (dynamic_cast<KCoreConfigSkeleton::ItemPassword*>(sipCpp))
            sipType = sipType_KCoreConfigSkeleton_ItemPassword;
        else if (dynamic_cast<KCoreConfigSkeleton::ItemPath*>(sipCpp))
            sipType = sipType_KCoreConfigSkeleton_ItemPath;
        }
    else if (dynamic_cast<KCoreConfigSkeleton::ItemStringList*>(sipCpp))
        {
        sipType = sipType_KCoreConfigSkeleton_ItemStringList;
        if (dynamic_cast<KCoreConfigSkeleton::ItemPathList*>(sipCpp))
            sipType = sipType_KCoreConfigSkeleton_ItemPathList;
        }
    else if (dynamic_cast<KCoreConfigSkeleton::ItemUInt*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemUInt;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemULongLong*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemULongLong;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemUrl*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemUrl;
    else if (dynamic_cast<KCoreConfigSkeleton::ItemUrlList*>(sipCpp))
        sipType = sipType_KCoreConfigSkeleton_ItemUrlList;
%End
"""
},
# ./kdecore/kservice.sip
"QList<KService::Ptr>": { #QList<KService::Ptr>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        KService::Ptr *t = new KService::Ptr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewType(t->data(), sipType_KService, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToType(PyList_GET_ITEM(sipPy, i), sipType_KService, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<KService::Ptr> *ql = new QList<KService::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        KService *t = reinterpret_cast<KService *>(sipConvertToType(PyList_GET_ITEM(sipPy, i), sipType_KService, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseType(t, sipType_KService, state);

            delete ql;
            return 0;
        }

        KSharedPtr<KService> *tptr = new KSharedPtr<KService> (t);

        ql->append(*tptr);

        sipReleaseType(t, sipType_KService, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/kcmdlineargs.sip
"KCmdLineOptions": { #KCmdLineOptions
"code":
"""
%TypeHeaderCode
#include <kcmdlineargs.h>
extern char **pyArgvToC(PyObject *argvlist,int *argcp);
extern void updatePyArgv(PyObject *argvlist,int argc,char **argv);
%End
"""
},
"KCmdLineArgs": { #KCmdLineArgs
"code":
"""
%TypeHeaderCode
#include <kcmdlineargs.h>
#include <qapplication.h>
extern char **pyArgvToC(PyObject *argvlist,int *argcp);
extern void updatePyArgv(PyObject *argvlist,int argc,char **argv);
%End
"""
},
# ./kdecore/ksharedconfig.sip
"KSharedConfigPtr": { #KSharedConfigPtr
"code":
"""
%ConvertFromTypeCode
    if (!sipCpp)
        return NULL;

    KSharedConfigPtr kcpp = *sipCpp;
    KSharedConfig *ksc    = kcpp.data ();
    ksc->ref.ref();
    PyObject *pyKsc       = sipConvertFromInstance(ksc, sipClass_KSharedConfig, sipTransferObj);
    return pyKsc;
%End
%ConvertToTypeCode
    if (sipIsErr == NULL)
        return 1;

    int state;
    KSharedConfig* ksc = (KSharedConfig *)sipConvertToInstance(sipPy, sipClass_KSharedConfig, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr);
    *sipCppPtr = new KSharedConfigPtr (ksc);
    ksc->ref.deref();
    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/kconfig.sip
"KConfig": { #KConfig : KConfigBase
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KConfigBase'
    sipType = NULL;

    if (dynamic_cast<KConfig*>(sipCpp))
        {
        sipType = sipType_KConfig;
        if (dynamic_cast<KDesktopFile*>(sipCpp))
            sipType = sipType_KDesktopFile;
        else if (dynamic_cast<KSharedConfig*>(sipCpp))
            sipType = sipType_KSharedConfig;
        }
    else if (dynamic_cast<KConfigGroup*>(sipCpp))
        sipType = sipType_KConfigGroup;
%End
"""
},
# ./kdecore/typedefs.sip
"QMap<TYPE1,TYPE2*>": { #QMap<TYPE1,TYPE2*>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QMap<TYPE1, TYPE2>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        TYPE1 *t1 = new TYPE1(i.key());
        TYPE2 *t2 = new TYPE2(i.value());

        PyObject *t1obj = sipConvertFromNewType(t1, sipType_TYPE1, sipTransferObj);
        PyObject *t2obj = sipConvertFromNewType(t2, sipType_TYPE2, sipTransferObj);

        if (t1obj == NULL || t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);
            else
                delete t1;

            if (t2obj)
                Py_DECREF(t2obj);
            else
                delete t2;

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, *t2obj))
        {
            if (!sipCanConvertToType(t1obj, sipType_TYPE1, SIP_NOT_NONE))
                return 0;

            if (!sipCanConvertToType(t2obj, sipType_TYPE2, SIP_NOT_NONE))
                return 0;
        }

        return 1;
    }

    QMap<TYPE1, TYPE2*> *qm = new QMap<TYPE1, TYPE2*>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1, state2;

        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, sipType_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
        TYPE2 *t2 = reinterpret_cast<TYPE2 *>(sipConvertToType(t2obj, sipType_TYPE2, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseType(t1, sipType_TYPE1, state1);
            sipReleaseType(t2, sipType_TYPE2, state2);

            delete qm;
            return 0;
        }

        qm->insert(*t1, t2);

        sipReleaseType(t1, sipType_TYPE1, state1);
        sipReleaseType(t2, sipType_TYPE2, state2);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
"QMap<TYPE1,int>": { #QMap<TYPE1,int>
"code":
"""
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
"""
},
"KSharedPtr<TYPE>": { #KSharedPtr<TYPE>
"code":
"""
%ConvertFromTypeCode
    // Convert to a Python instance

    if (!sipCpp)
        return NULL;

    KSharedPtr<TYPE> *cPtr = new KSharedPtr<TYPE> (*(KSharedPtr<TYPE> *)sipCpp);
    TYPE *cpp = cPtr->data ();
    PyObject *obj = sipConvertFromType(cpp, sipType_TYPE, sipTransferObj);

    return obj;
%End
%ConvertToTypeCode
    // Convert a Python instance to a Ptr on the heap.
    if (sipIsErr == NULL) {
        return 1;
    }

    int iserr = 0;
    TYPE *cpp = (TYPE *)sipForceConvertToType(sipPy, sipType_TYPE, NULL, 0, NULL, &iserr);

    if (iserr)
    {
        *sipIsErr = 1;
        return 0;
    }

    *sipCppPtr = new KSharedPtr<TYPE> (cpp);

    return 1;
%End
"""
},
"QHash<TYPE1,TYPE2>": { #QHash<TYPE1,TYPE2>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QHash<TYPE1, TYPE2>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        TYPE1 *t1 = new TYPE1(i.key());
        TYPE2 *t2 = new TYPE2(i.value());

        PyObject *t1obj = sipConvertFromNewInstance(t1, sipClass_TYPE1, sipTransferObj);
        PyObject *t2obj = sipConvertFromNewInstance(t2, sipClass_TYPE2, sipTransferObj);

        if (t1obj == NULL || t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);
            else
                delete t1;

            if (t2obj)
                Py_DECREF(t2obj);
            else
                delete t2;

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
        {
            if (!sipCanConvertToInstance(t1obj, sipClass_TYPE1, SIP_NOT_NONE))
                return 0;

            if (!sipCanConvertToInstance(t2obj, sipClass_TYPE2, SIP_NOT_NONE))
                return 0;
        }

        return 1;
    }

    QHash<TYPE1, TYPE2> *qm = new QHash<TYPE1, TYPE2>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1, state2;

        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToInstance(t1obj, sipClass_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
        TYPE2 *t2 = reinterpret_cast<TYPE2 *>(sipConvertToInstance(t2obj, sipClass_TYPE2, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t1, sipClass_TYPE1, state1);
            sipReleaseInstance(t2, sipClass_TYPE2, state2);

            delete qm;
            return 0;
        }

        qm->insert(*t1, *t2);

        sipReleaseInstance(t1, sipClass_TYPE1, state1);
        sipReleaseInstance(t2, sipClass_TYPE2, state2);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
"QHash<TYPE1,TYPE2*>": { #QHash<TYPE1,TYPE2*>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QHash<TYPE1, TYPE2*>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        TYPE1 *t1 = new TYPE1(i.key());
        TYPE2 *t2 = i.value();

        PyObject *t1obj = sipConvertFromNewType(t1, sipType_TYPE1, sipTransferObj);
        PyObject *t2obj = sipConvertFromNewType(t2, sipType_TYPE2, sipTransferObj);

        if (t1obj == NULL || t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);
            else
                delete t1;

            if (t2obj)
                Py_DECREF(t2obj);
            else
                delete t2;

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
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

            if (!sipCanConvertToType(t2obj, sipType_TYPE2, SIP_NOT_NONE))
                return 0;
        }

        return 1;
    }

    QHash<TYPE1, TYPE2*> *qm = new QHash<TYPE1, TYPE2*>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1, state2;

        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, sipType_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
        TYPE2 *t2 = reinterpret_cast<TYPE2 *>(sipConvertToType(t2obj, sipType_TYPE2, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseType(t1, sipType_TYPE1, state1);
            sipReleaseType(t2, sipType_TYPE2, state2);

            delete qm;
            return 0;
        }

        qm->insert(*t1, t2);

        sipReleaseType(t1, sipType_TYPE1, state1);
        sipReleaseType(t2, sipType_TYPE2, state2);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
"QPair<TYPE1,TYPE2>": { #QPair<TYPE1,TYPE2>
"code":
"""
%ConvertFromTypeCode
    // Create the tuple.
    TYPE1 *t1 = new TYPE1(sipCpp->first);
    TYPE2 *t2 = new TYPE2(sipCpp->second);

    PyObject *t1obj = sipConvertFromNewType(t1, sipType_TYPE1, sipTransferObj);
    PyObject *t2obj = sipConvertFromNewType(t2, sipType_TYPE2, sipTransferObj);

    if (t1obj == NULL || t2obj == NULL)
    {
        if (t1obj)
            Py_DECREF(t1obj);
        else
            delete t1;

        if (t2obj)
            Py_DECREF(t2obj);
        else
            delete t2;

        return NULL;
    }

    return Py_BuildValue((char *)"NN", t1obj, t2obj);
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return (PyTuple_Size(sipPy) == 2);


    int state1, state2;

    PyObject *t1obj = PyTuple_GET_ITEM(sipPy, 0);
    PyObject *t2obj = PyTuple_GET_ITEM(sipPy, 1);

    TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, sipType_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
    TYPE2 *t2 = reinterpret_cast<TYPE2 *>(sipConvertToType(t2obj, sipType_TYPE2, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

    if (*sipIsErr)
    {
        sipReleaseType(t1, sipType_TYPE1, state1);
        sipReleaseType(t2, sipType_TYPE2, state2);

        return 0;
    }

    QPair<TYPE1, TYPE2> *qp = new QPair<TYPE1, TYPE2>;

    qp->first  = *t1;
    qp->second = *t2;

    *sipCppPtr = qp;

    return sipGetState(sipTransferObj);
%End
"""
},
"QStack<TYPE*>": { #QStack<TYPE*>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        TYPE *t = (TYPE *)(sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t, sipClass_TYPE, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_TYPE, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QStack<TYPE*> *qv = new QStack<TYPE*>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        TYPE *t = reinterpret_cast<TYPE *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_TYPE, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_TYPE, state);

            delete qv;
            return 0;
        }

        qv->append(t);

        sipReleaseInstance(t, sipClass_TYPE, state);
    }

    *sipCppPtr = qv;

    return sipGetState(sipTransferObj);
%End
"""
},
"QHash<int,int>": { #QHash<int,int>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QHash<int, int>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        int t1 = i.key();
        int t2 = i.value();

#if PY_MAJOR_VERSION >= 3
        PyObject *t1obj = PyLong_FromLong ((long)t1);
        PyObject *t2obj = PyLong_FromLong ((long)t2);
#else
        PyObject *t1obj = PyInt_FromLong ((long)t1);
        PyObject *t2obj = PyInt_FromLong ((long)t2);
#endif

        if (PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);

            if (t2obj)
                Py_DECREF(t2obj);

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
        {
#if PY_MAJOR_VERSION >= 3
            if (!PyNumber_Check (t1obj))
#else
            if (!PyInt_Check (t1obj))
#endif
                return 0;

#if PY_MAJOR_VERSION >= 3
            if (!PyNumber_Check (t2obj))
#else
            if (!PyInt_Check (t2obj))
#endif
                return 0;
        }

        return 1;
    }

    QHash<int, int> *qm = new QHash<int, int>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state2;

#if PY_MAJOR_VERSION >= 3
        int t1 = PyLong_AsLong (t1obj);
#else
        int t1 = PyInt_AS_LONG (t1obj);
#endif

#if PY_MAJOR_VERSION >= 3
        int t2 = PyLong_AsLong (t2obj);
#else
        int t2 = PyInt_AS_LONG (t2obj);
#endif

        if (*sipIsErr)
        {
            delete qm;
            return 0;
        }

        qm->insert(t1, t2);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
"QHash<TYPE1,bool>": { #QHash<TYPE1,bool>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QHash<TYPE1, bool>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        TYPE1 *t1 = new TYPE1(i.key());
        bool t2 = i.value();

        PyObject *t1obj = sipConvertFromNewType(t1, sipType_TYPE1, sipTransferObj);
#if PY_MAJOR_VERSION >= 3
        PyObject *t2obj = PyBool_FromLong ((long)t2);
#else
        PyObject *t2obj = PyBool_FromLong ((long)t2);
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
    PyObject *t1obj, *t2obj;
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
            if (!PyBool_Check (t2obj))
#else
            if (!PyBool_Check (t2obj))
#endif
                return 0;
        }

        return 1;
    }

    QHash<TYPE1, bool> *qm = new QHash<TYPE1, bool>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state1, state2;

        TYPE1 *t1 = reinterpret_cast<TYPE1 *>(sipConvertToType(t1obj, sipType_TYPE1, sipTransferObj, SIP_NOT_NONE, &state1, sipIsErr));
#if PY_MAJOR_VERSION >= 3
        bool t2 = PyObject_IsTrue(t2obj);
#else
        bool t2 = PyObject_IsTrue (t2obj);
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
"""
},
"QVector<int>": { #QVector<int>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        int t = (sipCpp->at(i));

#if PY_MAJOR_VERSION >= 3
        PyObject *tobj = PyLong_FromLong(t);
#else
        PyObject *tobj = PyInt_FromLong(t);
#endif

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
            PyObject *tobj = PyList_GET_ITEM(sipPy, i);
#if PY_MAJOR_VERSION >= 3
            if (!PyNumber_Check(tobj))
#else
            if (!PyInt_Check(tobj))
#endif
                return 0;
        }
        return 1;
    }

    QVector<int> *qv = new QVector<int>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        PyObject *tobj = PyList_GET_ITEM(sipPy, i);
#if PY_MAJOR_VERSION >= 3
        int t = PyLong_AsLong (tobj);
#else
        int t = PyInt_AS_LONG (tobj);
#endif

        if (*sipIsErr)
        {
            delete qv;
            return 0;
        }

        qv->append(t);
    }

    *sipCppPtr = qv;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdecore/ktimezone.sip
"KTimeZone": { #KTimeZone
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KTimeZone'
    sipType = NULL;

    if (dynamic_cast<KSystemTimeZone*>(sipCpp))
        sipType = sipType_KSystemTimeZone;
    else if (dynamic_cast<KTzfileTimeZone*>(sipCpp))
        sipType = sipType_KTzfileTimeZone;
%End
"""
},
"KTimeZoneBackend": { #KTimeZoneBackend
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KTimeZoneBackend'
    sipType = NULL;

    if (dynamic_cast<KSystemTimeZoneBackend*>(sipCpp))
        sipType = sipType_KSystemTimeZoneBackend;
    else if (dynamic_cast<KTzfileTimeZoneBackend*>(sipCpp))
        sipType = sipType_KTzfileTimeZoneBackend;
%End
"""
},
"KTimeZoneSource": { #KTimeZoneSource
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KTimeZoneSource'
    sipType = NULL;

    if (dynamic_cast<KSystemTimeZoneSource*>(sipCpp))
        sipType = sipType_KSystemTimeZoneSource;
    else if (dynamic_cast<KTzfileTimeZoneSource*>(sipCpp))
        sipType = sipType_KTzfileTimeZoneSource;
%End
"""
},
# ./kdecore/kmacroexpander.sip
"KCharMacroExpander": { #KCharMacroExpander : KMacroExpanderBase
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KMacroExpanderBase'
    sipType = NULL;

    if (dynamic_cast<KCharMacroExpander*>(sipCpp))
        sipType = sipType_KCharMacroExpander;
    else if (dynamic_cast<KWordMacroExpander*>(sipCpp))
        sipType = sipType_KWordMacroExpander;
%End
"""
},
# ./dnssd/remoteservice.sip
"QList<DNSSD::RemoteService::Ptr>": { #QList<DNSSD::RemoteService::Ptr>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        DNSSD::RemoteService::Ptr *t = new DNSSD::RemoteService::Ptr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t->data(), sipClass_DNSSD_RemoteService, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_DNSSD_RemoteService, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<DNSSD::RemoteService::Ptr> *ql = new QList<DNSSD::RemoteService::Ptr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        DNSSD::RemoteService *t = reinterpret_cast<DNSSD::RemoteService *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_DNSSD_RemoteService, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_DNSSD_RemoteService, state);

            delete ql;
            return 0;
        }

        DNSSD::RemoteService::Ptr *tptr = new DNSSD::RemoteService::Ptr (t);

        ql->append(*tptr);

        sipReleaseInstance(t, sipClass_DNSSD_RemoteService, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./dnssd/servicebase.sip
"ServiceBase": { #ServiceBase : KShared
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'ServiceBase'
    sipType = NULL;

    if (dynamic_cast<DNSSD::ServiceBase*>(sipCpp))
        {
        sipType = sipType_DNSSD_ServiceBase;
        if (dynamic_cast<DNSSD::PublicService*>(sipCpp))
            sipType = sipType_DNSSD_PublicService;
        else if (dynamic_cast<DNSSD::RemoteService*>(sipCpp))
            sipType = sipType_DNSSD_RemoteService;
        }
%End
"""
},
# ./dnssd/domainbrowser.sip
"DomainBrowser": { #DomainBrowser : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<DNSSD::DomainBrowser*>(sipCpp))
        sipType = sipType_DNSSD_DomainBrowser;
    else if (dynamic_cast<DNSSD::PublicService*>(sipCpp))
        sipType = sipType_DNSSD_PublicService;
    else if (dynamic_cast<DNSSD::RemoteService*>(sipCpp))
        sipType = sipType_DNSSD_RemoteService;
    else if (dynamic_cast<DNSSD::ServiceBrowser*>(sipCpp))
        sipType = sipType_DNSSD_ServiceBrowser;
    else if (dynamic_cast<DNSSD::ServiceTypeBrowser*>(sipCpp))
        sipType = sipType_DNSSD_ServiceTypeBrowser;
    else if (dynamic_cast<DNSSD::DomainModel*>(sipCpp))
        sipType = sipType_DNSSD_DomainModel;
    else if (dynamic_cast<DNSSD::ServiceModel*>(sipCpp))
        sipType = sipType_DNSSD_ServiceModel;
%End
"""
},
# ./kutils/dialog.sip
"Dialog": { #Dialog : KCMultiDialog
"code":
"""
%TypeHeaderCode
#include <dialog.h>
#include <kcmultidialog.h>
%End
"""
},
# ./kutils/kcmoduleproxy.sip
"KCModuleProxy": { #KCModuleProxy : QWidget
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KEmoticons*>(sipCpp))
        sipType = sipType_KEmoticons;
    else if (dynamic_cast<KEmoticonsProvider*>(sipCpp))
        sipType = sipType_KEmoticonsProvider;
    else if (dynamic_cast<KIdleTime*>(sipCpp))
        sipType = sipType_KIdleTime;
    else if (dynamic_cast<KSettings::PluginPage*>(sipCpp))
        sipType = sipType_KSettings_PluginPage;
    else if (dynamic_cast<KCModuleProxy*>(sipCpp))
        sipType = sipType_KCModuleProxy;
    else if (dynamic_cast<KPluginSelector*>(sipCpp))
        sipType = sipType_KPluginSelector;
    else if (dynamic_cast<KCMultiDialog*>(sipCpp))
        {
        sipType = sipType_KCMultiDialog;
        if (dynamic_cast<KSettings::Dialog*>(sipCpp))
            sipType = sipType_KSettings_Dialog;
        }
    else if (dynamic_cast<KPrintPreview*>(sipCpp))
        sipType = sipType_KPrintPreview;
%End
"""
},
# ./kio/global.sip
"KIO::MetaData": { #KIO::MetaData
"code":
"""
%ConvertFromTypeCode
    // Convert to a Python dict

    if (!sipCpp)
        return PyDict_New();

    PyObject *dict;

    // Create the dictionary.

    if ((dict = PyDict_New()) == NULL)
        return NULL;

    // Get it.

    const QMap<QString,QString> cppmap = *sipCpp;
    QMap<QString,QString>::ConstIterator it;

    for (it = cppmap.begin (); it != cppmap.end (); ++it)
    {
        QString acpp = it.key ();
        QString bcpp = it.value ();
        PyObject *ainst = 0;
        PyObject *binst = 0;
        if (((ainst = sipBuildResult (NULL, "N", new QString (acpp), sipType_QString)) == NULL)
            || ((binst = sipBuildResult (NULL, "N", new QString (bcpp), sipType_QString)) == NULL)
            || (PyDict_SetItem (dict, ainst, binst) < 0))
        {
            Py_XDECREF (ainst);
            Py_XDECREF (binst);
            Py_DECREF (dict);
            return NULL;
        }
    }

    return dict;
%End
%ConvertToTypeCode
    // Convert a Python dictionary to a QMap on the heap.

    if (sipIsErr == NULL)
        return PyDict_Check(sipPy);


    QMap<QString,QString> *cppmap = new QMap<QString,QString>;

    PyObject *aelem, *belem;
    SIP_SSIZE_T pos = 0;
    QString *acpp;
    QString *bcpp;

    while (PyDict_Next(sipPy, &pos, &aelem, &belem))
    {
        int iserr = 0;

        acpp = (QString *)sipForceConvertToType(aelem, sipType_QString, NULL, 0, NULL, &iserr);
        bcpp = (QString *)sipForceConvertToType(belem, sipType_QString, NULL, 0, NULL, &iserr);

        if (iserr)
        {
            *sipIsErr = 1;
            delete cppmap;
            return 0;
        }

        cppmap->insert (*acpp, *bcpp);
    }

    *sipCppPtr = (KIO::MetaData *)cppmap;

    return 1;
%End
"""
},
# ./kio/kacl.sip
"ACLUserPermissionsList": { #ACLUserPermissionsList
"code":
"""
%ConvertFromTypeCode
    if (!sipCpp)
        return PyList_New(0);

    // Create the list
    PyObject *pylist;
    if ((pylist = PyList_New(0)) == NULL)
        return NULL;

    QList<QPair<QString, unsigned short> > *cpplist = (QList<QPair<QString, unsigned short> > *)sipCpp;
    PyObject *inst = NULL;

    // Get it.
    QList<QPair<QString, unsigned short> >::Iterator it;
    for( it = cpplist->begin(); it != cpplist->end(); ++it )
    {
        QString s = (*it).first;
        ushort  u = (*it).second;
        PyObject *pys = sipBuildResult (NULL, "N", new QString (s), sipType_QString);
        if ((pys == NULL) || ((inst = Py_BuildValue ("Ni", pys, u)) == NULL)
            || PyList_Append (pylist, inst) < 0)
        {
            Py_XDECREF (inst);
            Py_XDECREF (pys);
            Py_DECREF (pylist);
            return NULL;
        }
    }

    return pylist;
%End
%ConvertToTypeCode
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QList<QPair<QString, unsigned short> > *cpplist = new QList<QPair<QString, unsigned short> >;

    QString p1;
    int iserr = 0;

    for (int i = 0; i < PyList_Size (sipPy); i++)
    {
        PyObject *elem = PyList_GET_ITEM (sipPy, i);
        PyObject *pyp1 = PyTuple_GET_ITEM (elem, 0);
        p1 = *(QString *)sipForceConvertToType(pyp1, sipType_QString, NULL, 0, NULL, &iserr);
        if (iserr)
        {
            *sipIsErr = 1;
            delete cpplist;
            return 0;
        }
#if PY_MAJOR_VERSION >= 3
        ushort p2 = (ushort)(PyLong_AsLong (PyTuple_GET_ITEM (elem, 1)));
#else
        ushort p2 = (ushort)(PyInt_AS_LONG (PyTuple_GET_ITEM (elem, 1)));
#endif
        cpplist->append (QPair<QString, unsigned short> (p1, p2));
    }

    *sipCppPtr = cpplist;

    return 1;
%End
"""
},
# ./kio/tcpslavebase.sip
"TCPSlaveBase": { #TCPSlaveBase : KIO::SlaveBase
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'SlaveBase'
    sipType = NULL;

    if (dynamic_cast<KIO::ForwardingSlaveBase*>(sipCpp))
        sipType = sipType_KIO_ForwardingSlaveBase;
    else if (dynamic_cast<KIO::TCPSlaveBase*>(sipCpp))
        sipType = sipType_KIO_TCPSlaveBase;
%End
"""
},
# ./kio/karchive.sip
"KArchiveDirectory": { #KArchiveDirectory : KArchiveEntry
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KArchiveEntry'
    sipType = NULL;

    if (dynamic_cast<KArchiveDirectory*>(sipCpp))
        sipType = sipType_KArchiveDirectory;
    else if (dynamic_cast<KArchiveFile*>(sipCpp))
        {
        sipType = sipType_KArchiveFile;
        if (dynamic_cast<KZipFileEntry*>(sipCpp))
            sipType = sipType_KZipFileEntry;
        }
%End
"""
},
# ./kio/kimagefilepreview.sip
"KImageFilePreview": { #KImageFilePreview : KPreviewWidgetBase
"code":
"""
%TypeHeaderCode
#include <kimagefilepreview.h>
#include <jobclasses.h>
%End
"""
},
# ./kio/kservicegroup.sip
"KServiceGroup": { #KServiceGroup : KSycocaEntry
"code":
"""
%ConvertToSubClassCode

    if (dynamic_cast<KServiceGroup*>(sipCpp))
        sipClass = sipClass_KServiceGroup;
    else if (dynamic_cast<KServiceSeparator*>(sipCpp))
        sipClass = sipClass_KServiceSeparator;
    else
        sipClass = NULL;
%End
"""
},
"KServiceGroup::List": { #KServiceGroup::List
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        KServiceGroup::SPtr *t = new KServiceGroup::SPtr (sipCpp->at(i));
        PyObject *tobj;

        if ((tobj = sipConvertFromNewInstance(t->data(), sipClass_KServiceGroup, sipTransferObj)) == NULL)
        {
            Py_DECREF(l);
            delete t;

            return NULL;
        }

        PyList_SET_ITEM(l, i, tobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;

        for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
            if (!sipCanConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KServiceGroup, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QList<KServiceGroup::SPtr> *ql = new QList<KServiceGroup::SPtr>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
        int state;
        KServiceGroup *t = reinterpret_cast<KServiceGroup *>(sipConvertToInstance(PyList_GET_ITEM(sipPy, i), sipClass_KServiceGroup, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_KServiceGroup, state);

            delete ql;
            return 0;
        }

        KServiceGroup::SPtr *tptr = new KServiceGroup::SPtr (t);

        ql->append(*tptr);

        sipReleaseInstance(t, sipClass_KServiceGroup, state);
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kio/accessmanager.sip
"AccessManager": { #AccessManager : QNetworkAccessManager
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'AccessManager'
    sipType = NULL;

    if (dynamic_cast<KIO::AccessManager*>(sipCpp))
        sipType = sipType_KIO_AccessManager;
%End
"""
},
"CookieJar": { #CookieJar : QNetworkCookieJar
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'CookieJar'
    sipType = NULL;

    if (dynamic_cast<KIO::Integration::CookieJar*>(sipCpp))
        sipType = sipType_KIO_Integration_CookieJar;
%End
"""
},
# ./kio/kar.sip
"KAr": { #KAr : KArchive
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KArchive'
    sipType = NULL;

    if (dynamic_cast<KAr*>(sipCpp))
        sipType = sipType_KAr;
    else if (dynamic_cast<KTar*>(sipCpp))
        sipType = sipType_KTar;
    else if (dynamic_cast<KZip*>(sipCpp))
        sipType = sipType_KZip;
%End
"""
},
# ./kio/metainfojob.sip
"MetaInfoJob": { #MetaInfoJob : KIO::Job
"code":
"""
%TypeHeaderCode
#include <metainfojob.h>
#include <kfileitem.h>
#include <jobclasses.h>
%End
"""
},
# ./kio/kbookmarkmanager.sip
"KBookmarkOwner": { #KBookmarkOwner
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KBookmarkOwner'
    sipType = NULL;

    if (dynamic_cast<KonqBookmarkOwner*>(sipCpp))
        sipType = sipType_KonqBookmarkOwner;
%End
"""
},
# ./kio/thumbcreator.sip
"ThumbCreator": { #ThumbCreator
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'ThumbCreator'
    sipType = NULL;

    if (dynamic_cast<ThumbCreatorV2*>(sipCpp))
        sipType = sipType_ThumbCreatorV2;
    else if (dynamic_cast<ThumbSequenceCreator*>(sipCpp))
        sipType = sipType_ThumbSequenceCreator;
%End
"""
},
# ./kio/kbookmarkexporter.sip
"KBookmarkExporterBase": { #KBookmarkExporterBase
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KBookmarkExporterBase'
    sipType = NULL;

    if (dynamic_cast<KIEBookmarkExporterImpl*>(sipCpp))
        sipType = sipType_KIEBookmarkExporterImpl;
    else if (dynamic_cast<KNSBookmarkExporterImpl*>(sipCpp))
        sipType = sipType_KNSBookmarkExporterImpl;
    else if (dynamic_cast<KOperaBookmarkExporterImpl*>(sipCpp))
        sipType = sipType_KOperaBookmarkExporterImpl;
%End
"""
},
# ./kio/kurlpixmapprovider.sip
"KUrlPixmapProvider": { #KUrlPixmapProvider : KPixmapProvider
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KPixmapProvider'
    sipType = NULL;

    if (dynamic_cast<KUrlPixmapProvider*>(sipCpp))
        sipType = sipType_KUrlPixmapProvider;
%End
"""
},
# ./kio/kabstractfilemodule.sip
"KAbstractFileModule": { #KAbstractFileModule : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KAbstractFileItemActionPlugin*>(sipCpp))
        sipType = sipType_KAbstractFileItemActionPlugin;
    else if (dynamic_cast<KAbstractFileModule*>(sipCpp))
        sipType = sipType_KAbstractFileModule;
    else if (dynamic_cast<KAutoMount*>(sipCpp))
        sipType = sipType_KAutoMount;
    else if (dynamic_cast<KAutoUnmount*>(sipCpp))
        sipType = sipType_KAutoUnmount;
    else if (dynamic_cast<KBookmarkDomBuilder*>(sipCpp))
        sipType = sipType_KBookmarkDomBuilder;
    else if (dynamic_cast<KBookmarkImporterBase*>(sipCpp))
        {
        sipType = sipType_KBookmarkImporterBase;
        if (dynamic_cast<KCrashBookmarkImporterImpl*>(sipCpp))
            sipType = sipType_KCrashBookmarkImporterImpl;
        else if (dynamic_cast<KIEBookmarkImporterImpl*>(sipCpp))
            sipType = sipType_KIEBookmarkImporterImpl;
        else if (dynamic_cast<KNSBookmarkImporterImpl*>(sipCpp))
            {
            sipType = sipType_KNSBookmarkImporterImpl;
            if (dynamic_cast<KMozillaBookmarkImporterImpl*>(sipCpp))
                sipType = sipType_KMozillaBookmarkImporterImpl;
            }
        else if (dynamic_cast<KOperaBookmarkImporterImpl*>(sipCpp))
            sipType = sipType_KOperaBookmarkImporterImpl;
        else if (dynamic_cast<KXBELBookmarkImporterImpl*>(sipCpp))
            sipType = sipType_KXBELBookmarkImporterImpl;
        }
    else if (dynamic_cast<KBookmarkManager*>(sipCpp))
        sipType = sipType_KBookmarkManager;
    else if (dynamic_cast<KBookmarkMenu*>(sipCpp))
        {
        sipType = sipType_KBookmarkMenu;
        if (dynamic_cast<KonqBookmarkMenu*>(sipCpp))
            sipType = sipType_KonqBookmarkMenu;
        }
    else if (dynamic_cast<KUrlCompletion*>(sipCpp))
        {
        sipType = sipType_KUrlCompletion;
        if (dynamic_cast<KShellCompletion*>(sipCpp))
            sipType = sipType_KShellCompletion;
        }
    else if (dynamic_cast<KCrashBookmarkImporter*>(sipCpp))
        sipType = sipType_KCrashBookmarkImporter;
    else if (dynamic_cast<KDataTool*>(sipCpp))
        sipType = sipType_KDataTool;
    else if (dynamic_cast<KDirLister*>(sipCpp))
        sipType = sipType_KDirLister;
    else if (dynamic_cast<KDirWatch*>(sipCpp))
        sipType = sipType_KDirWatch;
    else if (dynamic_cast<KDiskFreeSpace*>(sipCpp))
        sipType = sipType_KDiskFreeSpace;
    else if (dynamic_cast<KFileItemActionPlugin*>(sipCpp))
        sipType = sipType_KFileItemActionPlugin;
    else if (dynamic_cast<KFileItemActions*>(sipCpp))
        sipType = sipType_KFileItemActions;
    else if (dynamic_cast<KFilePreviewGenerator*>(sipCpp))
        sipType = sipType_KFilePreviewGenerator;
    else if (dynamic_cast<KFileWritePlugin*>(sipCpp))
        sipType = sipType_KFileWritePlugin;
    else if (dynamic_cast<KIO::Connection*>(sipCpp))
        sipType = sipType_KIO_Connection;
    else if (dynamic_cast<KIO::ConnectionServer*>(sipCpp))
        sipType = sipType_KIO_ConnectionServer;
    else if (dynamic_cast<KIO::FileUndoManager*>(sipCpp))
        sipType = sipType_KIO_FileUndoManager;
    else if (dynamic_cast<KIO::ForwardingSlaveBase*>(sipCpp))
        sipType = sipType_KIO_ForwardingSlaveBase;
    else if (dynamic_cast<KIO::NetAccess*>(sipCpp))
        sipType = sipType_KIO_NetAccess;
    else if (dynamic_cast<KIO::Scheduler*>(sipCpp))
        sipType = sipType_KIO_Scheduler;
    else if (dynamic_cast<KIO::SessionData*>(sipCpp))
        sipType = sipType_KIO_SessionData;
    else if (dynamic_cast<KIO::SlaveConfig*>(sipCpp))
        sipType = sipType_KIO_SlaveConfig;
    else if (dynamic_cast<KIO::SlaveInterface*>(sipCpp))
        {
        sipType = sipType_KIO_SlaveInterface;
        if (dynamic_cast<KIO::Slave*>(sipCpp))
            sipType = sipType_KIO_Slave;
        }
    else if (dynamic_cast<KIO::Job*>(sipCpp))
        {
        sipType = sipType_KIO_Job;
        if (dynamic_cast<KIO::ChmodJob*>(sipCpp))
            sipType = sipType_KIO_ChmodJob;
        else if (dynamic_cast<KIO::CopyJob*>(sipCpp))
            sipType = sipType_KIO_CopyJob;
        else if (dynamic_cast<KIO::DeleteJob*>(sipCpp))
            sipType = sipType_KIO_DeleteJob;
        else if (dynamic_cast<KIO::DirectorySizeJob*>(sipCpp))
            sipType = sipType_KIO_DirectorySizeJob;
        else if (dynamic_cast<KIO::FileCopyJob*>(sipCpp))
            sipType = sipType_KIO_FileCopyJob;
        else if (dynamic_cast<KIO::MetaInfoJob*>(sipCpp))
            sipType = sipType_KIO_MetaInfoJob;
        else if (dynamic_cast<KIO::PreviewJob*>(sipCpp))
            sipType = sipType_KIO_PreviewJob;
        else if (dynamic_cast<KIO::SimpleJob*>(sipCpp))
            {
            sipType = sipType_KIO_SimpleJob;
            if (dynamic_cast<KIO::FileJob*>(sipCpp))
                sipType = sipType_KIO_FileJob;
            else if (dynamic_cast<KIO::ListJob*>(sipCpp))
                sipType = sipType_KIO_ListJob;
            else if (dynamic_cast<KIO::StatJob*>(sipCpp))
                sipType = sipType_KIO_StatJob;
            else if (dynamic_cast<KIO::TransferJob*>(sipCpp))
                {
                sipType = sipType_KIO_TransferJob;
                if (dynamic_cast<KIO::DavJob*>(sipCpp))
                    sipType = sipType_KIO_DavJob;
                else if (dynamic_cast<KIO::MimetypeJob*>(sipCpp))
                    sipType = sipType_KIO_MimetypeJob;
                else if (dynamic_cast<KIO::MultiGetJob*>(sipCpp))
                    sipType = sipType_KIO_MultiGetJob;
                else if (dynamic_cast<KIO::SpecialJob*>(sipCpp))
                    sipType = sipType_KIO_SpecialJob;
                else if (dynamic_cast<KIO::StoredTransferJob*>(sipCpp))
                    sipType = sipType_KIO_StoredTransferJob;
                }
            }
        }
    else if (dynamic_cast<KIO::JobUiDelegate*>(sipCpp))
        sipType = sipType_KIO_JobUiDelegate;
    else if (dynamic_cast<KNFSShare*>(sipCpp))
        sipType = sipType_KNFSShare;
    else if (dynamic_cast<KPropertiesDialogPlugin*>(sipCpp))
        {
        sipType = sipType_KPropertiesDialogPlugin;
        if (dynamic_cast<KFileSharePropsPlugin*>(sipCpp))
            sipType = sipType_KFileSharePropsPlugin;
        }
    else if (dynamic_cast<KRun*>(sipCpp))
        sipType = sipType_KRun;
    else if (dynamic_cast<KSambaShare*>(sipCpp))
        sipType = sipType_KSambaShare;
    else if (dynamic_cast<KUriFilterPlugin*>(sipCpp))
        sipType = sipType_KUriFilterPlugin;
    else if (dynamic_cast<KFileItemDelegate*>(sipCpp))
        sipType = sipType_KFileItemDelegate;
    else if (dynamic_cast<KDeviceListModel*>(sipCpp))
        sipType = sipType_KDeviceListModel;
    else if (dynamic_cast<KDirModel*>(sipCpp))
        sipType = sipType_KDirModel;
    else if (dynamic_cast<KFilePlacesModel*>(sipCpp))
        sipType = sipType_KFilePlacesModel;
    else if (dynamic_cast<KDirSortFilterProxyModel*>(sipCpp))
        sipType = sipType_KDirSortFilterProxyModel;
    else if (dynamic_cast<KBookmarkActionMenu*>(sipCpp))
        sipType = sipType_KBookmarkActionMenu;
    else if (dynamic_cast<KNewFileMenu*>(sipCpp))
        sipType = sipType_KNewFileMenu;
    else if (dynamic_cast<KBookmarkAction*>(sipCpp))
        sipType = sipType_KBookmarkAction;
    else if (dynamic_cast<KDataToolAction*>(sipCpp))
        sipType = sipType_KDataToolAction;
    else if (dynamic_cast<KDirOperator*>(sipCpp))
        sipType = sipType_KDirOperator;
    else if (dynamic_cast<KFileMetaDataConfigurationWidget*>(sipCpp))
        sipType = sipType_KFileMetaDataConfigurationWidget;
    else if (dynamic_cast<KFileMetaDataWidget*>(sipCpp))
        sipType = sipType_KFileMetaDataWidget;
    else if (dynamic_cast<KFileWidget*>(sipCpp))
        sipType = sipType_KFileWidget;
    else if (dynamic_cast<KIO::RenameDialogPlugin*>(sipCpp))
        sipType = sipType_KIO_RenameDialogPlugin;
    else if (dynamic_cast<KPreviewWidgetBase*>(sipCpp))
        {
        sipType = sipType_KPreviewWidgetBase;
        if (dynamic_cast<KImageFilePreview*>(sipCpp))
            sipType = sipType_KImageFilePreview;
        }
    else if (dynamic_cast<KStatusBarOfflineIndicator*>(sipCpp))
        sipType = sipType_KStatusBarOfflineIndicator;
    else if (dynamic_cast<KUrlNavigator*>(sipCpp))
        sipType = sipType_KUrlNavigator;
    else if (dynamic_cast<KIconButton*>(sipCpp))
        sipType = sipType_KIconButton;
    else if (dynamic_cast<KFileFilterCombo*>(sipCpp))
        sipType = sipType_KFileFilterCombo;
    else if (dynamic_cast<KUrlComboBox*>(sipCpp))
        sipType = sipType_KUrlComboBox;
    else if (dynamic_cast<KBookmarkDialog*>(sipCpp))
        sipType = sipType_KBookmarkDialog;
    else if (dynamic_cast<KDirSelectDialog*>(sipCpp))
        sipType = sipType_KDirSelectDialog;
    else if (dynamic_cast<KFileDialog*>(sipCpp))
        {
        sipType = sipType_KFileDialog;
        if (dynamic_cast<KEncodingFileDialog*>(sipCpp))
            sipType = sipType_KEncodingFileDialog;
        }
    else if (dynamic_cast<KIO::SkipDialog*>(sipCpp))
        sipType = sipType_KIO_SkipDialog;
    else if (dynamic_cast<KIconDialog*>(sipCpp))
        sipType = sipType_KIconDialog;
    else if (dynamic_cast<KMimeTypeChooserDialog*>(sipCpp))
        sipType = sipType_KMimeTypeChooserDialog;
    else if (dynamic_cast<KNameAndUrlInputDialog*>(sipCpp))
        sipType = sipType_KNameAndUrlInputDialog;
    else if (dynamic_cast<KOpenWithDialog*>(sipCpp))
        sipType = sipType_KOpenWithDialog;
    else if (dynamic_cast<KOCRDialog*>(sipCpp))
        sipType = sipType_KOCRDialog;
    else if (dynamic_cast<KPropertiesDialog*>(sipCpp))
        sipType = sipType_KPropertiesDialog;
    else if (dynamic_cast<KScanDialog*>(sipCpp))
        sipType = sipType_KScanDialog;
    else if (dynamic_cast<KIO::PasswordDialog*>(sipCpp))
        sipType = sipType_KIO_PasswordDialog;
    else if (dynamic_cast<KUrlRequesterDialog*>(sipCpp))
        sipType = sipType_KUrlRequesterDialog;
    else if (dynamic_cast<KIO::RenameDialog*>(sipCpp))
        sipType = sipType_KIO_RenameDialog;
    else if (dynamic_cast<KBuildSycocaProgressDialog*>(sipCpp))
        sipType = sipType_KBuildSycocaProgressDialog;
    else if (dynamic_cast<KUrlRequester*>(sipCpp))
        {
        sipType = sipType_KUrlRequester;
        if (dynamic_cast<KUrlComboRequester*>(sipCpp))
            sipType = sipType_KUrlComboRequester;
        }
    else if (dynamic_cast<KMimeTypeChooser*>(sipCpp))
        sipType = sipType_KMimeTypeChooser;
    else if (dynamic_cast<KFilePlacesView*>(sipCpp))
        sipType = sipType_KFilePlacesView;
    else if (dynamic_cast<KIconCanvas*>(sipCpp))
        sipType = sipType_KIconCanvas;
    else if (dynamic_cast<KBookmarkContextMenu*>(sipCpp))
        sipType = sipType_KBookmarkContextMenu;
%End
"""
},
# ./solid/deviceinterface.sip
"DeviceInterface": { #DeviceInterface : QObject
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<Solid::DeviceInterface*>(sipCpp))
        {
        sipType = sipType_Solid_DeviceInterface;
        if (dynamic_cast<Solid::AcAdapter*>(sipCpp))
            sipType = sipType_Solid_AcAdapter;
        else if (dynamic_cast<Solid::AudioInterface*>(sipCpp))
            sipType = sipType_Solid_AudioInterface;
        else if (dynamic_cast<Solid::Battery*>(sipCpp))
            sipType = sipType_Solid_Battery;
        else if (dynamic_cast<Solid::Block*>(sipCpp))
            sipType = sipType_Solid_Block;
        else if (dynamic_cast<Solid::Button*>(sipCpp))
            sipType = sipType_Solid_Button;
        else if (dynamic_cast<Solid::Camera*>(sipCpp))
            sipType = sipType_Solid_Camera;
        else if (dynamic_cast<Solid::DvbInterface*>(sipCpp))
            sipType = sipType_Solid_DvbInterface;
        else if (dynamic_cast<Solid::GenericInterface*>(sipCpp))
            sipType = sipType_Solid_GenericInterface;
        else if (dynamic_cast<Solid::InternetGateway*>(sipCpp))
            sipType = sipType_Solid_InternetGateway;
        else if (dynamic_cast<Solid::NetworkInterface*>(sipCpp))
            sipType = sipType_Solid_NetworkInterface;
        else if (dynamic_cast<Solid::NetworkShare*>(sipCpp))
            sipType = sipType_Solid_NetworkShare;
        else if (dynamic_cast<Solid::PortableMediaPlayer*>(sipCpp))
            sipType = sipType_Solid_PortableMediaPlayer;
        else if (dynamic_cast<Solid::Processor*>(sipCpp))
            sipType = sipType_Solid_Processor;
        else if (dynamic_cast<Solid::SerialInterface*>(sipCpp))
            sipType = sipType_Solid_SerialInterface;
        else if (dynamic_cast<Solid::SmartCardReader*>(sipCpp))
            sipType = sipType_Solid_SmartCardReader;
        else if (dynamic_cast<Solid::StorageAccess*>(sipCpp))
            sipType = sipType_Solid_StorageAccess;
        else if (dynamic_cast<Solid::StorageDrive*>(sipCpp))
            {
            sipType = sipType_Solid_StorageDrive;
            if (dynamic_cast<Solid::OpticalDrive*>(sipCpp))
                sipType = sipType_Solid_OpticalDrive;
            }
        else if (dynamic_cast<Solid::StorageVolume*>(sipCpp))
            {
            sipType = sipType_Solid_StorageVolume;
            if (dynamic_cast<Solid::OpticalDisc*>(sipCpp))
                sipType = sipType_Solid_OpticalDisc;
            }
        else if (dynamic_cast<Solid::Video*>(sipCpp))
            sipType = sipType_Solid_Video;
        }
    else if (dynamic_cast<Solid::DeviceNotifier*>(sipCpp))
        sipType = sipType_Solid_DeviceNotifier;
    else if (dynamic_cast<Solid::Networking::Notifier*>(sipCpp))
        sipType = sipType_Solid_Networking_Notifier;
%End
"""
},
# ./solid/powermanagement.sip
"QSet<Solid::PowerManagement::SleepState>": { #QSet<Solid::PowerManagement::SleepState>
"code":
"""
%TypeHeaderCode
#include <qset.h>
#include <powermanagement.h>
%End
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    QSet<Solid::PowerManagement::SleepState> set = *sipCpp;
    int i = 0;
    foreach (Solid::PowerManagement::SleepState value, set)
    {
#if PY_MAJOR_VERSION >= 3
        PyObject *obj = PyLong_FromLong ((long) value);
#else
        PyObject *obj = PyInt_FromLong ((long) value);
#endif
        if (obj == NULL || PyList_SET_ITEM (l, i, obj) < 0)
        {
            Py_DECREF(l);

            if (obj)
                Py_DECREF(obj);

            return NULL;
        }

        Py_DECREF(obj);
        i++;
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    QSet<Solid::PowerManagement::SleepState> *qs = new QSet<Solid::PowerManagement::SleepState>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
#if PY_MAJOR_VERSION >= 3
        Solid::PowerManagement::SleepState t = (Solid::PowerManagement::SleepState)PyLong_AsLong (PyList_GET_ITEM (sipPy, i));
#else
        Solid::PowerManagement::SleepState t = (Solid::PowerManagement::SleepState)PyInt_AS_LONG (PyList_GET_ITEM (sipPy, i));
#endif
        *qs << t;

    }

    *sipCppPtr = qs;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./solid/predicate.sip
"QSet<Solid::DeviceInterface::Type>": { #QSet<Solid::DeviceInterface::Type>
"code":
"""
%TypeHeaderCode
#include <qset.h>
#include <powermanagement.h>
%End
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    QSet<Solid::DeviceInterface::Type> set = *sipCpp;
    int i = 0;
    foreach (Solid::DeviceInterface::Type value, set)
    {
#if PY_MAJOR_VERSION >= 3
        PyObject *obj = PyLong_FromLong ((long) value);
#else
        PyObject *obj = PyInt_FromLong ((long) value);
#endif
        if (obj == NULL || PyList_SET_ITEM (l, i, obj) < 0)
        {
            Py_DECREF(l);

            if (obj)
                Py_DECREF(obj);

            return NULL;
        }

        Py_DECREF(obj);
        i++;
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyList_Check(sipPy))
            return 0;
    }

    QSet<Solid::DeviceInterface::Type> *qs = new QSet<Solid::DeviceInterface::Type>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i)
    {
#if PY_MAJOR_VERSION >= 3
        Solid::DeviceInterface::Type t = (Solid::DeviceInterface::Type)PyLong_AsLong (PyList_GET_ITEM (sipPy, i));
#else
        Solid::DeviceInterface::Type t = (Solid::DeviceInterface::Type)PyInt_AS_LONG (PyList_GET_ITEM (sipPy, i));
#endif
*qs << t;

    }

    *sipCppPtr = qs;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kterminal/kterminal.sip
"KTerminal": { #KTerminal
"code":
"""
%TypeHeaderCode
#include <kde_terminal_interface.h>
#include <kde_terminal_interface_v2.h>
#include <kparts/part.h>
%End
"""
},
# ./ktexteditor/annotationinterface.sip
"AnnotationInterface": { #AnnotationInterface
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'AnnotationInterface'
    sipType = NULL;

    if (dynamic_cast<KTextEditor::AnnotationViewInterface*>(sipCpp))
        sipType = sipType_KTextEditor_AnnotationViewInterface;
%End
"""
},
# ./ktexteditor/templateinterface.sip
"TemplateInterface": { #TemplateInterface
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'TemplateInterface'
    sipType = NULL;

    if (dynamic_cast<KTextEditor::TemplateInterface2*>(sipCpp))
        sipType = sipType_KTextEditor_TemplateInterface2;
%End
"""
},
# ./ktexteditor/view.sip
"View": { #View : QWidget, KXMLGUIClient /Abstract/
"code":
"""
%TypeHeaderCode
#include <ktexteditor/view.h>

#include <ktexteditor/codecompletioninterface.h>
#include <ktexteditor/sessionconfiginterface.h>
#include <ktexteditor/texthintinterface.h>
#include <ktexteditor/annotationinterface.h>
#include <ktexteditor/configinterface.h>
#include <ktexteditor/templateinterface.h>
#include <ktexteditor/templateinterface2.h>
%End
"""
},
# ./ktexteditor/markinterface.sip
"QHash<int,KTextEditor::Mark*>": { #QHash<int,KTextEditor::Mark*>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QHash<int, KTextEditor::Mark*>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        int t1 = i.key();
        KTextEditor::Mark *t2 = i.value();

#if PY_MAJOR_VERSION >= 3
        PyObject *t1obj = PyLong_FromLong ((long)t1);
#else
        PyObject *t1obj = PyInt_FromLong ((long)t1);
#endif
        PyObject *t2obj = sipConvertFromNewInstance(t2, sipClass_KTextEditor_Mark, sipTransferObj);

        if (t2obj == NULL || PyDict_SetItem(d, t1obj, t2obj) < 0)
        {
            Py_DECREF(d);

            if (t1obj)
                Py_DECREF(t1obj);

            if (t2obj)
                Py_DECREF(t2obj);
            else
                delete t2;

            return NULL;
        }

        Py_DECREF(t1obj);
        Py_DECREF(t2obj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *t1obj, *t2obj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
        {
#if PY_MAJOR_VERSION >= 3
            if (!PyNumber_Check (t1obj))
#else
            if (!PyInt_Check (t1obj))
#endif
                return 0;

            if (!sipCanConvertToInstance(t2obj, sipClass_KTextEditor_Mark, SIP_NOT_NONE))
                return 0;
        }

        return 1;
    }

    QHash<int, KTextEditor::Mark*> *qm = new QHash<int, KTextEditor::Mark*>;

    while (PyDict_Next(sipPy, &i, &t1obj, &t2obj))
    {
        int state2;

#if PY_MAJOR_VERSION >= 3
        int t1 = PyLong_AsLong (t1obj);
#else
        int t1 = PyInt_AS_LONG (t1obj);
#endif
        KTextEditor::Mark *t2 = reinterpret_cast<KTextEditor::Mark *>(sipConvertToInstance(t2obj, sipClass_KTextEditor_Mark, sipTransferObj, SIP_NOT_NONE, &state2, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t2, sipClass_KTextEditor_Mark, state2);

            delete qm;
            return 0;
        }

        qm->insert(t1, t2);

        sipReleaseInstance(t2, sipClass_KTextEditor_Mark, state2);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./ktexteditor/document.sip
"Document": { #Document : KParts::ReadWritePart
"code":
"""
%TypeHeaderCode
#include <ktexteditor/document.h>

#include <ktexteditor/modificationinterface.h>
#include <ktexteditor/markinterface.h>
#include <ktexteditor/searchinterface.h>
#include <ktexteditor/sessionconfiginterface.h>
#include <ktexteditor/smartinterface.h>
#include <ktexteditor/templateinterface.h>
#include <ktexteditor/variableinterface.h>
#include <ktexteditor/movinginterface.h>
#include <ktexteditor/annotationinterface.h>
#include <ktexteditor/highlightinterface.h>
#include <ktexteditor/configinterface.h>
#include <ktexteditor/modeinterface.h>
#include <ktexteditor/sessionconfiginterface.h>
#include <ktexteditor/recoveryinterface.h>

%End
# ./ktexteditor/document.sip
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KTextEditor::Document*>(sipCpp))
        sipType = sipType_KTextEditor_Document;
    else if (dynamic_cast<KTextEditor::AnnotationModel*>(sipCpp))
        sipType = sipType_KTextEditor_AnnotationModel;
    else if (dynamic_cast<KTextEditor::Editor*>(sipCpp))
        sipType = sipType_KTextEditor_Editor;
    else if (dynamic_cast<KTextEditor::LoadSaveFilterCheckPlugin*>(sipCpp))
        sipType = sipType_KTextEditor_LoadSaveFilterCheckPlugin;
    else if (dynamic_cast<KTextEditor::Plugin*>(sipCpp))
        sipType = sipType_KTextEditor_Plugin;
    else if (dynamic_cast<KTextEditor::CodeCompletionModel*>(sipCpp))
        {
        sipType = sipType_KTextEditor_CodeCompletionModel;
        if (dynamic_cast<KTextEditor::CodeCompletionModel2*>(sipCpp))
            sipType = sipType_KTextEditor_CodeCompletionModel2;
        }
    else if (dynamic_cast<KTextEditor::ConfigPage*>(sipCpp))
        sipType = sipType_KTextEditor_ConfigPage;
    else if (dynamic_cast<KTextEditor::EditorChooser*>(sipCpp))
        sipType = sipType_KTextEditor_EditorChooser;
    else if (dynamic_cast<KTextEditor::View*>(sipCpp))
        sipType = sipType_KTextEditor_View;
%End
"""
},
# ./ktexteditor/codecompletionmodel.sip
"CodeCompletionModel": { #CodeCompletionModel : QAbstractItemModel
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KTextEditor::Document*>(sipCpp))
        sipType = sipType_KTextEditor_Document;
    else if (dynamic_cast<KTextEditor::AnnotationModel*>(sipCpp))
        sipType = sipType_KTextEditor_AnnotationModel;
    else if (dynamic_cast<KTextEditor::Editor*>(sipCpp))
        sipType = sipType_KTextEditor_Editor;
    else if (dynamic_cast<KTextEditor::LoadSaveFilterCheckPlugin*>(sipCpp))
        sipType = sipType_KTextEditor_LoadSaveFilterCheckPlugin;
    else if (dynamic_cast<KTextEditor::Plugin*>(sipCpp))
        sipType = sipType_KTextEditor_Plugin;
    else if (dynamic_cast<KTextEditor::CodeCompletionModel*>(sipCpp))
        {
        sipType = sipType_KTextEditor_CodeCompletionModel;
        if (dynamic_cast<KTextEditor::CodeCompletionModel2*>(sipCpp))
            sipType = sipType_KTextEditor_CodeCompletionModel2;
        }
    else if (dynamic_cast<KTextEditor::ConfigPage*>(sipCpp))
        sipType = sipType_KTextEditor_ConfigPage;
    else if (dynamic_cast<KTextEditor::EditorChooser*>(sipCpp))
        sipType = sipType_KTextEditor_EditorChooser;
    else if (dynamic_cast<KTextEditor::View*>(sipCpp))
        sipType = sipType_KTextEditor_View;
%End
"""
},
# ./ktexteditor/attribute.sip
"Attribute": { #Attribute : QTextCharFormat
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QTextFormat'
    sipType = NULL;

    if (dynamic_cast<KTextEditor::Attribute*>(sipCpp))
        sipType = sipType_KTextEditor_Attribute;
%End
"""
},
# ./kdeui/kratingwidget.sip
"KRatingWidget": { #KRatingWidget : QFrame
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KActionCategory*>(sipCpp))
        sipType = sipType_KActionCategory;
    else if (dynamic_cast<KActionCollection*>(sipCpp))
        sipType = sipType_KActionCollection;
    else if (dynamic_cast<KCategoryDrawerV2*>(sipCpp))
        {
        sipType = sipType_KCategoryDrawerV2;
        if (dynamic_cast<KCategoryDrawerV3*>(sipCpp))
            sipType = sipType_KCategoryDrawerV3;
        }
    else if (dynamic_cast<KCompletion*>(sipCpp))
        sipType = sipType_KCompletion;
    else if (dynamic_cast<KConfigDialogManager*>(sipCpp))
        sipType = sipType_KConfigDialogManager;
    else if (dynamic_cast<KConfigSkeleton*>(sipCpp))
        sipType = sipType_KConfigSkeleton;
    else if (dynamic_cast<KFind*>(sipCpp))
        {
        sipType = sipType_KFind;
        if (dynamic_cast<KReplace*>(sipCpp))
            sipType = sipType_KReplace;
        }
    else if (dynamic_cast<KGlobalAccel*>(sipCpp))
        sipType = sipType_KGlobalAccel;
    else if (dynamic_cast<KGlobalSettings*>(sipCpp))
        sipType = sipType_KGlobalSettings;
    else if (dynamic_cast<KGlobalShortcutInfo*>(sipCpp))
        sipType = sipType_KGlobalShortcutInfo;
    else if (dynamic_cast<KHelpMenu*>(sipCpp))
        sipType = sipType_KHelpMenu;
    else if (dynamic_cast<KIconLoader*>(sipCpp))
        sipType = sipType_KIconLoader;
    else if (dynamic_cast<KAbstractWidgetJobTracker*>(sipCpp))
        {
        sipType = sipType_KAbstractWidgetJobTracker;
        if (dynamic_cast<KStatusBarJobTracker*>(sipCpp))
            sipType = sipType_KStatusBarJobTracker;
        else if (dynamic_cast<KWidgetJobTracker*>(sipCpp))
            sipType = sipType_KWidgetJobTracker;
        }
    else if (dynamic_cast<KUiServerJobTracker*>(sipCpp))
        sipType = sipType_KUiServerJobTracker;
    else if (dynamic_cast<KDialogJobUiDelegate*>(sipCpp))
        sipType = sipType_KDialogJobUiDelegate;
    else if (dynamic_cast<KMessageBoxMessageHandler*>(sipCpp))
        sipType = sipType_KMessageBoxMessageHandler;
    else if (dynamic_cast<KModelIndexProxyMapper*>(sipCpp))
        sipType = sipType_KModelIndexProxyMapper;
    else if (dynamic_cast<KModifierKeyInfo*>(sipCpp))
        sipType = sipType_KModifierKeyInfo;
    else if (dynamic_cast<KNotification*>(sipCpp))
        sipType = sipType_KNotification;
    else if (dynamic_cast<KNotificationRestrictions*>(sipCpp))
        sipType = sipType_KNotificationRestrictions;
    else if (dynamic_cast<KPageWidgetItem*>(sipCpp))
        sipType = sipType_KPageWidgetItem;
    else if (dynamic_cast<KPassivePopupMessageHandler*>(sipCpp))
        sipType = sipType_KPassivePopupMessageHandler;
    else if (dynamic_cast<KPixmapSequenceOverlayPainter*>(sipCpp))
        sipType = sipType_KPixmapSequenceOverlayPainter;
    else if (dynamic_cast<KSelectionOwner*>(sipCpp))
        sipType = sipType_KSelectionOwner;
    else if (dynamic_cast<KSelectionWatcher*>(sipCpp))
        sipType = sipType_KSelectionWatcher;
    else if (dynamic_cast<KStartupInfo*>(sipCpp))
        sipType = sipType_KStartupInfo;
    else if (dynamic_cast<KStatusNotifierItem*>(sipCpp))
        sipType = sipType_KStatusNotifierItem;
    else if (dynamic_cast<KViewStateMaintainerBase*>(sipCpp))
        sipType = sipType_KViewStateMaintainerBase;
    else if (dynamic_cast<KViewStateSaver*>(sipCpp))
        sipType = sipType_KViewStateSaver;
    else if (dynamic_cast<KWallet::Wallet*>(sipCpp))
        sipType = sipType_KWallet_Wallet;
    else if (dynamic_cast<KXMLGUIFactory*>(sipCpp))
        sipType = sipType_KXMLGUIFactory;
    else if (dynamic_cast<KWidgetItemDelegate*>(sipCpp))
        sipType = sipType_KWidgetItemDelegate;
    else if (dynamic_cast<KExtendableItemDelegate*>(sipCpp))
        sipType = sipType_KExtendableItemDelegate;
    else if (dynamic_cast<KPageModel*>(sipCpp))
        {
        sipType = sipType_KPageModel;
        if (dynamic_cast<KPageWidgetModel*>(sipCpp))
            sipType = sipType_KPageWidgetModel;
        }
    else if (dynamic_cast<KDescendantsProxyModel*>(sipCpp))
        sipType = sipType_KDescendantsProxyModel;
    else if (dynamic_cast<KIdentityProxyModel*>(sipCpp))
        {
        sipType = sipType_KIdentityProxyModel;
        if (dynamic_cast<KCheckableProxyModel*>(sipCpp))
            sipType = sipType_KCheckableProxyModel;
        }
    else if (dynamic_cast<KSelectionProxyModel*>(sipCpp))
        sipType = sipType_KSelectionProxyModel;
    else if (dynamic_cast<KCategorizedSortFilterProxyModel*>(sipCpp))
        sipType = sipType_KCategorizedSortFilterProxyModel;
    else if (dynamic_cast<KRecursiveFilterProxyModel*>(sipCpp))
        sipType = sipType_KRecursiveFilterProxyModel;
    else if (dynamic_cast<KAction*>(sipCpp))
        {
        sipType = sipType_KAction;
        if (dynamic_cast<KActionMenu*>(sipCpp))
            sipType = sipType_KActionMenu;
        else if (dynamic_cast<KDualAction*>(sipCpp))
            sipType = sipType_KDualAction;
        else if (dynamic_cast<KPasteTextAction*>(sipCpp))
            sipType = sipType_KPasteTextAction;
        else if (dynamic_cast<KSelectAction*>(sipCpp))
            {
            sipType = sipType_KSelectAction;
            if (dynamic_cast<KCodecAction*>(sipCpp))
                sipType = sipType_KCodecAction;
            else if (dynamic_cast<KFontAction*>(sipCpp))
                sipType = sipType_KFontAction;
            else if (dynamic_cast<KFontSizeAction*>(sipCpp))
                sipType = sipType_KFontSizeAction;
            else if (dynamic_cast<KRecentFilesAction*>(sipCpp))
                sipType = sipType_KRecentFilesAction;
            }
        else if (dynamic_cast<KToggleAction*>(sipCpp))
            {
            sipType = sipType_KToggleAction;
            if (dynamic_cast<KToggleFullScreenAction*>(sipCpp))
                sipType = sipType_KToggleFullScreenAction;
            else if (dynamic_cast<KToggleToolBarAction*>(sipCpp))
                sipType = sipType_KToggleToolBarAction;
            }
        else if (dynamic_cast<KToolBarLabelAction*>(sipCpp))
            sipType = sipType_KToolBarLabelAction;
        else if (dynamic_cast<KToolBarPopupAction*>(sipCpp))
            sipType = sipType_KToolBarPopupAction;
        else if (dynamic_cast<KToolBarSpacerAction*>(sipCpp))
            sipType = sipType_KToolBarSpacerAction;
        }
    else if (dynamic_cast<KApplication*>(sipCpp))
        {
        sipType = sipType_KApplication;
        if (dynamic_cast<KUniqueApplication*>(sipCpp))
            sipType = sipType_KUniqueApplication;
        }
    else if (dynamic_cast<KBreadcrumbSelectionModel*>(sipCpp))
        sipType = sipType_KBreadcrumbSelectionModel;
    else if (dynamic_cast<KLinkItemSelectionModel*>(sipCpp))
        sipType = sipType_KLinkItemSelectionModel;
    else if (dynamic_cast<KStyle*>(sipCpp))
        sipType = sipType_KStyle;
    else if (dynamic_cast<KSvgRenderer*>(sipCpp))
        sipType = sipType_KSvgRenderer;
    else if (dynamic_cast<Sonnet::Highlighter*>(sipCpp))
        sipType = sipType_Sonnet_Highlighter;
    else if (dynamic_cast<KSystemTrayIcon*>(sipCpp))
        sipType = sipType_KSystemTrayIcon;
    else if (dynamic_cast<KUndoStack*>(sipCpp))
        sipType = sipType_KUndoStack;
    else if (dynamic_cast<KDateValidator*>(sipCpp))
        sipType = sipType_KDateValidator;
    else if (dynamic_cast<KFloatValidator*>(sipCpp))
        sipType = sipType_KFloatValidator;
    else if (dynamic_cast<KIntValidator*>(sipCpp))
        sipType = sipType_KIntValidator;
    else if (dynamic_cast<KMimeTypeValidator*>(sipCpp))
        sipType = sipType_KMimeTypeValidator;
    else if (dynamic_cast<KStringListValidator*>(sipCpp))
        sipType = sipType_KStringListValidator;
    else if (dynamic_cast<KDoubleValidator*>(sipCpp))
        sipType = sipType_KDoubleValidator;
    else if (dynamic_cast<KActionSelector*>(sipCpp))
        sipType = sipType_KActionSelector;
    else if (dynamic_cast<KCModule*>(sipCpp))
        sipType = sipType_KCModule;
    else if (dynamic_cast<KCapacityBar*>(sipCpp))
        sipType = sipType_KCapacityBar;
    else if (dynamic_cast<KCharSelect*>(sipCpp))
        sipType = sipType_KCharSelect;
    else if (dynamic_cast<KDateTable*>(sipCpp))
        sipType = sipType_KDateTable;
    else if (dynamic_cast<KDateTimeEdit*>(sipCpp))
        sipType = sipType_KDateTimeEdit;
    else if (dynamic_cast<KDateTimeWidget*>(sipCpp))
        sipType = sipType_KDateTimeWidget;
    else if (dynamic_cast<KDateWidget*>(sipCpp))
        sipType = sipType_KDateWidget;
    else if (dynamic_cast<KEditListWidget*>(sipCpp))
        sipType = sipType_KEditListWidget;
    else if (dynamic_cast<KFadeWidgetEffect*>(sipCpp))
        sipType = sipType_KFadeWidgetEffect;
    else if (dynamic_cast<KFilterProxySearchLine*>(sipCpp))
        sipType = sipType_KFilterProxySearchLine;
    else if (dynamic_cast<KFontChooser*>(sipCpp))
        sipType = sipType_KFontChooser;
    else if (dynamic_cast<KFontRequester*>(sipCpp))
        sipType = sipType_KFontRequester;
    else if (dynamic_cast<KKeySequenceWidget*>(sipCpp))
        sipType = sipType_KKeySequenceWidget;
    else if (dynamic_cast<KLanguageButton*>(sipCpp))
        sipType = sipType_KLanguageButton;
    else if (dynamic_cast<KLed*>(sipCpp))
        sipType = sipType_KLed;
    else if (dynamic_cast<KMultiTabBar*>(sipCpp))
        sipType = sipType_KMultiTabBar;
    else if (dynamic_cast<KNumInput*>(sipCpp))
        {
        sipType = sipType_KNumInput;
        if (dynamic_cast<KDoubleNumInput*>(sipCpp))
            sipType = sipType_KDoubleNumInput;
        else if (dynamic_cast<KIntNumInput*>(sipCpp))
            sipType = sipType_KIntNumInput;
        }
    else if (dynamic_cast<KPageView*>(sipCpp))
        {
        sipType = sipType_KPageView;
        if (dynamic_cast<KPageWidget*>(sipCpp))
            sipType = sipType_KPageWidget;
        }
    else if (dynamic_cast<KPixmapRegionSelectorWidget*>(sipCpp))
        sipType = sipType_KPixmapRegionSelectorWidget;
    else if (dynamic_cast<KPixmapSequenceWidget*>(sipCpp))
        sipType = sipType_KPixmapSequenceWidget;
    else if (dynamic_cast<KShortcutWidget*>(sipCpp))
        sipType = sipType_KShortcutWidget;
    else if (dynamic_cast<KShortcutsEditor*>(sipCpp))
        sipType = sipType_KShortcutsEditor;
    else if (dynamic_cast<KTitleWidget*>(sipCpp))
        sipType = sipType_KTitleWidget;
    else if (dynamic_cast<KTreeWidgetSearchLineWidget*>(sipCpp))
        sipType = sipType_KTreeWidgetSearchLineWidget;
    else if (dynamic_cast<KXMessages*>(sipCpp))
        sipType = sipType_KXMessages;
    else if (dynamic_cast<KXYSelector*>(sipCpp))
        {
        sipType = sipType_KXYSelector;
        if (dynamic_cast<KHueSaturationSelector*>(sipCpp))
            sipType = sipType_KHueSaturationSelector;
        }
    else if (dynamic_cast<KArrowButton*>(sipCpp))
        sipType = sipType_KArrowButton;
    else if (dynamic_cast<KColorButton*>(sipCpp))
        sipType = sipType_KColorButton;
    else if (dynamic_cast<KMultiTabBarButton*>(sipCpp))
        {
        sipType = sipType_KMultiTabBarButton;
        if (dynamic_cast<KMultiTabBarTab*>(sipCpp))
            sipType = sipType_KMultiTabBarTab;
        }
    else if (dynamic_cast<KPushButton*>(sipCpp))
        sipType = sipType_KPushButton;
    else if (dynamic_cast<KAnimatedButton*>(sipCpp))
        sipType = sipType_KAnimatedButton;
    else if (dynamic_cast<KRuler*>(sipCpp))
        sipType = sipType_KRuler;
    else if (dynamic_cast<KSelector*>(sipCpp))
        {
        sipType = sipType_KSelector;
        if (dynamic_cast<KColorValueSelector*>(sipCpp))
            sipType = sipType_KColorValueSelector;
        else if (dynamic_cast<KGradientSelector*>(sipCpp))
            sipType = sipType_KGradientSelector;
        }
    else if (dynamic_cast<KIntSpinBox*>(sipCpp))
        sipType = sipType_KIntSpinBox;
    else if (dynamic_cast<KColorCombo*>(sipCpp))
        sipType = sipType_KColorCombo;
    else if (dynamic_cast<KComboBox*>(sipCpp))
        {
        sipType = sipType_KComboBox;
        if (dynamic_cast<KDateComboBox*>(sipCpp))
            sipType = sipType_KDateComboBox;
        else if (dynamic_cast<KFontComboBox*>(sipCpp))
            sipType = sipType_KFontComboBox;
        else if (dynamic_cast<KHistoryComboBox*>(sipCpp))
            sipType = sipType_KHistoryComboBox;
        else if (dynamic_cast<KTimeComboBox*>(sipCpp))
            sipType = sipType_KTimeComboBox;
        else if (dynamic_cast<Sonnet::DictionaryComboBox*>(sipCpp))
            sipType = sipType_Sonnet_DictionaryComboBox;
        }
    else if (dynamic_cast<KDialog*>(sipCpp))
        {
        sipType = sipType_KDialog;
        if (dynamic_cast<KAboutApplicationDialog*>(sipCpp))
            sipType = sipType_KAboutApplicationDialog;
        else if (dynamic_cast<KBugReport*>(sipCpp))
            sipType = sipType_KBugReport;
        else if (dynamic_cast<KColorDialog*>(sipCpp))
            sipType = sipType_KColorDialog;
        else if (dynamic_cast<KEditToolBar*>(sipCpp))
            sipType = sipType_KEditToolBar;
        else if (dynamic_cast<KFindDialog*>(sipCpp))
            {
            sipType = sipType_KFindDialog;
            if (dynamic_cast<KReplaceDialog*>(sipCpp))
                sipType = sipType_KReplaceDialog;
            }
        else if (dynamic_cast<KFontDialog*>(sipCpp))
            sipType = sipType_KFontDialog;
        else if (dynamic_cast<KNewPasswordDialog*>(sipCpp))
            sipType = sipType_KNewPasswordDialog;
        else if (dynamic_cast<KPageDialog*>(sipCpp))
            {
            sipType = sipType_KPageDialog;
            if (dynamic_cast<KAssistantDialog*>(sipCpp))
                sipType = sipType_KAssistantDialog;
            else if (dynamic_cast<KConfigDialog*>(sipCpp))
                sipType = sipType_KConfigDialog;
            }
        else if (dynamic_cast<KPasswordDialog*>(sipCpp))
            sipType = sipType_KPasswordDialog;
        else if (dynamic_cast<KPixmapRegionSelectorDialog*>(sipCpp))
            sipType = sipType_KPixmapRegionSelectorDialog;
        else if (dynamic_cast<KProgressDialog*>(sipCpp))
            sipType = sipType_KProgressDialog;
        else if (dynamic_cast<KShortcutsDialog*>(sipCpp))
            sipType = sipType_KShortcutsDialog;
        else if (dynamic_cast<KTipDialog*>(sipCpp))
            sipType = sipType_KTipDialog;
        else if (dynamic_cast<Sonnet::ConfigDialog*>(sipCpp))
            sipType = sipType_Sonnet_ConfigDialog;
        else if (dynamic_cast<Sonnet::Dialog*>(sipCpp))
            sipType = sipType_Sonnet_Dialog;
        }
    else if (dynamic_cast<KDialogButtonBox*>(sipCpp))
        sipType = sipType_KDialogButtonBox;
    else if (dynamic_cast<KColorPatch*>(sipCpp))
        sipType = sipType_KColorPatch;
    else if (dynamic_cast<KDatePicker*>(sipCpp))
        sipType = sipType_KDatePicker;
    else if (dynamic_cast<KHBox*>(sipCpp))
        {
        sipType = sipType_KHBox;
        if (dynamic_cast<KVBox*>(sipCpp))
            sipType = sipType_KVBox;
        }
    else if (dynamic_cast<KMessageWidget*>(sipCpp))
        sipType = sipType_KMessageWidget;
    else if (dynamic_cast<KPassivePopup*>(sipCpp))
        sipType = sipType_KPassivePopup;
    else if (dynamic_cast<KPlotWidget*>(sipCpp))
        sipType = sipType_KPlotWidget;
    else if (dynamic_cast<KPopupFrame*>(sipCpp))
        sipType = sipType_KPopupFrame;
    else if (dynamic_cast<KRatingWidget*>(sipCpp))
        sipType = sipType_KRatingWidget;
    else if (dynamic_cast<KSeparator*>(sipCpp))
        sipType = sipType_KSeparator;
    else if (dynamic_cast<KCategorizedView*>(sipCpp))
        sipType = sipType_KCategorizedView;
    else if (dynamic_cast<KListWidget*>(sipCpp))
        {
        sipType = sipType_KListWidget;
        if (dynamic_cast<KCompletionBox*>(sipCpp))
            sipType = sipType_KCompletionBox;
        }
    else if (dynamic_cast<KColorCells*>(sipCpp))
        sipType = sipType_KColorCells;
    else if (dynamic_cast<KTimeZoneWidget*>(sipCpp))
        sipType = sipType_KTimeZoneWidget;
    else if (dynamic_cast<KTextEdit*>(sipCpp))
        {
        sipType = sipType_KTextEdit;
        if (dynamic_cast<KRichTextEdit*>(sipCpp))
            {
            sipType = sipType_KRichTextEdit;
            if (dynamic_cast<KRichTextWidget*>(sipCpp))
                sipType = sipType_KRichTextWidget;
            }
        }
    else if (dynamic_cast<KTextBrowser*>(sipCpp))
        sipType = sipType_KTextBrowser;
    else if (dynamic_cast<KSqueezedTextLabel*>(sipCpp))
        sipType = sipType_KSqueezedTextLabel;
    else if (dynamic_cast<KUrlLabel*>(sipCpp))
        sipType = sipType_KUrlLabel;
    else if (dynamic_cast<KButtonGroup*>(sipCpp))
        sipType = sipType_KButtonGroup;
    else if (dynamic_cast<KEditListBox*>(sipCpp))
        sipType = sipType_KEditListBox;
    else if (dynamic_cast<KLineEdit*>(sipCpp))
        {
        sipType = sipType_KLineEdit;
        if (dynamic_cast<KListWidgetSearchLine*>(sipCpp))
            sipType = sipType_KListWidgetSearchLine;
        else if (dynamic_cast<KRestrictedLine*>(sipCpp))
            sipType = sipType_KRestrictedLine;
        else if (dynamic_cast<KTreeWidgetSearchLine*>(sipCpp))
            sipType = sipType_KTreeWidgetSearchLine;
        }
    else if (dynamic_cast<KMainWindow*>(sipCpp))
        {
        sipType = sipType_KMainWindow;
        if (dynamic_cast<KXmlGuiWindow*>(sipCpp))
            sipType = sipType_KXmlGuiWindow;
        }
    else if (dynamic_cast<KMenu*>(sipCpp))
        sipType = sipType_KMenu;
    else if (dynamic_cast<KMenuBar*>(sipCpp))
        sipType = sipType_KMenuBar;
    else if (dynamic_cast<KSplashScreen*>(sipCpp))
        sipType = sipType_KSplashScreen;
    else if (dynamic_cast<KStatusBar*>(sipCpp))
        sipType = sipType_KStatusBar;
    else if (dynamic_cast<KTabBar*>(sipCpp))
        sipType = sipType_KTabBar;
    else if (dynamic_cast<KTabWidget*>(sipCpp))
        sipType = sipType_KTabWidget;
    else if (dynamic_cast<KToolBar*>(sipCpp))
        sipType = sipType_KToolBar;
    else if (dynamic_cast<Sonnet::ConfigWidget*>(sipCpp))
        sipType = sipType_Sonnet_ConfigWidget;
%End
"""
},
# ./kdeui/kpixmapcache.sip
"KPixmapCache": { #KPixmapCache
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KPixmapCache'
    sipType = NULL;

    if (dynamic_cast<KIconCache*>(sipCpp))
        sipType = sipType_KIconCache;
%End
"""
},
# ./kdeui/kwidgetitemdelegate.sip
"QList<QEvent::Type>": { #QList<QEvent::Type>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i) {
        PyObject *pobj;

#if PY_MAJOR_VERSION >= 3
        if ((pobj = PyLong_FromLong ((long)sipCpp->value(i))) == NULL) {
#else
        if ((pobj = PyInt_FromLong ((long)sipCpp->value(i))) == NULL) {
#endif
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QList<QEvent::Type> *ql = new QList<QEvent::Type>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
#if PY_MAJOR_VERSION >= 3
        ql->append((QEvent::Type)PyLong_AsLong(PyList_GET_ITEM(sipPy, i)));
#else
        ql->append((QEvent::Type)PyInt_AS_LONG (PyList_GET_ITEM(sipPy, i)));
#endif
    }

    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdeui/kcompletion.sip
"QMap<KCompletionBase::KeyBindingType,KShortcut>": { #QMap<KCompletionBase::KeyBindingType,KShortcut>
"code":
"""
%ConvertFromTypeCode
    // Create the dictionary.
    PyObject *d = PyDict_New();

    if (!d)
        return NULL;

    // Set the dictionary elements.
    QMap<KCompletionBase::KeyBindingType, KShortcut>::const_iterator i = sipCpp->constBegin();

    while (i != sipCpp->constEnd())
    {
        KShortcut *t = new KShortcut(i.value());

#if PY_MAJOR_VERSION >= 3
        PyObject *kobj = PyLong_FromLong((int)i.key());
#else
        PyObject *kobj = PyInt_FromLong((int)i.key());
#endif
        PyObject *tobj = sipConvertFromNewInstance(t, sipClass_KShortcut, sipTransferObj);

        if (kobj == NULL || tobj == NULL || PyDict_SetItem(d, kobj, tobj) < 0)
        {
            Py_DECREF(d);

            if (kobj)
                Py_DECREF(kobj);

            if (tobj)
                Py_DECREF(tobj);
            else
                delete t;

            return NULL;
        }

        Py_DECREF(kobj);
        Py_DECREF(tobj);

        ++i;
    }

    return d;
%End
%ConvertToTypeCode
    PyObject *kobj, *tobj;
    SIP_SSIZE_T i = 0;

    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
    {
        if (!PyDict_Check(sipPy))
            return 0;

        while (PyDict_Next(sipPy, &i, &kobj, &tobj))
            if (!sipCanConvertToInstance(tobj, sipClass_KShortcut, SIP_NOT_NONE))
                return 0;

        return 1;
    }

    QMap<KCompletionBase::KeyBindingType, KShortcut> *qm = new QMap<KCompletionBase::KeyBindingType, KShortcut>;

    while (PyDict_Next(sipPy, &i, &kobj, &tobj))
    {
        int state;
#if PY_MAJOR_VERSION >= 3
        int k = PyLong_AsLong(kobj);
#else
        int k = PyInt_AsLong(kobj);
#endif
        KShortcut *t = reinterpret_cast<KShortcut *>(sipConvertToInstance(tobj, sipClass_KShortcut, sipTransferObj, SIP_NOT_NONE, &state, sipIsErr));

        if (*sipIsErr)
        {
            sipReleaseInstance(t, sipClass_KShortcut, state);

            delete qm;
            return 0;
        }

        qm->insert((KCompletionBase::KeyBindingType)k, *t);

        sipReleaseInstance(t, sipClass_KShortcut, state);
    }

    *sipCppPtr = qm;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdeui/kabstractwidgetjobtracker.sip
"KAbstractWidgetJobTracker": { #KAbstractWidgetJobTracker : KJobTrackerInterface
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QObject'
    sipType = NULL;

    if (dynamic_cast<KActionCategory*>(sipCpp))
        sipType = sipType_KActionCategory;
    else if (dynamic_cast<KActionCollection*>(sipCpp))
        sipType = sipType_KActionCollection;
    else if (dynamic_cast<KCategoryDrawerV2*>(sipCpp))
        {
        sipType = sipType_KCategoryDrawerV2;
        if (dynamic_cast<KCategoryDrawerV3*>(sipCpp))
            sipType = sipType_KCategoryDrawerV3;
        }
    else if (dynamic_cast<KCompletion*>(sipCpp))
        sipType = sipType_KCompletion;
    else if (dynamic_cast<KConfigDialogManager*>(sipCpp))
        sipType = sipType_KConfigDialogManager;
    else if (dynamic_cast<KConfigSkeleton*>(sipCpp))
        sipType = sipType_KConfigSkeleton;
    else if (dynamic_cast<KFind*>(sipCpp))
        {
        sipType = sipType_KFind;
        if (dynamic_cast<KReplace*>(sipCpp))
            sipType = sipType_KReplace;
        }
    else if (dynamic_cast<KGlobalAccel*>(sipCpp))
        sipType = sipType_KGlobalAccel;
    else if (dynamic_cast<KGlobalSettings*>(sipCpp))
        sipType = sipType_KGlobalSettings;
    else if (dynamic_cast<KGlobalShortcutInfo*>(sipCpp))
        sipType = sipType_KGlobalShortcutInfo;
    else if (dynamic_cast<KHelpMenu*>(sipCpp))
        sipType = sipType_KHelpMenu;
    else if (dynamic_cast<KIconLoader*>(sipCpp))
        sipType = sipType_KIconLoader;
    else if (dynamic_cast<KAbstractWidgetJobTracker*>(sipCpp))
        {
        sipType = sipType_KAbstractWidgetJobTracker;
        if (dynamic_cast<KStatusBarJobTracker*>(sipCpp))
            sipType = sipType_KStatusBarJobTracker;
        else if (dynamic_cast<KWidgetJobTracker*>(sipCpp))
            sipType = sipType_KWidgetJobTracker;
        }
    else if (dynamic_cast<KUiServerJobTracker*>(sipCpp))
        sipType = sipType_KUiServerJobTracker;
    else if (dynamic_cast<KDialogJobUiDelegate*>(sipCpp))
        sipType = sipType_KDialogJobUiDelegate;
    else if (dynamic_cast<KMessageBoxMessageHandler*>(sipCpp))
        sipType = sipType_KMessageBoxMessageHandler;
    else if (dynamic_cast<KModelIndexProxyMapper*>(sipCpp))
        sipType = sipType_KModelIndexProxyMapper;
    else if (dynamic_cast<KModifierKeyInfo*>(sipCpp))
        sipType = sipType_KModifierKeyInfo;
    else if (dynamic_cast<KNotification*>(sipCpp))
        sipType = sipType_KNotification;
    else if (dynamic_cast<KNotificationRestrictions*>(sipCpp))
        sipType = sipType_KNotificationRestrictions;
    else if (dynamic_cast<KPageWidgetItem*>(sipCpp))
        sipType = sipType_KPageWidgetItem;
    else if (dynamic_cast<KPassivePopupMessageHandler*>(sipCpp))
        sipType = sipType_KPassivePopupMessageHandler;
    else if (dynamic_cast<KPixmapSequenceOverlayPainter*>(sipCpp))
        sipType = sipType_KPixmapSequenceOverlayPainter;
    else if (dynamic_cast<KSelectionOwner*>(sipCpp))
        sipType = sipType_KSelectionOwner;
    else if (dynamic_cast<KSelectionWatcher*>(sipCpp))
        sipType = sipType_KSelectionWatcher;
    else if (dynamic_cast<KStartupInfo*>(sipCpp))
        sipType = sipType_KStartupInfo;
    else if (dynamic_cast<KStatusNotifierItem*>(sipCpp))
        sipType = sipType_KStatusNotifierItem;
    else if (dynamic_cast<KViewStateMaintainerBase*>(sipCpp))
        sipType = sipType_KViewStateMaintainerBase;
    else if (dynamic_cast<KViewStateSaver*>(sipCpp))
        sipType = sipType_KViewStateSaver;
    else if (dynamic_cast<KWallet::Wallet*>(sipCpp))
        sipType = sipType_KWallet_Wallet;
    else if (dynamic_cast<KXMLGUIFactory*>(sipCpp))
        sipType = sipType_KXMLGUIFactory;
    else if (dynamic_cast<KWidgetItemDelegate*>(sipCpp))
        sipType = sipType_KWidgetItemDelegate;
    else if (dynamic_cast<KExtendableItemDelegate*>(sipCpp))
        sipType = sipType_KExtendableItemDelegate;
    else if (dynamic_cast<KPageModel*>(sipCpp))
        {
        sipType = sipType_KPageModel;
        if (dynamic_cast<KPageWidgetModel*>(sipCpp))
            sipType = sipType_KPageWidgetModel;
        }
    else if (dynamic_cast<KDescendantsProxyModel*>(sipCpp))
        sipType = sipType_KDescendantsProxyModel;
    else if (dynamic_cast<KIdentityProxyModel*>(sipCpp))
        {
        sipType = sipType_KIdentityProxyModel;
        if (dynamic_cast<KCheckableProxyModel*>(sipCpp))
            sipType = sipType_KCheckableProxyModel;
        }
    else if (dynamic_cast<KSelectionProxyModel*>(sipCpp))
        sipType = sipType_KSelectionProxyModel;
    else if (dynamic_cast<KCategorizedSortFilterProxyModel*>(sipCpp))
        sipType = sipType_KCategorizedSortFilterProxyModel;
    else if (dynamic_cast<KRecursiveFilterProxyModel*>(sipCpp))
        sipType = sipType_KRecursiveFilterProxyModel;
    else if (dynamic_cast<KAction*>(sipCpp))
        {
        sipType = sipType_KAction;
        if (dynamic_cast<KActionMenu*>(sipCpp))
            sipType = sipType_KActionMenu;
        else if (dynamic_cast<KDualAction*>(sipCpp))
            sipType = sipType_KDualAction;
        else if (dynamic_cast<KPasteTextAction*>(sipCpp))
            sipType = sipType_KPasteTextAction;
        else if (dynamic_cast<KSelectAction*>(sipCpp))
            {
            sipType = sipType_KSelectAction;
            if (dynamic_cast<KCodecAction*>(sipCpp))
                sipType = sipType_KCodecAction;
            else if (dynamic_cast<KFontAction*>(sipCpp))
                sipType = sipType_KFontAction;
            else if (dynamic_cast<KFontSizeAction*>(sipCpp))
                sipType = sipType_KFontSizeAction;
            else if (dynamic_cast<KRecentFilesAction*>(sipCpp))
                sipType = sipType_KRecentFilesAction;
            }
        else if (dynamic_cast<KToggleAction*>(sipCpp))
            {
            sipType = sipType_KToggleAction;
            if (dynamic_cast<KToggleFullScreenAction*>(sipCpp))
                sipType = sipType_KToggleFullScreenAction;
            else if (dynamic_cast<KToggleToolBarAction*>(sipCpp))
                sipType = sipType_KToggleToolBarAction;
            }
        else if (dynamic_cast<KToolBarLabelAction*>(sipCpp))
            sipType = sipType_KToolBarLabelAction;
        else if (dynamic_cast<KToolBarPopupAction*>(sipCpp))
            sipType = sipType_KToolBarPopupAction;
        else if (dynamic_cast<KToolBarSpacerAction*>(sipCpp))
            sipType = sipType_KToolBarSpacerAction;
        }
    else if (dynamic_cast<KApplication*>(sipCpp))
        {
        sipType = sipType_KApplication;
        if (dynamic_cast<KUniqueApplication*>(sipCpp))
            sipType = sipType_KUniqueApplication;
        }
    else if (dynamic_cast<KBreadcrumbSelectionModel*>(sipCpp))
        sipType = sipType_KBreadcrumbSelectionModel;
    else if (dynamic_cast<KLinkItemSelectionModel*>(sipCpp))
        sipType = sipType_KLinkItemSelectionModel;
    else if (dynamic_cast<KStyle*>(sipCpp))
        sipType = sipType_KStyle;
    else if (dynamic_cast<KSvgRenderer*>(sipCpp))
        sipType = sipType_KSvgRenderer;
    else if (dynamic_cast<Sonnet::Highlighter*>(sipCpp))
        sipType = sipType_Sonnet_Highlighter;
    else if (dynamic_cast<KSystemTrayIcon*>(sipCpp))
        sipType = sipType_KSystemTrayIcon;
    else if (dynamic_cast<KUndoStack*>(sipCpp))
        sipType = sipType_KUndoStack;
    else if (dynamic_cast<KDateValidator*>(sipCpp))
        sipType = sipType_KDateValidator;
    else if (dynamic_cast<KFloatValidator*>(sipCpp))
        sipType = sipType_KFloatValidator;
    else if (dynamic_cast<KIntValidator*>(sipCpp))
        sipType = sipType_KIntValidator;
    else if (dynamic_cast<KMimeTypeValidator*>(sipCpp))
        sipType = sipType_KMimeTypeValidator;
    else if (dynamic_cast<KStringListValidator*>(sipCpp))
        sipType = sipType_KStringListValidator;
    else if (dynamic_cast<KDoubleValidator*>(sipCpp))
        sipType = sipType_KDoubleValidator;
    else if (dynamic_cast<KActionSelector*>(sipCpp))
        sipType = sipType_KActionSelector;
    else if (dynamic_cast<KCModule*>(sipCpp))
        sipType = sipType_KCModule;
    else if (dynamic_cast<KCapacityBar*>(sipCpp))
        sipType = sipType_KCapacityBar;
    else if (dynamic_cast<KCharSelect*>(sipCpp))
        sipType = sipType_KCharSelect;
    else if (dynamic_cast<KDateTable*>(sipCpp))
        sipType = sipType_KDateTable;
    else if (dynamic_cast<KDateTimeEdit*>(sipCpp))
        sipType = sipType_KDateTimeEdit;
    else if (dynamic_cast<KDateTimeWidget*>(sipCpp))
        sipType = sipType_KDateTimeWidget;
    else if (dynamic_cast<KDateWidget*>(sipCpp))
        sipType = sipType_KDateWidget;
    else if (dynamic_cast<KEditListWidget*>(sipCpp))
        sipType = sipType_KEditListWidget;
    else if (dynamic_cast<KFadeWidgetEffect*>(sipCpp))
        sipType = sipType_KFadeWidgetEffect;
    else if (dynamic_cast<KFilterProxySearchLine*>(sipCpp))
        sipType = sipType_KFilterProxySearchLine;
    else if (dynamic_cast<KFontChooser*>(sipCpp))
        sipType = sipType_KFontChooser;
    else if (dynamic_cast<KFontRequester*>(sipCpp))
        sipType = sipType_KFontRequester;
    else if (dynamic_cast<KKeySequenceWidget*>(sipCpp))
        sipType = sipType_KKeySequenceWidget;
    else if (dynamic_cast<KLanguageButton*>(sipCpp))
        sipType = sipType_KLanguageButton;
    else if (dynamic_cast<KLed*>(sipCpp))
        sipType = sipType_KLed;
    else if (dynamic_cast<KMultiTabBar*>(sipCpp))
        sipType = sipType_KMultiTabBar;
    else if (dynamic_cast<KNumInput*>(sipCpp))
        {
        sipType = sipType_KNumInput;
        if (dynamic_cast<KDoubleNumInput*>(sipCpp))
            sipType = sipType_KDoubleNumInput;
        else if (dynamic_cast<KIntNumInput*>(sipCpp))
            sipType = sipType_KIntNumInput;
        }
    else if (dynamic_cast<KPageView*>(sipCpp))
        {
        sipType = sipType_KPageView;
        if (dynamic_cast<KPageWidget*>(sipCpp))
            sipType = sipType_KPageWidget;
        }
    else if (dynamic_cast<KPixmapRegionSelectorWidget*>(sipCpp))
        sipType = sipType_KPixmapRegionSelectorWidget;
    else if (dynamic_cast<KPixmapSequenceWidget*>(sipCpp))
        sipType = sipType_KPixmapSequenceWidget;
    else if (dynamic_cast<KShortcutWidget*>(sipCpp))
        sipType = sipType_KShortcutWidget;
    else if (dynamic_cast<KShortcutsEditor*>(sipCpp))
        sipType = sipType_KShortcutsEditor;
    else if (dynamic_cast<KTitleWidget*>(sipCpp))
        sipType = sipType_KTitleWidget;
    else if (dynamic_cast<KTreeWidgetSearchLineWidget*>(sipCpp))
        sipType = sipType_KTreeWidgetSearchLineWidget;
    else if (dynamic_cast<KXMessages*>(sipCpp))
        sipType = sipType_KXMessages;
    else if (dynamic_cast<KXYSelector*>(sipCpp))
        {
        sipType = sipType_KXYSelector;
        if (dynamic_cast<KHueSaturationSelector*>(sipCpp))
            sipType = sipType_KHueSaturationSelector;
        }
    else if (dynamic_cast<KArrowButton*>(sipCpp))
        sipType = sipType_KArrowButton;
    else if (dynamic_cast<KColorButton*>(sipCpp))
        sipType = sipType_KColorButton;
    else if (dynamic_cast<KMultiTabBarButton*>(sipCpp))
        {
        sipType = sipType_KMultiTabBarButton;
        if (dynamic_cast<KMultiTabBarTab*>(sipCpp))
            sipType = sipType_KMultiTabBarTab;
        }
    else if (dynamic_cast<KPushButton*>(sipCpp))
        sipType = sipType_KPushButton;
    else if (dynamic_cast<KAnimatedButton*>(sipCpp))
        sipType = sipType_KAnimatedButton;
    else if (dynamic_cast<KRuler*>(sipCpp))
        sipType = sipType_KRuler;
    else if (dynamic_cast<KSelector*>(sipCpp))
        {
        sipType = sipType_KSelector;
        if (dynamic_cast<KColorValueSelector*>(sipCpp))
            sipType = sipType_KColorValueSelector;
        else if (dynamic_cast<KGradientSelector*>(sipCpp))
            sipType = sipType_KGradientSelector;
        }
    else if (dynamic_cast<KIntSpinBox*>(sipCpp))
        sipType = sipType_KIntSpinBox;
    else if (dynamic_cast<KColorCombo*>(sipCpp))
        sipType = sipType_KColorCombo;
    else if (dynamic_cast<KComboBox*>(sipCpp))
        {
        sipType = sipType_KComboBox;
        if (dynamic_cast<KDateComboBox*>(sipCpp))
            sipType = sipType_KDateComboBox;
        else if (dynamic_cast<KFontComboBox*>(sipCpp))
            sipType = sipType_KFontComboBox;
        else if (dynamic_cast<KHistoryComboBox*>(sipCpp))
            sipType = sipType_KHistoryComboBox;
        else if (dynamic_cast<KTimeComboBox*>(sipCpp))
            sipType = sipType_KTimeComboBox;
        else if (dynamic_cast<Sonnet::DictionaryComboBox*>(sipCpp))
            sipType = sipType_Sonnet_DictionaryComboBox;
        }
    else if (dynamic_cast<KDialog*>(sipCpp))
        {
        sipType = sipType_KDialog;
        if (dynamic_cast<KAboutApplicationDialog*>(sipCpp))
            sipType = sipType_KAboutApplicationDialog;
        else if (dynamic_cast<KBugReport*>(sipCpp))
            sipType = sipType_KBugReport;
        else if (dynamic_cast<KColorDialog*>(sipCpp))
            sipType = sipType_KColorDialog;
        else if (dynamic_cast<KEditToolBar*>(sipCpp))
            sipType = sipType_KEditToolBar;
        else if (dynamic_cast<KFindDialog*>(sipCpp))
            {
            sipType = sipType_KFindDialog;
            if (dynamic_cast<KReplaceDialog*>(sipCpp))
                sipType = sipType_KReplaceDialog;
            }
        else if (dynamic_cast<KFontDialog*>(sipCpp))
            sipType = sipType_KFontDialog;
        else if (dynamic_cast<KNewPasswordDialog*>(sipCpp))
            sipType = sipType_KNewPasswordDialog;
        else if (dynamic_cast<KPageDialog*>(sipCpp))
            {
            sipType = sipType_KPageDialog;
            if (dynamic_cast<KAssistantDialog*>(sipCpp))
                sipType = sipType_KAssistantDialog;
            else if (dynamic_cast<KConfigDialog*>(sipCpp))
                sipType = sipType_KConfigDialog;
            }
        else if (dynamic_cast<KPasswordDialog*>(sipCpp))
            sipType = sipType_KPasswordDialog;
        else if (dynamic_cast<KPixmapRegionSelectorDialog*>(sipCpp))
            sipType = sipType_KPixmapRegionSelectorDialog;
        else if (dynamic_cast<KProgressDialog*>(sipCpp))
            sipType = sipType_KProgressDialog;
        else if (dynamic_cast<KShortcutsDialog*>(sipCpp))
            sipType = sipType_KShortcutsDialog;
        else if (dynamic_cast<KTipDialog*>(sipCpp))
            sipType = sipType_KTipDialog;
        else if (dynamic_cast<Sonnet::ConfigDialog*>(sipCpp))
            sipType = sipType_Sonnet_ConfigDialog;
        else if (dynamic_cast<Sonnet::Dialog*>(sipCpp))
            sipType = sipType_Sonnet_Dialog;
        }
    else if (dynamic_cast<KDialogButtonBox*>(sipCpp))
        sipType = sipType_KDialogButtonBox;
    else if (dynamic_cast<KColorPatch*>(sipCpp))
        sipType = sipType_KColorPatch;
    else if (dynamic_cast<KDatePicker*>(sipCpp))
        sipType = sipType_KDatePicker;
    else if (dynamic_cast<KHBox*>(sipCpp))
        {
        sipType = sipType_KHBox;
        if (dynamic_cast<KVBox*>(sipCpp))
            sipType = sipType_KVBox;
        }
    else if (dynamic_cast<KMessageWidget*>(sipCpp))
        sipType = sipType_KMessageWidget;
    else if (dynamic_cast<KPassivePopup*>(sipCpp))
        sipType = sipType_KPassivePopup;
    else if (dynamic_cast<KPlotWidget*>(sipCpp))
        sipType = sipType_KPlotWidget;
    else if (dynamic_cast<KPopupFrame*>(sipCpp))
        sipType = sipType_KPopupFrame;
    else if (dynamic_cast<KRatingWidget*>(sipCpp))
        sipType = sipType_KRatingWidget;
    else if (dynamic_cast<KSeparator*>(sipCpp))
        sipType = sipType_KSeparator;
    else if (dynamic_cast<KCategorizedView*>(sipCpp))
        sipType = sipType_KCategorizedView;
    else if (dynamic_cast<KListWidget*>(sipCpp))
        {
        sipType = sipType_KListWidget;
        if (dynamic_cast<KCompletionBox*>(sipCpp))
            sipType = sipType_KCompletionBox;
        }
    else if (dynamic_cast<KColorCells*>(sipCpp))
        sipType = sipType_KColorCells;
    else if (dynamic_cast<KTimeZoneWidget*>(sipCpp))
        sipType = sipType_KTimeZoneWidget;
    else if (dynamic_cast<KTextEdit*>(sipCpp))
        {
        sipType = sipType_KTextEdit;
        if (dynamic_cast<KRichTextEdit*>(sipCpp))
            {
            sipType = sipType_KRichTextEdit;
            if (dynamic_cast<KRichTextWidget*>(sipCpp))
                sipType = sipType_KRichTextWidget;
            }
        }
    else if (dynamic_cast<KTextBrowser*>(sipCpp))
        sipType = sipType_KTextBrowser;
    else if (dynamic_cast<KSqueezedTextLabel*>(sipCpp))
        sipType = sipType_KSqueezedTextLabel;
    else if (dynamic_cast<KUrlLabel*>(sipCpp))
        sipType = sipType_KUrlLabel;
    else if (dynamic_cast<KButtonGroup*>(sipCpp))
        sipType = sipType_KButtonGroup;
    else if (dynamic_cast<KEditListBox*>(sipCpp))
        sipType = sipType_KEditListBox;
    else if (dynamic_cast<KLineEdit*>(sipCpp))
        {
        sipType = sipType_KLineEdit;
        if (dynamic_cast<KListWidgetSearchLine*>(sipCpp))
            sipType = sipType_KListWidgetSearchLine;
        else if (dynamic_cast<KRestrictedLine*>(sipCpp))
            sipType = sipType_KRestrictedLine;
        else if (dynamic_cast<KTreeWidgetSearchLine*>(sipCpp))
            sipType = sipType_KTreeWidgetSearchLine;
        }
    else if (dynamic_cast<KMainWindow*>(sipCpp))
        {
        sipType = sipType_KMainWindow;
        if (dynamic_cast<KXmlGuiWindow*>(sipCpp))
            sipType = sipType_KXmlGuiWindow;
        }
    else if (dynamic_cast<KMenu*>(sipCpp))
        sipType = sipType_KMenu;
    else if (dynamic_cast<KMenuBar*>(sipCpp))
        sipType = sipType_KMenuBar;
    else if (dynamic_cast<KSplashScreen*>(sipCpp))
        sipType = sipType_KSplashScreen;
    else if (dynamic_cast<KStatusBar*>(sipCpp))
        sipType = sipType_KStatusBar;
    else if (dynamic_cast<KTabBar*>(sipCpp))
        sipType = sipType_KTabBar;
    else if (dynamic_cast<KTabWidget*>(sipCpp))
        sipType = sipType_KTabWidget;
    else if (dynamic_cast<KToolBar*>(sipCpp))
        sipType = sipType_KToolBar;
    else if (dynamic_cast<Sonnet::ConfigWidget*>(sipCpp))
        sipType = sipType_Sonnet_ConfigWidget;
%End
"""
},
# ./kdeui/kcursor.sip
"KCursor": { #KCursor : QCursor
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QCursor'
    sipType = NULL;

    if (dynamic_cast<KCursor*>(sipCpp))
        sipType = sipType_KCursor;
%End
"""
},
# ./kdeui/kapplication.sip
"KApplication": { #KApplication : QApplication
"code":
"""
%TypeCode
// Convert a Python argv list to a conventional C argc count and argv array.
static char **kdeui_ArgvToC(PyObject *argvlist, int &argc)
{
    char **argv;

    argc = PyList_GET_SIZE(argvlist);

    // Allocate space for two copies of the argument pointers, plus the
    // terminating NULL.
    if ((argv = (char **)sipMalloc(2 * (argc + 1) * sizeof (char *))) == NULL)
        return NULL;

    // Convert the list.
    for (int a = 0; a < argc; ++a)
    {
        char *arg;
#if PY_MAJOR_VERSION >= 3
        PyObject *utf8bytes = PyUnicode_AsUTF8String(PyList_GetItem(argvlist,a));
        arg = PyBytes_AsString(utf8bytes);
#else
        arg = PyString_AsString(PyList_GetItem(argvlist,a));
#endif
        // Get the argument and allocate memory for it.
        if (arg == NULL ||
            (argv[a] = (char *)sipMalloc(strlen(arg) + 1)) == NULL)
            return NULL;

        // Copy the argument and save a pointer to it.
        strcpy(argv[a], arg);
        argv[a + argc + 1] = argv[a];
#if PY_MAJOR_VERSION >= 3
        Py_DECREF(utf8bytes);
#endif
    }

    argv[argc + argc + 1] = argv[argc] = NULL;

    return argv;
}


// Remove arguments from the Python argv list that have been removed from the
// C argv array.
static void kdeui_UpdatePyArgv(PyObject *argvlist, int argc, char **argv)
{
    for (int a = 0, na = 0; a < argc; ++a)
    {
        // See if it was removed.
        if (argv[na] == argv[a + argc + 1])
            ++na;
        else
            PyList_SetSlice(argvlist, na, na + 1, NULL);
    }
}
%End
"""
},
# ./kdeui/kstandardaction.sip
"QList<KStandardAction::StandardAction>": { #QList<KStandardAction::StandardAction>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i)
    {
        PyObject *pobj;
#if PY_MAJOR_VERSION >= 3
        if ((pobj = PyLong_FromLong ((long)sipCpp->value(i))) == NULL) {
#else
        if ((pobj = PyInt_FromLong ((long)sipCpp->value(i))) == NULL) {
#endif
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QList<KStandardAction::StandardAction> *ql = new QList<KStandardAction::StandardAction>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
#if PY_MAJOR_VERSION >= 3
        ql->append((KStandardAction::StandardAction)PyLong_AsLong (PyList_GET_ITEM(sipPy, i)));
#else
        ql->append((KStandardAction::StandardAction)PyInt_AS_LONG (PyList_GET_ITEM(sipPy, i)));
#endif
    }
    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
# ./kdeui/kicon.sip
"KIcon": { #KIcon : QIcon
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'QIcon'
    sipType = NULL;

    if (dynamic_cast<KIcon*>(sipCpp))
        sipType = sipType_KIcon;
%End
"""
},
# ./kdeui/kiconcache.sip
"KIconCache": { #KIconCache : KPixmapCache
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KPixmapCache'
    sipType = NULL;

    if (dynamic_cast<KIconCache*>(sipCpp))
        sipType = sipType_KIconCache;
%End
"""
},
# ./kdeui/kconfigskeleton.sip
"KConfigSkeleton": { #KConfigSkeleton : KCoreConfigSkeleton
"code":
"""
%ConvertToSubClassCode
    // CTSCC for subclasses of 'KConfigSkeletonItem'
    sipType = NULL;

    if (dynamic_cast<KConfigSkeleton::ItemColor*>(sipCpp))
        sipType = sipType_KConfigSkeleton_ItemColor;
    else if (dynamic_cast<KConfigSkeleton::ItemFont*>(sipCpp))
        sipType = sipType_KConfigSkeleton_ItemFont;
%End
"""
},
# ./kdeui/kwindowsystem.sip
"QList<WId>": { #QList<WId>
"code":
"""
%ConvertFromTypeCode
    // Create the list.
    PyObject *l;

    if ((l = PyList_New(sipCpp->size())) == NULL)
        return NULL;

    // Set the list elements.
    for (int i = 0; i < sipCpp->size(); ++i) {
        PyObject *pobj;

#if PY_MAJOR_VERSION >= 3
        if ((pobj = PyLong_FromLong ((long)sipCpp->value(i))) == NULL) {
#else
        if ((pobj = PyInt_FromLong ((long)sipCpp->value(i))) == NULL) {
#endif
            Py_DECREF(l);

            return NULL;
        }

        PyList_SET_ITEM(l, i, pobj);
    }

    return l;
%End
%ConvertToTypeCode
    // Check the type if that is all that is required.
    if (sipIsErr == NULL)
        return PyList_Check(sipPy);

    QList<WId> *ql = new QList<WId>;

    for (int i = 0; i < PyList_GET_SIZE(sipPy); ++i) {
#if PY_MAJOR_VERSION >= 3
        ql->append((WId)PyLong_AsLong(PyList_GET_ITEM(sipPy, i)));
#else
        ql->append((WId)PyInt_AS_LONG (PyList_GET_ITEM(sipPy, i)));
#endif
    }
    *sipCppPtr = ql;

    return sipGetState(sipTransferObj);
%End
"""
},
}
