#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.PageItem import PageItem

class Mcomponent(PageItem):
	def __init__(self,id,name,tag,type,elementos=[]):
		self.style = None
		self.interactions = []
		self.data = []
		self.props = {}
		self.hasCloseAction = False
		self.upperIdComponent = None
		self.zindex = 0
		self.isComponentInstance = False
		self.initialOpacity = None
		self.hasAnimation = False
		self.hasConditionalVisibility = False
		self.isVariant = False
		self.variantName = None
		self.isOverlay = False
		self.topmostnode = None
		super().__init__(id,name,tag,type,elementos) 

	def getIdComponent(self):
		"""@ReturnType String"""
		return super().getId()

	def setIdComponent(self, idComponent):
		"""@ParamType idComponent String
		@ReturnType void"""
		super().setId(idComponent)

	def getNameComponent(self):
		"""@ReturnType String"""
		return super().getname()

	def setNameComponent(self, name):
		"""@ParamType componentName String
		@ReturnType void"""
		super().setname(name)

	def gettag(self):
		"""@ReturnType String"""
		return super().gettag()

	def setTagComponent(self, tag):
		"""@ParamType tag String
		@ReturnType void"""
		super().settag(tag)

	def getTypeComponent(self):
		"""@ReturnType String"""
		return super().gettype()

	def setTypeComponent(self, type):
		"""@ParamType type String
		@ReturnType void"""
		super().settype(type)

	def gethasAnimation(self):
		"""@ReturnType boolean"""
		return self.hasAnimation

	def sethasAnimation(self, hasAnimation):
		"""@ParamType type boolean
		@ReturnType void"""
		self.hasAnimation = hasAnimation
  
	def setComponentStyle(self, style):
		"""@ParamType type String
		@ReturnType void"""
		self.style = style

	def getComponentStyle(self):
		"""@ParamType type String
		@ReturnType void"""
		return self.style

	def getisVariant(self):
		return self.isVariant

	def setisVariant(self, isVariant):
		self.isVariant = isVariant
	
	def getinitialOpacity(self):
		return self.initialOpacity

	def setinitialOpacity(self, initialOpacity):
		self.initialOpacity = initialOpacity
  
	def getupperIdComponent(self):
		return self.upperIdComponent

	def setupperIdComponent(self, id):
		self.upperIdComponent = id

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data

	def getProps(self):
		"""@ReturnType object"""
		return self.props

	def setProps(self, props):
		"""@ParamType props
		@ReturnType void"""
		self.props = props

	def addVariable(self,var):
		exists = False
		for k in list(var.keys()):
			for d in self.data:
				if(k in d.keys()):
					exists = True
		if(exists==False):
			self.data.append(var)

	def getHasCloseAction(self):
		return self.hasCloseAction

	def setHasCloseAction(self, hasCloseAction):
		self.hasCloseAction = hasCloseAction

	def getChildren(self):
		return super().getChildren()
  
	def setChildren(self, nchildren):
		super().setChildren(nchildren)

	def addChildren(self,elem):
		super().addChildren(elem)
  
	def getzindex(self):
		return self.zindex

	def setzindex(self, zindex):
		self.zindex = zindex

	def getisComponentInstance(self):
		"""@ReturnType String"""
		return self.isComponentInstance

	def setisComponentInstance(self, isComponentInstance):
		"""@ParamType isComponentInstance String
		@ReturnType void"""
		self.isComponentInstance = isComponentInstance

	def getVariantName(self):
		return self.variantName

	def setVariantName(self, variantName):
		self.variantName = variantName

	def gethascondvisib(self):
		return self.hasConditionalVisibility

	def sethascondvisib(self, hascondvisib):
		self.hasConditionalVisibility = hascondvisib

	def gettopmostnode(self):
		return self.topmostnode

	def settopmostnode(self, topmostnode):
		self.topmostnode = topmostnode

	def getInteractions(self):
		return self.interactions

	def setInteractions(self, interactions):
		self.interactions = interactions

	def addInteractionsList(self,interactions):
		self.interactions.extend(interactions)

	def __str__(self):
		return "(id: " + str(self.idComponent) + ",name: "+  str(self.componentName) + ",type: "+  str(self.type) + ",tag: "+  str(self.gettag()) + "; interactions: ["+ ";".join(str(val) for val in self.interactions)  +"]" + ", children: [" + ";".join(str(val) for val in self.getChildren()) + "],"+ "data: ["+ ";".join(str(val) for val in self.data)  +"])" 