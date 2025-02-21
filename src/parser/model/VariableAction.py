#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import ElementAction

class VariableAction(ElementAction):
	def getVariable(self):
		"""@ReturnType String"""
		return self.variable

	def setVariable(self, variable):
		"""@ParamType variable String
		@ReturnType void"""
		self.variable = variable

	def getValue(self):
		"""@ReturnType String"""
		return self.value

	def setValue(self, value):
		"""@ParamType value String
		@ReturnType void"""
		self.value = value

	def __init__(self):
		self.variable = None
		"""@AttributeType String"""
		self.value = None
		"""@AttributeType String"""

