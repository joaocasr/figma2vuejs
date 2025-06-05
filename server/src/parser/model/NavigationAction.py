#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.ElementAction import ElementAction

class NavigationAction(ElementAction):
	def __init__(self,id):

		super().__init__("NAVIGATION") 
		self.destinationID = id

	def getDestinationID(self):
		"""@ReturnType destinationID"""
		return self.destinationID

	def setDestinationID(self, id):
		"""@ParamType destinationID String
		@ReturnType void"""
		self.destinationID = id
