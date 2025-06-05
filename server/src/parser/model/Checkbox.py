#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class Checkbox(Mcomponent):
	def __init__(self,id,tag,name,type,boxes,style):

		super().__init__(id,name,tag,type) 

		self.boxes = boxes
		self.style = style
