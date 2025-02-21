#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import InteractionElement

class ElementAction(object):
	def getActionType(self):
		"""@ReturnType String"""
		return self.actionType

	def setActionType(self, actionType):
		"""@ParamType actionType String
		@ReturnType void"""
		self.actionType = actionType

	def getTargetID(self):
		"""@ReturnType String"""
		return self.targetID

	def setTargetID(self, targetID):
		"""@ParamType targetID String
		@ReturnType void"""
		self.targetID = targetID

	def __init__(self):
		self.actionType = None
		"""@AttributeType String"""
		self.targetID = None
		"""@AttributeType String"""
		self.unnamed_InteractionElement_ = None
		"""@AttributeType InteractionElement
		# @AssociationType InteractionElement"""

