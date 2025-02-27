#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum

class InteractionElement(object):
	class Interaction(Enum):
		ONCLICK = 1
		ONHOVER = 2
		ONDRAG = 3
	
	onclick = Interaction.ONCLICK
	onhover = Interaction.ONHOVER
	ondrag = Interaction.ONDRAG


	def __init__(self):
		self.interactiontype = None
		self.actions = []

	def getInteractionType(self):
		"""@ReturnType String"""
		return self.interactiontype

	def setInteractionType(self, interactionType):
		"""@ParamType interactionType String
		@ReturnType void"""
		self.interactiontype = interactionType

	def getActions(self):
		"""@ReturnType String"""
		return self.actions

	def setActions(self, actions):
		"""@ParamType interactionType String
		@ReturnType void"""
		self.actions = actions

	def addAction(self,action):
		self.actions.append(action)