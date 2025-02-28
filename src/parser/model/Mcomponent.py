#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Mcomponent(object):
	def __init__(self,id,name,tag,type,elementos=[]):
		self.idComponent = id
		self.componentName = name
		self.elements = elementos
		self.tag = tag
		self.type = type
		self.style = None

	def getIdComponent(self):
		"""@ReturnType String"""
		return self.idComponent

	def setIdComponent(self, idComponent):
		"""@ParamType idComponent String
		@ReturnType void"""
		self.idComponent = idComponent

	def getNameComponent(self):
		"""@ReturnType String"""
		return self.componentName

	def setNameComponent(self, name):
		"""@ParamType componentName String
		@ReturnType void"""
		self.componentName = name

	def getTagComponent(self):
		"""@ReturnType String"""
		return self.tag

	def setTagComponent(self, tag):
		"""@ParamType tag String
		@ReturnType void"""
		self.tag = tag

	def getTypeComponent(self):
		"""@ReturnType String"""
		return self.type

	def setTypeComponent(self, type):
		"""@ParamType type String
		@ReturnType void"""
		self.type = type

	def setComponentStyle(self, style):
		"""@ParamType type String
		@ReturnType void"""
		self.style = style

	def getComponentStyle(self):
		"""@ParamType type String
		@ReturnType void"""
		return self.style

	def __str__(self):
		return "(id: " + str(self.idComponent) + ",name: "+  str(self.componentName) + ",type: "+  str(self.type) + ",tag: "+  str(self.tag) + ", style: "+  str(self.style) + ", elements: [" + ";".join(str(val) for val in self.elements) + "]"