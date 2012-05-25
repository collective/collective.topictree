from zope.interface import implements

from Products.Archetypes.public import ReferenceField

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

class _TopicTagsExtensionField(ExtensionField, ReferenceField): pass

class TopicTagsExtender(object):
    implements(IOrderableSchemaExtender)

    fields = [
        _TopicTagsExtensionField(
            "topics",
            widget=ReferenceBrowserWidget(
                label=u"Topics",
                description=u"Tag content with topics from a topic tree",
                allow_search=False,
            ),
            multiValued=True,
            allowed_types=('collective.topictree.topic',),
            relationship='topics',
            schemata='categorization',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ Put topics field below subject
        """
        schematas["categorization"] = ['subject', 'topics', 'relatedItems', 
                                       'location', 'language']
        return schematas

    def getFields(self):
        return self.fields

