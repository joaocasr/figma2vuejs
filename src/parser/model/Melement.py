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

	def getIdElement(self):
		return self.idElement

	def setIdElement(self, idElement):
		self.idElement = idElement

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

	def getInteractions(self):
		return self.interactions

	def setInteractions(self, interactions):
		self.interactions = interactions

	def __str__(self):
		return "(id: " + str(self.idElement) + "; tag: " + str(self.tag) + "; children : ["+ ''.join(str(c) for c in self.children) + "]" + "; interactions : ["+ ''.join(str(c) for c in self.interactions) + "])"

