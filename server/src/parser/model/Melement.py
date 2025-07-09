#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Melement(object):

	def __init__(self,id,tag,name):
		if("#" in name):
			self.name = name.split("#")[0]
		else:
			self.name = name
		self.idElement = id
		self.tag = tag
		self.children = []
		self.interactions = []
		self.upperIdComponent = None
		self.zindex = 0
		self.initialOpacity = None
		self.hasAnimation = False
		self.hasConditionalVisibility = False
		self.typeElement = None
  
	def getIdElement(self):
		return self.idElement

	def setIdElement(self, idElement):
		self.idElement = idElement
	
	def getinitialOpacity(self):
		return self.initialOpacity

	def setinitialOpacity(self, initialOpacity):
		self.initialOpacity = initialOpacity

	def getTag(self):
		return self.tag

	def setTag(self, tag):
		self.tag = tag

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def setChildren(self, nchildren):
		self.children = nchildren

	def addChildren(self,elem):
		self.children.append(elem)

	def getupperIdComponent(self):
		return self.upperIdComponent

	def setupperIdComponent(self, id):
		self.upperIdComponent = id

	def getInteractions(self):
		return self.interactions

	def getzindex(self):
		return self.zindex

	def setzindex(self, zindex):
		self.zindex = zindex

	def gethasAnimation(self):
		"""@ReturnType boolean"""
		return self.hasAnimation

	def sethasAnimation(self, hasAnimation):
		"""@ParamType type boolean
		@ReturnType void"""
		self.hasAnimation = hasAnimation
  
	def gettypeElement(self):
		return self.typeElement

	def settypeElement(self,typelem):
		self.typeElement=typelem

	def gethascondvisib(self):
		return self.hasConditionalVisibility

	def sethascondvisib(self, hascondvisib):
		self.hasConditionalVisibility = hascondvisib

	def setInteractions(self, interactions):
		self.interactions = interactions

	def addInteractionsList(self,interactions):
		self.interactions.extend(interactions)

	def __str__(self):
		return "(id: " + str(self.idElement) + "; tag: " + str(self.tag) + "; children : ["+ ''.join(str(c) for c in self.children) + "]" + "; interactions : ["+ ''.join(str(c) for c in self.interactions) + "])"

