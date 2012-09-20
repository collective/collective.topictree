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

    # overwrite add handler because we are overwritting cancel handler,
    # seems both are necessary for things to work
    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        super(TopicTreeEditForm, self).handleAdd(self,action)

    # overwrite cancel handler so that StatusMessage does not get displayed
    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self,action):
        # do not call IStatusMessage
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))


