#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Dropdown(Mcomponent):
	def __init__(self,id,tag,name,type,selected,options,placeholder,ismulti,componentStyle):

		super().__init__(id,name,tag,type) 

		self.options = options
		self.ismulti = ismulti
		self.vmodel = selected
		self.placeholder = placeholder
		self.style = componentStyle
