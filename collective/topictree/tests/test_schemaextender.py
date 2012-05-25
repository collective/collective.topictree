import unittest2 as unittest

from zope.interface import alsoProvides 
from zope.component import queryMultiAdapter

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from base import PROJECTNAME
from base import INTEGRATION_TESTING

class TestSchemaExtender(unittest.TestCase):
    """ Test schema extender 
    """
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        self.portal.invokeFactory('Document', id='test_page')
        context = self.portal.test_page
        self.assertTrue('topics' in context.Schema())

