#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.ElementAction import ElementAction

class OverlayAction(ElementAction):
	def __init__(self,id):

		super().__init__("OVERLAY") 
		self.destinationID = id
		self.position=None
		self.closeClickOutside=None
		self.resetscrollposition=None
		self.background = None

	def getDestinationID(self):
		"""@ReturnType destinationID"""
		return self.destinationID

	def setDestinationID(self, id):
		"""@ParamType destinationID String
		@ReturnType void"""
		self.destinationID = id

	def getPosition(self):
		"""@ReturnType position"""
		return self.position

	def setPosition(self, position):
		"""@ParamType position String
		@ReturnType void"""
		self.position = position

	def getCloseClickOutside(self):
		"""@ReturnType closeClickOutside"""
		return self.closeClickOutside

	def getCloseClickOutside(self, closeClickOutside):
		"""@ParamType closeClickOutside
		@ReturnType boolean"""
		self.closeClickOutside = closeClickOutside
  
	def getResetScrollPosition(self):
		"""@ReturnType resetscrollposition"""
		return self.resetscrollposition

	def setResetScrollPosition(self, resetscrollposition):
		"""@ParamType resetscrollposition String
		@ReturnType boolean"""
		self.resetscrollposition = resetscrollposition
