import json
import transaction
import unittest2 as unittest

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import createObject

from plone.uuid.interfaces import IUUID
from plone.dexterity.utils import createContentInContainer

from Products.CMFCore.utils import getToolByName

from collective.topictree.topictree import ITopicTree
from collective.topictree.topic import ITopic

from base import PROJECTNAME
from base import INTEGRATION_TESTING
from base import CollectiveTopictreeTestBase

class TestContentTypes(unittest.TestCase):
    """ Test content types """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_topictree(self):
        tree = createObject('collective.topictree.topictree', id='tree')
        self.assertTrue(ITopicTree.providedBy(tree))

    def test_topic(self):
        topic = createObject('collective.topictree.topic', id='topic')
        self.assertTrue(ITopic.providedBy(topic))

class TestAddTopicView(CollectiveTopictreeTestBase):
    """ Methods to test add topic tree view """

    def test_addTopic(self):
        view = self.topictree.restrictedTraverse('@@addtopic')
        AddTopic = view.__call__()
        self.assertEqual(AddTopic,'UNDEFINED')

        self.request.set('context_node_uid',IUUID(self.topictree))
        AddTopic = view.__call__()
        self.assertEquals(len(self.topictree.getFolderContents()),1)
        created_type = self.topictree.getFolderContents()[0].portal_type       
        self.assertEquals(created_type,'collective.topictree.topic')
       
class TestEditTopicView(CollectiveTopictreeTestBase):
    """ Methods to test edit topic tree view """

    def test_editTopic(self):
        view = self.topictree.restrictedTraverse('@@edittopic')
        EditTopic = view.__call__()
        self.assertEqual(EditTopic,'UNDEFINED')

        topic = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='New Topic') 

        notify(ObjectModifiedEvent(topic))

        self.request.set('node_uid',IUUID(topic))
        self.request.set('topic_title','Renamed Topic')
        EditTopic = view.__call__()
        self.assertEqual(topic.title,'Renamed Topic')

class TestDeleteTopicView(CollectiveTopictreeTestBase):
    """ Methods to test delete topic tree view """

    def test_deleteTopic(self):
        view = self.topictree.restrictedTraverse('@@deletetopic')
        DeleteTopic = view.__call__()
        self.assertEqual(DeleteTopic,'UNDEFINED')

        topic = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='NewTopic') 

        notify(ObjectModifiedEvent(topic))
        self.request.set('node_uid',IUUID(topic))
        self.assertEqual(self.topictree.getFolderContents()[0].Title,'NewTopic')
        DeleteTopic = view.__call__()
        self.assertEqual(len(self.topictree.getFolderContents()),0)

class TestTreeDataView(CollectiveTopictreeTestBase):
    """ Methods to test tree data view """

    def test_treeData(self):
        view = self.topictree.restrictedTraverse('@@treedata')

        parent = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='Parent')
        child1 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child1')
        child2 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child2')

        notify(ObjectModifiedEvent(parent))
        notify(ObjectModifiedEvent(child1))
        notify(ObjectModifiedEvent(child2))

        T_Ref = '{ "data" : "", ' +\
                  '"attr" : ' +\
                    '{ "node_uid" : "' + IUUID(self.topictree) +'", ' +\
                      '"rel" : "root" }, ' +\
                      '"children" : [ { "data" : "Parent", ' +\
                        '"attr" : { "node_uid" : "' + IUUID(parent) + '", ' +\
                        '"rel" : "default" }, ' +\
                        '"children" : ' +\
                          '[ { "data" : "Child1", ' +\
                          '"attr" : { "node_uid" : "' + IUUID(child1) + '", ' +\
                          '"rel" : "default" } }, ' +\
                            '{ "data" : "Child2", ' +\
                          '"attr" : { "node_uid" : "' + IUUID(child2) + '", ' +\
                          '"rel" : "default" } } ] ' +\
                        '} ] }'

        TreeData = view.__call__()
        self.assertEqual(TreeData,T_Ref)

    def test_TopicJSON(self):
        view = self.topictree.restrictedTraverse('@@treedata')

        parent = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='Parent')
        child1 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child1')
        child2 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child2')

        notify(ObjectModifiedEvent(parent))
        notify(ObjectModifiedEvent(child1))
        notify(ObjectModifiedEvent(child2))

        T_Ref = '{ "data" : "", ' +\
                  '"attr" : ' +\
                    '{ "node_uid" : "' + IUUID(self.topictree) +'", ' +\
                      '"rel" : "root" }, ' +\
                      '"children" : [ { "data" : "Parent", ' +\
                        '"attr" : { "node_uid" : "' + IUUID(parent) + '", ' +\
                        '"rel" : "default" }, ' +\
                        '"children" : ' +\
                          '[ { "data" : "Child1", ' +\
                          '"attr" : { "node_uid" : "' + IUUID(child1) + '", ' +\
                          '"rel" : "default" } }, ' +\
                            '{ "data" : "Child2", ' +\
                          '"attr" : { "node_uid" : "' + IUUID(child2) + '", ' +\
                          '"rel" : "default" } } ] ' +\
                        '} ] }'

        TopicJSON = view.TopicJSON(IUUID(self.topictree))
        self.assertEqual(TopicJSON,T_Ref)

class TestPasteTopicView(CollectiveTopictreeTestBase):
    """ Methods to test paste topic tree view """

    def test_pasteTopic(self):
        view = self.topictree.restrictedTraverse('@@pastetopic')

        # no cut, no copy scenario
        PasteTopic = view.__call__()
        self.assertEqual(PasteTopic,None)

        # cut/paste scenario
        parent = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='Parent')
        child1 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child1')
        child2 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child2')

        child1_2 = createContentInContainer(child1,
                                         "collective.topictree.topic",
                                         title='Child1_2')

        notify(ObjectModifiedEvent(parent))
        notify(ObjectModifiedEvent(child1))
        notify(ObjectModifiedEvent(child2))
        notify(ObjectModifiedEvent(child1_2))

        transaction.savepoint(optimistic=True)

        self.request.set('cut_source_uid',IUUID(child1_2))
        self.request.set('paste_uid',IUUID(child2))
        PasteTopic = view.__call__()
        # child1_2 moved inside child2
        self.assertEqual(child2.getFolderContents()[0].UID,IUUID(child1_2))
        # child1 should now not contain any children
        self.assertEqual(len(child1.getFolderContents()),0)

        #delete the tree except for root (to clear for next test)
        self.topictree.manage_delObjects([parent.getId()])
        self.assertEquals(len(self.topictree.getFolderContents()),0)
        #clear the request variable
        self.request.set('cut_source_uid','')

        # copy/paste scenario
        parent = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='Parent')
        child1 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child1')
        child2 = createContentInContainer(parent,
                                         "collective.topictree.topic",
                                         title='Child2')

        child1_2 = createContentInContainer(child1,
                                         "collective.topictree.topic",
                                         title='Child1_2')

        notify(ObjectModifiedEvent(parent))
        notify(ObjectModifiedEvent(child1))
        notify(ObjectModifiedEvent(child2))
        notify(ObjectModifiedEvent(child1_2))

        self.request.set('copy_source_uid',IUUID(child1_2))
        self.request.set('paste_uid',IUUID(child2))
        PasteTopic = view.__call__()
        # child1_2 copied inside child2
        # child1 should still contain child1_2
        self.assertEqual(child1.getFolderContents()[0].UID,IUUID(child1_2))
        # child1_2 and its copy should match titles
        self.assertEqual(child1_2.Title(),child2.getFolderContents()[0].Title)
        # child1_2 and its copy should NOT match UIDs
        self.assertNotEqual(IUUID(child1_2),child2.getFolderContents()[0].UID)

