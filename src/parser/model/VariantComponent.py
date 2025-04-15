#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.Mcomponent import Mcomponent

class VariantComponent(Mcomponent):
	def __init__(self,id,tag,name,type,componentsInvolved):

		super().__init__(id,name,tag,type) 
		self.variantComponents = componentsInvolved
		self.variantProperties = {}
		self.defaultComponent = None

	def getVariantProperties(self):
		return self.variantProperties

	def setVariantProperties(self, variantProperties):
		self.variantProperties = variantProperties

	def getDefaultComponent(self):
		return self.defaultComponent

	def setDefaultComponent(self, defaultComponent):
		self.defaultComponent = defaultComponent

