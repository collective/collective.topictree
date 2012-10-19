from zope import schema
from five import grok
from plone.directives import form

from collective.topictree import MessageFactory as _

class ITopicTree(form.Schema):
    """ Simple container class for a topic tree.
    """

    title = schema.TextLine(
        title = _(u'label_title', default=u'Title'),
        required = True
        )

class View(grok.View):
    grok.context(ITopicTree)
    grok.require('zope2.View')
