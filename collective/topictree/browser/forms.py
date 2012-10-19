from five import grok

from plone.directives import dexterity

from collective.topictree.topictree import ITopicTree

from collective.topictree.interfaces import ITopicTreeLayer

grok.templatedir('templates')
grok.layer(ITopicTreeLayer)

class TopicTreeEditForm(dexterity.EditForm):
    grok.name('edit')
    grok.context(ITopicTree)
    grok.template('edittopictree')

    formname = 'edit-topictree-form'
    kssformname = "kssattr-formname-@@edit"
