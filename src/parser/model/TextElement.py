#!/usr/bin/python
# -*- coding: UTF-8 -*-
from parser.model.Melement import Melement

class TextElement(Melement):
	def __init__(self,id,tag,text,textstyle):

		super().__init__(id,tag) 

		self.text = text
		self.textStyle = textstyle
