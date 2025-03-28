#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Melement import Melement

class VideoElement(Melement):
	def __init__(self,id,tag,name,src,style):

		super().__init__(id,tag,name) 

		self.src = src
		self.style = style

	def getSrc(self):
		return self.src

	def setSrc(self, src):
		self.src = src