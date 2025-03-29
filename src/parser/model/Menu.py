#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Menu(Mcomponent):
	def __init__(self,id,tag,name,type,options,iconImage,style):

		super().__init__(id,name,tag,type) 

		self.style = style
		self.options = options
		self.iconImage = iconImage

