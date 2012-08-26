from zope import schema
from five import grok
from plone.directives import dexterity, form

from collective.topictree import MessageFactory as _

class ITopicTree(form.Schema):
    """ Simple container class for a topic tree.
    """

    title = schema.TextLine(
        title = _(u'label_title', default=u'Title'),
        required = True
        )
        
