#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum

class InteractionElement(object):
	class Interaction(Enum):
		ONCLICK = 1
		ONHOVER = 2
		ONDRAG = 3
		ONKEYDOWN = 4
		AFTERTIMEOUT = 5
	onclick = Interaction.ONCLICK
	onhover = Interaction.ONHOVER
	ondrag = Interaction.ONDRAG
	onkeydown = Interaction.ONKEYDOWN
	aftertimeout = Interaction.AFTERTIMEOUT

	def __init__(self):
		self.interactiontype = None
		self.actions = []
		self.keyCodes = []
		self.timeout = 0

	def getInteractionType(self):
		"""@ReturnType String"""
		return self.interactiontype

	def setInteractionType(self, interactionType):
		"""@ParamType interactionType String
		@ReturnType void"""
		self.interactiontype = interactionType

	def getKeyCodes(self):
		"""@ReturnType list"""
		return self.keyCodes

	def setKeyCodes(self, keyCodes):
		"""@ParamType keyCodes list
		@ReturnType void"""
		self.keyCodes = keyCodes

	def getActions(self):
		"""@ReturnType String"""
		return self.actions

	def setActions(self, actions):
		"""@ParamType interactionType String
		@ReturnType void"""
		self.actions = actions

	def addAction(self,action):
		self.actions.append(action)
  
	def getTimeout(self):
		"""@ReturnType int"""
		return self.timeout

	def setTimeout(self, timeout):
		"""@ParamType timeout int
		@ReturnType void"""
		self.timeout = timeout
