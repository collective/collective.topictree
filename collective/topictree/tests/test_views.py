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

class TestAddTopicView(CollectiveTopictreeTestBase):
    """ Methods to test add topic tree view """

    def test_view(self):
        addtopic = self.topictree.restrictedTraverse('@@addtopic')
        self.assertRaises(KeyError, addtopic)

        self.request.set('context_uid', IUUID(self.topictree))
        self.request.set('title', 'New Topic')
        addtopic()
        self.assertEquals(len(self.topictree.getFolderContents()), 1)
        topic = self.topictree.getFolderContents()[0].getObject()
        self.assertTrue(ITopic.providedBy(topic))
        self.assertEquals(topic.title, 'New Topic')
       
class TestEditTopicView(CollectiveTopictreeTestBase):
    """ Methods to test edit topic tree view """

    def test_view(self):
        edittopic = self.topictree.restrictedTraverse('@@edittopic')
        self.assertRaises(KeyError, edittopic)

        topic = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='New Topic') 

        notify(ObjectModifiedEvent(topic))

        self.request.set('node_uid', IUUID(topic))
        self.request.set('topic_title', 'Renamed Title')
        edittopic()
        self.assertEqual(topic.title, 'Renamed Title')

class TestDeleteTopicView(CollectiveTopictreeTestBase):
    """ Methods to test delete topic tree view """

    def test_view(self):
        deltopic = self.topictree.restrictedTraverse('@@deletetopic')
        self.assertRaises(KeyError, deltopic)

        topic = createContentInContainer(self.topictree,
                                         "collective.topictree.topic",
                                         title='NewTopic') 

        notify(ObjectModifiedEvent(topic))
        self.request.set('node_uid', IUUID(topic))
        self.assertEqual(self.topictree.getFolderContents()[0].Title,
                         'NewTopic')
        deltopic()
        self.assertEqual(len(self.topictree.getFolderContents()), 0)

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

        treedata = {
            "data": "",
            "attr": {
                "node_uid": IUUID(self.topictree), "id": IUUID(self.topictree)
                },
            "rel": "root",
            "children": [
                {
                "data": parent.title,
                "attr": {
                    "node_uid": IUUID(parent),
                    "id": IUUID(parent)},
                "rel": "default",
                "children": [
                    {
                    "data": child1.title,
                    "attr": {
                        "node_uid": IUUID(child1),
                        "id": IUUID(child1)},
                    "rel": "default",
                    "children": []
                    },
                    {
                    "data": child2.title,
                    "attr": {
                        "node_uid": IUUID(child2),
                        "id": IUUID(child2)},
                    "rel": "default",
                    "children": []
                    },
                    ],
                }
            ]
        }

        self.assertEqual(json.loads(view()), treedata)


class TestPasteTopicView(CollectiveTopictreeTestBase):
    """ Methods to test paste topic tree view """

    def test_pasteTopic(self):
        pastetopic = self.topictree.restrictedTraverse('@@pastetopic')
        self.assertRaises(KeyError, pastetopic)

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

        self.request.set('source_uid',IUUID(child1_2))
        self.request.set('target_uid',IUUID(child2))
        self.request.set('is_copy', 'false')
        pastetopic()
        # child1_2 moved inside child2
        self.assertEqual(child2.getFolderContents()[0].UID, IUUID(child1_2))
        # child1 should now not contain any children
        self.assertEqual(len(child1.getFolderContents()), 0)

        # delete the tree except for root (to clear for next test)
        self.topictree.manage_delObjects([parent.getId()])
        self.assertEquals(len(self.topictree.getFolderContents()), 0)
        # clear the request variable
        self.request.set('source_uid', '')

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

        self.request.set('source_uid', IUUID(child1_2))
        self.request.set('target_uid', IUUID(child2))
        self.request.set('is_copy', 'true')
        pastetopic()
        # child1_2 copied inside child2
        # child1 should still contain child1_2
        self.assertEqual(child1.getFolderContents()[0].UID, IUUID(child1_2))
        # child1_2 and its copy should match titles
        self.assertEqual(child1_2.Title(), child2.getFolderContents()[0].Title)
        # child1_2 and its copy should NOT match UIDs
        self.assertNotEqual(IUUID(child1_2), child2.getFolderContents()[0].UID)

