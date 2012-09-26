import json

from five import grok

from zope.interface import Interface
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from collective.topictree import MessageFactory as _
from collective.topictree.topictree import ITopicTree

from plone.uuid.interfaces import IUUID
from plone.dexterity.utils import createContentInContainer

from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class AddTopicView(grok.View):
    """ Add Topic to the topic tree
    """
    grok.context(ITopicTree)
    grok.name('addtopic') 
    grok.require('zope2.View')

    def __call__(self):
        request = self.request
        context = self.context
        topic = createContentInContainer(context, "collective.topictree.topic",
                                                             title='New Topic') 
        result = 'success'
        return json.dumps({ 'result'   : result,
                            'node_uid' : IUUID(topic),
                            'path'     : topic.absolute_url()})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class EditTopicView(grok.View):
    """ Edit Topic on the topic tree
    """
    grok.context(ITopicTree)
    grok.name('edittopic') 
    grok.require('zope2.View')

    def __call__(self):
        request = self.request
        context = self.context
        topic_title = request.get('topic_title', '')
        node_uid = request.get('node_uid', '')
        if not topic_title and not node_uid:
            return
   
        # find the node object
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(
                 portal_type='collective.topictree.topic',
                 UID=node_uid)
        obj = brains[0].getObject()

        # set the new title
        obj.title = topic_title
        notify(ObjectModifiedEvent(obj))

        result = 'success'
        return json.dumps({ 'result' : result})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

class DeleteTopicView(grok.View):
    """ Delete Topic from the topic tree
    """
    grok.context(ITopicTree)
    grok.name('deletetopic') 
    grok.require('zope2.View')

    def __call__(self):
        request = self.request
        context = self.context
        node_uid = request.get('node_uid', '')
        if not node_uid:
            return
    
        # find the node object
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(
                 portal_type='collective.topictree.topic',
                 UID=node_uid)
        obj = brains[0].getObject()

        # delete the object
        parent = obj.aq_parent
        parent.manage_delObjects([obj.getId()])

        result = 'success'
        return json.dumps({ 'result' : result})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

class StateOfTreeView(grok.View):
    """ Return the JSON representation of the entire Topic Tree
    """
    grok.context(ITopicTree)
    grok.name('stateoftree') 
    grok.require('zope2.View')

    def __call__(self):
        request = self.request
        context = self.context
    
        result = 'success'
        return json.dumps({ 'result' : result})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

