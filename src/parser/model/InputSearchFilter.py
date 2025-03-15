#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class InputSearchFilter(Mcomponent):
	def __init__(self,id,tag,name,type,vmodel,placeholder,style):

		super().__init__(id,name,tag,type) 

		self.style = style
		self.vmodel = vmodel
		self.placeholder = placeholder