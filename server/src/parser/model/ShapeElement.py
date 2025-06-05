#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Melement import Melement

class ShapeElement(Melement):
	def __init__(self,id,tag,name,type,shapeStyle):

		super().__init__(id,tag,name) 

		self.style = shapeStyle
		self.type = type
    
	def getType(self):
		return self.type