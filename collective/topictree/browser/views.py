import json

from five import grok

from zope.interface import Interface

from collective.topictree import MessageFactory as _
from collective.topictree.topictree import ITopicTree

grok.templatedir('templates')

class AddTopicView(grok.View):
    """ Add Topic to the topic tree
    """
    grok.context(ITopicTree)
    grok.name('addtopic') 
    grok.template('addtopic')
    grok.require('zope2.View')

    def addTopic(self):
        request = self.request
        context = self.context

        topic_title = request.get('topic_title', '')
        if not topic_title:
            return

        return topic_title

