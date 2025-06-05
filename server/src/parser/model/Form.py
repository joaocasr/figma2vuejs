#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Form(Mcomponent):
	def __init__(self,id,tag,name,type,inputs,buttontxt,style):

		super().__init__(id,name,tag,type) 

		self.inputs = inputs
		self.buttontxt = buttontxt
		self.style = style
