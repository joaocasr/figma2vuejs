#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Slider(Mcomponent):
	def __init__(self,id,tag,name,type,selected,componentStyle):

		super().__init__(id,name,tag,type) 

		self.vmodel = selected
		self.style = componentStyle
