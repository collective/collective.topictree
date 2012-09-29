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

        context_node_uid = request.get('context_node_uid', '')
        if not context_node_uid:
            return 'UNDEFINED'

        # find the context object
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(UID=context_node_uid)

        obj = brains[0].getObject()        
        topic = createContentInContainer(obj,
                                         "collective.topictree.topic",
                                         title='New Topic') 
        result = 'success'
        return json.dumps({ 'result'   : result,
                            'node_uid' : IUUID(topic) })

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
        brains = catalog(portal_type='collective.topictree.topic',
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
        # get the JSON representation of the topic tree
        # call TopicJSON on root
        return self.TopicJSON(IUUID(self.context))

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

    def TopicJSON(self,node_uid):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(UID=node_uid)
        contents = brains[0].getObject().getFolderContents()
        node_name = brains[0].Title

        # node_rel should be default unless it is a root node
        if brains[0].portal_type == 'collective.topictree.topictree':
            node_rel = 'root'
        else:
            node_rel = 'default'        

        Json_string = ''

        if len(contents) == 0: 
            # Tree leaf
            Json_string = '{ "data" : "' + node_name +\
                          '", "attr" : { "node_uid" : "' + node_uid +\
                          '", "rel" : "' + node_rel + '" } }'
        else:
            # Non Tree leaf
            Json_string = '{ "data" : "' + node_name +\
                          '", "attr" : { "node_uid" : "' + node_uid +\
                          '", "rel" : "' + node_rel +\
                          '" }, "children" : [ '

            for brain in contents:
                    brain_uid = brain.UID                
                    Json_string = Json_string + self.TopicJSON(brain_uid) + ', '

            # remove last 2 characters ", " (not needed after last child)
            Json_string = Json_string[:-2]
            # add closing brackets
            Json_string = Json_string + ' ] }'

        return Json_string

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

        paste_uid = request.get('paste_uid', '')
        cut_source_uid = request.get('cut_source_uid', '')
        copy_source_uid = request.get('copy_source_uid', '')

        # if cut or copy have not been clicked yet  - return
        if cut_source_uid == '' and copy_source_uid == '':
            return 

        # if cut node_uid has valid uid - cut was pressed
        if cut_source_uid != '':
            brains = catalog(UID=cut_source_uid)
            obj = brains[0].getObject()
            source_folder = obj.aq_parent
            obj_id = brains[0].id
            # cut
            cp = source_folder.manage_cutObjects(obj_id)

        # if copy node_uid has valid uid - copy was pressed
        if copy_source_uid != '':
            brains = catalog(UID=copy_source_uid)
            obj = brains[0].getObject()
            source_folder = obj.aq_parent
            obj_id = brains[0].id
            # copy
            cp = source_folder.manage_copyObjects(obj_id)

        # get the paste
        brains2 = catalog(UID=paste_uid)
        paste_folder = brains2[0].getObject()

        # paste
        paste_folder.manage_pasteObjects(cp)
   
        result = 'success'
        return json.dumps({ 'result' : result})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''
