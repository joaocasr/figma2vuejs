#!/usr/bin/python
# -*- coding: UTF-8 -*-
from parser.model.PageItem import PageItem

class Melement(PageItem):

	def __init__(self,id,tag,name):
		ename  = ""
		if("#" in name):
			ename = name.split("#")[0]
		else:
			ename = name
		self.interactions = []
		self.upperIdComponent = None
		self.zindex = 0
		self.initialOpacity = None
		self.hasAnimation = False
		self.hasConditionalVisibility = False
		self.topmostnode = None
		super().__init__(id,ename,tag,None,[]) 

	def getIdElement(self):
		return super().getId()

	def setIdElement(self, idElement):
		super().setId(idElement)
	
	def getinitialOpacity(self):
		return self.initialOpacity

	def setinitialOpacity(self, initialOpacity):
		self.initialOpacity = initialOpacity

	def gettag(self):
		return super().gettag()

	def settag(self, tag):
		super().settag(tag)

	def getName(self):
		return super().getname()

	def setName(self, name):
		super().setname(name)

	def getChildren(self):
		return super().getChildren()
  
	def setChildren(self, nchildren):
		super().setChildren(nchildren)

	def addChildren(self,elem):
		super().addChildren(elem)

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

	def gettopmostnode(self):
		return self.topmostnode

	def settopmostnode(self, topmostnode):
		self.topmostnode = topmostnode

	def gethasAnimation(self):
		"""@ReturnType boolean"""
		return self.hasAnimation

	def sethasAnimation(self, hasAnimation):
		"""@ParamType type boolean
		@ReturnType void"""
		self.hasAnimation = hasAnimation
  
	def gettypeElement(self):
		return super().gettype()

	def settypeElement(self,typelem):
		super().settype(typelem)

	def gethascondvisib(self):
		return self.hasConditionalVisibility

	def sethascondvisib(self, hascondvisib):
		self.hasConditionalVisibility = hascondvisib

	def setInteractions(self, interactions):
		self.interactions = interactions

	def addInteractionsList(self,interactions):
		self.interactions.extend(interactions)

	def __str__(self):
		return "(id: " + str(self.idElement) + "; tag: " + str(self.gettag()) + "; children : ["+ ''.join(str(c) for c in self.getChildren()) + "]" + "; interactions : ["+ ''.join(str(c) for c in self.interactions) + "])"

