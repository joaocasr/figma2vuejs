#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Table(Mcomponent):
	def __init__(self,id,tag,name,type,values,header,nrrows,componentStyle):

		super().__init__(id,name,tag,type) 

		self.values = values
		self.header = header
		self.nrrows = nrrows
		self.style = componentStyle
