import json

from five import grok

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

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
        context_uid = self.request['context_uid']
        title = self.request['title']

        # find the context object
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(UID=context_uid)

        obj = brains[0].getObject()        
        topic = createContentInContainer(obj, "collective.topictree.topic",
                                         title=title) 
        return json.dumps({'node_uid': IUUID(topic)})

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
        topic_title = self.request['topic_title']
        node_uid = self.request['node_uid']
   
        # find the node object
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(portal_type='collective.topictree.topic', UID=node_uid)
        obj = brains[0].getObject()

        # set the new title
        obj.title = topic_title
        notify(ObjectModifiedEvent(obj))

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
        node_uid = self.request['node_uid']
    
        # find the node object
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(portal_type='collective.topictree.topic', UID=node_uid)
        obj = brains[0].getObject()

        # delete the object
        parent = obj.aq_parent
        parent.manage_delObjects(obj.getId())

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''


class TreeDataView(grok.View):
    """ Return the JSON representation of the entire Topic Tree
    """
    grok.context(ITopicTree)
    grok.name('treedata') 
    grok.require('zope2.View')

    def __call__(self):
        return json.dumps(self.data(IUUID(self.context)))

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

    def data(self, node_uid):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(UID=node_uid)
        contents = brains[0].getObject().getFolderContents()
        node_name = brains[0].Title

        # node_rel should be default unless it is a root node
        if brains[0].portal_type == 'collective.topictree.topictree':
            node_rel = 'root'
        else:
            node_rel = 'default'        

        data = {
            'data': node_name,
            'attr': {'node_uid': node_uid, 'id': node_uid},
            'rel': node_rel,
            'children': [],
        }

        for brain in contents:
            data['children'].append(self.data(brain.UID))

        return data


class PasteTopicView(grok.View):
    """ Paste a Topic (and its children) into a new place in the tree
    """
    grok.context(ITopicTree)
    grok.name('pastetopic') 
    grok.require('zope2.View')

    def __call__(self):
        request = self.request
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')

        source_uid = request['source_uid']
        target_uid = request['target_uid']
        is_copy = request['is_copy'] == 'true'

        brains = catalog(UID=source_uid)
        if not brains:
            return
        obj = brains[0].getObject()
        if is_copy:
            cp = obj.aq_parent.manage_copyObjects(obj.getId())
        else:
            cp = obj.aq_parent.manage_cutObjects(obj.getId())

        # get the target folder
        brains = catalog(UID=target_uid)
        target = brains[0].getObject()

        # paste
        target.manage_pasteObjects(cp)
   
    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
