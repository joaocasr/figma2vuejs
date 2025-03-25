#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Paginator(Mcomponent):
	def __init__(self,id,tag,name,type,vmodel,totalvisible,length,style):

		super().__init__(id,name,tag,type) 

		self.totalvisible = totalvisible
		self.length = length
		self.vmodel = vmodel
		self.style = style
