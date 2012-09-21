import json

from five import grok

from zope.interface import Interface

from collective.topictree import MessageFactory as _
from collective.topictree.topictree import ITopicTree

from plone.uuid.interfaces import IUUID
from plone.dexterity.utils import createContentInContainer

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

        topic_title = request.get('topic_title', '')
        if not topic_title:
            return

        topic = createContentInContainer(context, "collective.topictree.topic",
                                                             title=topic_title) 

        result = 'success'
        return json.dumps({'result'   : result,
                           'title'    : topic_title,
                           'node_uid' : IUUID(topic),
                           'path'     : topic.absolute_url()})

    def render(self):
        """ No-op to keep grok.View happy
        """
        return ''

