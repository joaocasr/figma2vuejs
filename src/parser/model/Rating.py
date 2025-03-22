#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Rating(Mcomponent):
	def __init__(self,id,tag,name,type,nrstars,readonly,vmodel,selected,style):

		super().__init__(id,name,tag,type) 

		self.nrstars = nrstars
		self.readonly = readonly
		self.vmodel = vmodel
		self.selected = selected
		self.style = style
