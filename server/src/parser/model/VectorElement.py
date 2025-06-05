#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Melement import Melement

class VectorElement(Melement):
	def __init__(self,id,tag,name,svgpath,style):

		super().__init__(id,tag,name) 

		self.svgpath = svgpath
		self.style = style

	def getsvgpath(self):
		"""@ReturnType String"""
		return self.svgpath

	def setsvgpath(self, svgpath):
		"""@ParamType svgpath String
		@ReturnType void"""
		self.svgpath = svgpath