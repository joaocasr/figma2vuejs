#!/usr/bin/python
# -*- coding: UTF-8 -*-
class ElementAction(object):
	def __init__(self,type,transition):
		self.actionType = type
		self.transition = transition

	def getActionType(self):
		"""@ReturnType String"""
		return self.actionType

	def setActionType(self, actionType):
		"""@ParamType actionType String
		@ReturnType void"""
		self.actionType = actionType

	def getTransition(self):
		"""@ReturnType object"""
		return self.transition

	def setTransition(self, transition):
		"""@ParamType transition object
		@ReturnType void"""
		self.transition = transition