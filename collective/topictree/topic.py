from zope import schema
from plone.directives import form

from collective.topictree import MessageFactory as _

class ITopic(form.Schema):
    """ Simple interface for ITopic
    """

    title = schema.TextLine(
        title = _(u'label_title', default=u'Title'),
        required = True
        )
        
