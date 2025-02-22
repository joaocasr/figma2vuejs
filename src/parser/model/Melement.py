#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Melement(object):

	def __init__(self,id,tag):
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

	def setChildren(self, nchildren):
		self.children = nchildren

	def __str__(self):
		return str(self.idElement) + "" + str(self.tag)

