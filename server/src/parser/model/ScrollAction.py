#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.ElementAction import ElementAction

class ScrollAction(ElementAction):
	def __init__(self,id,transition):

		super().__init__("SCROLL",transition) 
		self.destinationID = id

	def getDestinationID(self):
		"""@ReturnType destinationID"""
		return self.destinationID

	def setDestinationID(self, id):
		"""@ParamType destinationID String
		@ReturnType void"""
		self.destinationID = id
