#!/usr/bin/python
# -*- coding: UTF-8 -*-
class Mcomponent(object):
	def __init__(self,id,name,tag,type,elementos=[]):
		self.idComponent = id
		self.componentName = name
		self.children = elementos
		self.tag = tag
		self.type = type
		self.style = None
		self.interactions = []
		self.data = []
		self.hasCloseAction = False

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

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data

	def addVariable(self,var):
		return self.data.append(var)

	def getHasCloseAction(self):
		return self.hasCloseAction

	def setHasCloseAction(self, hasCloseAction):
		self.hasCloseAction = hasCloseAction

	def setChildren(self,children):
		self.children = children

	def getInteractions(self):
		return self.interactions

	def setInteractions(self, interactions):
		self.interactions = interactions

	def __str__(self):
		return "(id: " + str(self.idComponent) + ",name: "+  str(self.componentName) + ",type: "+  str(self.type) + ",tag: "+  str(self.tag) + "; interactions: ["+ ";".join(str(val) for val in self.interactions)  +"]" + ", children: [" + ";".join(str(val) for val in self.children) + "]"