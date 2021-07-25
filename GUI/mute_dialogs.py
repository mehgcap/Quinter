import wx
import mutes
from utils import alert

class NewMuteDialog(wx.Dialog):

	#IDs used when returning from modal
	#yes, we are re-using WX's IDs, but if we want to change/add to these in the future, code checking the return in other classes won't have to change anything
	ID_CANCEL = wx.ID_CANCEL
	ID_SAVE = wx.ID_SAVE

	def __init__(self, parent, id, title="New Mute"):
		super(NewMuteDialog, self).__init__(parent, id=id, title=title)
		self.panel = wx.Panel(self)
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		#holds the mute type list box and the edit field for the mute value
		self.controlsSizer = wx.BoxSizer(wx.HORIZONTAL)
		muteTypes = [mutes.Mute.TYPE_CLIENT, mutes.Mute.TYPE_HASHTAG, mutes.Mute.TYPE_USER]
		self.muteTypesLabel = wx.StaticText(self, label="Mute Types")
		self.muteTypesList = wx.ListBox(self, choices=muteTypes, style=wx.LB_SINGLE)
		self.muteTypesList.SetFocus()
		self.muteTypesList.SetSelection(0)
		self.controlsSizer.Add(self.muteTypesLabel)
		self.controlsSizer.Add(self.muteTypesList)
		self.muteValueLabel = wx.StaticText(self, label="Mute Value")
		self.muteValueInput = wx.TextCtrl(self, -1, "mute value", size=wx.Size(100, 60))
		self.controlsSizer.Add(self.muteValueLabel)
		self.controlsSizer.Add(self.muteValueInput)
		self.mainSizer.Add(self.controlsSizer)

		#holds the two buttons
		self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.saveButton = wx.Button(self.panel, id=wx.ID_SAVE, label="Save")
		self.saveButton.Bind(wx.EVT_BUTTON, self.onSave)
		self.cancelButton = wx.Button(self.panel, id=wx.ID_CANCEL, label="Cancel")
		self.cancelButton.Bind(wx.EVT_BUTTON, self.onCancel)
		self.buttonSizer.AddMany([self.saveButton, self.cancelButton])
		self.mainSizer.Add(self.buttonSizer)

	def onSave(self, event):
		#make sure we have a value
		if self.muteValueInput.GetValue() == "":
			alert("This mute has no value, so can't mute anything. You have to type something before you can save.", "Invalid Value")
			self.muteValueInput.SetFocus()
			return False
		elif self.muteTypesList.GetSelection() == -1:
			alert("You have to choose what kind of mute this is before you can save it.", "No Type Chosen")
			self.muteTypesList.SetFocus()
			return False
		self.EndModal(self.ID_SAVE)

	def onCancel(self, event):
		#there's nothing much to do here
		self.EndModal(self.ID_CANCEL)

class EditMuteDialog(NewMuteDialog):

	def __init__(self, parent, id, mute, title="Edit Mute"):
		super(EditMuteDialog, self).__init__(parent, id=id, title=title)
		self.mute = mute
		self.muteTypesList.SetStringSelection(self.mute.type, True)
		self.muteValueInput.SetValue(self.mute.value)
