from five import grok

#from zope.component.hooks import getSite

from plone.directives import dexterity
from z3c.form import form, button

#from Acquisition import aq_inner

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


