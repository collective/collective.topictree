import unittest2 as unittest

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import z2

PROJECTNAME = "collective.topictree"

class TestCase(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.topictree
        self.loadZCML(package=collective.topictree)
        z2.installProduct(app, PROJECTNAME)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, '%s:default' % PROJECTNAME)

    def tearDownZope(self, app):
        z2.uninstallProduct(app, PROJECTNAME)

FIXTURE = TestCase()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,),
                                         name="fixture:Integration")

class CollectiveTopictreeTestBase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.request = self.layer['request']

        self.portal.invokeFactory('collective.topictree.topictree', 'topictree')
        topictree = self.portal._getOb('topictree')
        notify(ObjectModifiedEvent(topictree))
        self.topictree = topictree




