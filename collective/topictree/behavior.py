from zope.interface import alsoProvides

from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice, RelationList

from collective.topictree import MessageFactory as _

class ITopicTags(form.Schema):
    """ Behavior that enables tagging content with topics in a topic
        tree.
    """

    topics = RelationList(
        title=u"Topics",
        default=[],
        value_type=RelationChoice(title=_(u"Related"),
                                  source=ObjPathSourceBinder(
                                  object_provides=
                                      'collective.topictree.topic.ITopic')
                                  ),
        required=False,
    )

alsoProvides(ITopicTags, IFormFieldProvider)

