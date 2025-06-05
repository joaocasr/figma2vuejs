#!/usr/bin/python
# -*- coding: UTF-8 -*-
from parser.model.Melement import Melement

class TextElement(Melement):
	def __init__(self,id,tag,name,text,textstyle):

		super().__init__(id,tag,name) 

		self.text = text
		self.style = textstyle

	def setInteractions(self, interactions):
		super().setInteractions(interactions)