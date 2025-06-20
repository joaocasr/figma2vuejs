#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.ElementAction import ElementAction

class BackAction(ElementAction):
	def __init__(self,transition):

		super().__init__("BACK",transition) 
