#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import Melement
#import Mcomponent
#import Entity

class Mpage(object):

	def __init__(self,name,path,id,pagestyle=None):
		self.pagename = name
		self.pagepath = path
		self.idpage = id
		self.elements = []
		self.components = []
		self.data = []
		self.containerstyle = pagestyle

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

	def setPageStyle(self, style):
		self.containerstyle = style

	def __str__(self):
		allelements=""
		for e in self.elements:
			allelements += str(e) + ";"
		return "name:" + self.pagename + ", "+ "path:" + self.pagepath + ", elements: [" + allelements + "] , style: "+ str(self.containerstyle)
