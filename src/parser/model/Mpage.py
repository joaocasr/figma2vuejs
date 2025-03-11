#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Mpage(object):

	def __init__(self,name,path,id,style=None):
		self.pagename = name
		self.pagepath = path
		self.idpage = id
		self.elements = []
		self.components = []
		self.data = []
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

	def assignPageStyle(self, style):
		self.style = style

	def addElement(self,element):
		self.elements.append(element)

	def addVariable(self,var):
		return self.data.append(var)

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
