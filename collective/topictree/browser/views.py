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
        request = self.request
        context = self.context
    
        # get the JSON representation of the topic tree - call TopicJSON on root
        TreeJSON = self.TopicJSON( IUUID(self.context) )

        print TreeJSON
        return json.dumps([TreeJSON])

        test = { "data" : self.context.title, "attr" : { "node_uid" : IUUID(self.context), "rel" : "root" } }
        return json.dumps([test])

#        return json.dumps([
#        { "data" : self.context.title, "attr" : { "node_uid" : IUUID(self.context), "rel" : "root" } }
#          "children" : [ "Child 1", "A Child 2" ] 
                ])

#        return json.dumps([

#        { "data" : "I am a root node",
#          "attr" : { "rel" : "root" },
#          "children" : [ "Child 1", "A Child 2" ] },
#        { "data" : "I am a more complicated root node",
#          "attr" : { "rel" : "root" },
#          "children" : [ 
#

#        # this 'child 1' has two of its own children.
#        { "data" : "I have 2 children",
#          "attr" : { "node_uid" : "88888888888888888888",
#                     "rel" : "topic",
#                   },
#          "children" : [ "Child 1", "A Child 2" ] },
#
#         "A Child 2" ] },
#     
#        { "data" : "A node", "metadata" : { "id" : "23" }, 
#                             "children" : [ "Child 1", "A Child 2" ] },
#        { "attr" : { "id" : "li.node.id1" },
#          "data" : { "title" : "Long format demo",
#                     "attr" : { "href" : "#" } } }
#               ])

# XXX Older examples - remove upon successfull loading state of the tree.
 
#	{ "data" : "A node", "state" : "open" },
#	"Ajax node",
#	{ "data" : "A node", "children" : [ { "data" : "Only child", "state" : "open" } ], "state" : "open" },

#               ])

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

    def TopicJSON(self,node_uid):

        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(UID=node_uid)
        contents = brains[0].getFolderContents()
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
                          '" , "rel" : "' + node_rel + '" } }'
        else:
            # Non Tree leaf
            print 'NOT YET IMPLEMENTED'      
#            Json_string = '{ "data" : "' + node_name +\
#                          '", "attr" : { "node_uid" : "' + node_uid +\
#                          '" , "rel" : "' + node_rel +\
#                          '" }, children : ['

        #            for each object in the container
        #                get its node_uid
        #                Json_string = Json_string + TopicJSON(node_uid) + ' ,'
        #            end
            
#            remove the last , from the string
#            Json_string = Json_string + ' ] }'

#        import pdb; pdb.set_trace()

#        Json_string = 'nothing yet'
        return Json_string

