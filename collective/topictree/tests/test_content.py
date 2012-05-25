import unittest2 as unittest

from zope.component import createObject

from Products.CMFCore.utils import getToolByName

from collective.topictree.topictree import ITopicTree
from collective.topictree.topic import ITopic

from base import PROJECTNAME
from base import INTEGRATION_TESTING

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
