#!/usr/bin/python
# -*- coding: UTF-8 -*-
class ElementAction(object):
	def __init__(self,type):
		self.actionType = type

	def getActionType(self):
		"""@ReturnType String"""
		return self.actionType

	def setActionType(self, actionType):
		"""@ParamType actionType String
		@ReturnType void"""
		self.actionType = actionType
