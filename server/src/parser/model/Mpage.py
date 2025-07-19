#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List
from parser.model.PageItem import PageItem
from parser.model.Mcomponent import Mcomponent
from utils.tools import getId

class Mpage(object):

	def __init__(self,name,path,id,style=None):
		self.pagename = name
		self.pagepath = path
		self.idpage = id
		self.elements:List[PageItem] = []
		self.components:List[Mcomponent] = []
		self.data = []
		self.objectDL = {}
		self.props = []
		self.style = style

	def getPagename(self):
		"""@ReturnType String"""
		return self.pagename

	def setPagename(self, pagename):
		"""@ParamType pagename String
		@ReturnType void"""
		self.pagename = pagename

	def getPagepath(self):
		"""@ReturnType String"""
		return self.pagepath

	def setPagepath(self, pagepath):
		"""@ParamType pagepath String
		@ReturnType void"""
		self.pagepath = pagepath

	def getIdpage(self):
		"""@ReturnType String"""
		return self.idpage

	def setIdpage(self, idpage):
		"""@ParamType idpage String
		@ReturnType void"""
		self.idpage = idpage

	def getobjectDL(self):
		"""@ReturnType object"""
		return self.objectDL

	def setobjectDL(self, objectDL):
		"""@ParamType objectDL
		@ReturnType void"""
		self.objectDL = objectDL
  
	def assignPageStyle(self, style):
		self.style = style

	def addElement(self,element):
		exists = False
		for x in self.elements:
			if(getId(x)==getId(element)):
				self.elements[self.elements.index(x)] = element
				exists = True
		if(exists==False): self.elements.append(element)

	def addVariable(self,var):
		exists = False
		for k in list(var.keys()):
			for d in self.data:
				if(k in d.keys()):
					exists = True
		if(exists==False):
			self.data.append(var)
   
	def getData(self):
		return self.data
		
	def __str__(self):
		allelements=""
		allcomponents=""
		for e in self.elements:
			allelements += str(e) + ","
		for c in self.components:
			allcomponents += str(c) + ","
		return "name:" + str(self.pagename) + ", "+ "path:" + str(self.pagepath) + ", elements: [" + allelements + "]"+ ", components: [" + allcomponents + "], style: "+ str(self.style)
