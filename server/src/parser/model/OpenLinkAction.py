#!/usr/bin/python
# -*- coding: UTF-8 -*-
from  parser.model.ElementAction import ElementAction

class OpenLinkAction(ElementAction):
	def __init__(self,url,openInNewTab,transition):

		super().__init__("URL",transition) 
		self.url = url
		self.openInNewTab = openInNewTab

	def getUrl(self):
		"""@ReturnType url"""
		return self.url

	def setUrl(self, url):
		"""@ParamType url String
		@ReturnType void"""
		self.url = url

	def getopenInNewTab(self):
		"""@ReturnType openInNewTab"""
		return self.openInNewTab

	def setopenInNewTab(self, openInNewTab):
		"""@ParamType openInNewTab String
		@ReturnType void"""
		self.openInNewTab = openInNewTab