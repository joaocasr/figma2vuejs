#!/usr/bin/python
# -*- coding: UTF-8 -*-
from parser.model.Melement import Melement

class ImageElement(Melement):
	def __init__(self,id,tag,name,src,imageStyle):

		super().__init__(id,tag,name) 
		self.src = src

		self.style = imageStyle
	
	def getSrc(self):
		"""@ReturnType String"""
		return self.src

	def setSrc(self, src):
		"""@ParamType src String
		@ReturnType void"""
		self.src = src