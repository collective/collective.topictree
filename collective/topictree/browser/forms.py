from five import grok

from zope.event import notify

from plone.dexterity.events import EditCancelledEvent
from plone.dexterity.events import AddCancelledEvent
from plone.directives import dexterity
from z3c.form import form, button

from collective.topictree import MessageFactory as _
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
