#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import ElementAction

class OverlayAction(ElementAction):
	def getX(self):
		"""@ReturnType String"""
		return self.x

	def setX(self, x):
		"""@ParamType x String
		@ReturnType void"""
		self.x = x

	def getY(self):
		"""@ReturnType String"""
		return self.y

	def setY(self, y):
		"""@ParamType y String
		@ReturnType void"""
		self.y = y

	def __init__(self):
		self.x = None
		"""@AttributeType String"""
		self.y = None
		"""@AttributeType String"""

