#!/usr/bin/python
# -*- coding: UTF-8 -*-
import Melement

class ContainerElement(Melement):
	def __init__(self,id,tag,containerstyle):

        super().__init__(id,tag) 

		self.containerStyle = containerstyle
