#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Melement import Melement

class ContainerElement(Melement):
	def __init__(self,id,tag,name,containerstyle):

		super().__init__(id,tag,name) 

		self.style = containerstyle

	def setInteractions(self, interactions):
		super().setInteractions(interactions)