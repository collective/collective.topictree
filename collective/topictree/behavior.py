from zope.interface import alsoProvides

from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice

from collective.topictree import MessageFactory as _

class ITopicTags(form.Schema):
    """ Behavior that enables tagging content with topics in a topic
        tree.
    """

    topics = RelationChoice(
        title=_(u'label_topics', default=u'Topics'),
        source=ObjPathSourceBinder(
          object_provides='collective.topictree.topic.ITopic'),
        required=False,
    )

alsoProvides(ITopicTags, IFormFieldProvider)
