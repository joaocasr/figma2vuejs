#!/usr/bin/python
# -*- coding: UTF-8 -*-

class InteractionElement(object):
	def __init__(self,type):
		self.triggerType = type
		self.action = []

	def getInteractionType(self):
		"""@ReturnType String"""
		pass

	def setInteractionType(self, interactionType):
		"""@ParamType interactionType String
		@ReturnType void"""
		pass