#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import List

class PageItem(object):
	def __init__(self,id,name,tag,type,elementos):
		self.id = id
		self.name = name
		self.tag = tag
		self.type = type
		self.children:List[PageItem] = elementos

	def getId(self):
		return self.id

	def getname(self):
		return self.name

	def gettag(self):
		return self.tag

	def gettype(self):
		return self.type

	def setId(self,id):
		self.id=id

	def setname(self,name):
		self.name=name

	def settag(self,tag):
		self.tag=tag

	def settype(self,type):
		self.type=type
  
	def getChildren(self):
		return self.children

	def setChildren(self,elementos):
		self.children=elementos
  
	def addChildren(self,elemento):
		self.children.append(elemento)