#!/usr/bin/python
# -*- coding: UTF-8 -*-
class SliderStyle(object):

	def __init__(self,backgroundtrack,backgroundcontent,backgroundrange,colorhover,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.backgroundtrack = backgroundtrack
		self.backgroundcontent = backgroundcontent
		self.backgroundrange = backgroundrange
		self.colorhover = colorhover
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.position = None
		self.gridArea = None

	def getbackgroundtrack(self):
		return self.backgroundtrack

	def setbackgroundtrack(self, backgroundtrack):
		self.backgroundtrack = backgroundtrack

	def getbackgroundcontent(self):
		return self.backgroundcontent

	def setbackgroundcontent(self, backgroundcontent):
		self.backgroundcontent = backgroundcontent

	def getbackgroundrange(self):
		return self.backgroundrange

	def setbackgroundrange(self, backgroundrange):
		self.backgroundrange = backgroundrange

	def getcolorhover(self):
		return self.colorhover

	def setcolorhover(self, colorhover):
		self.colorhover = colorhover

	def getGridcolumnStart(self):
		"""@ReturnType String"""
		return self.gridcolumnStart

	def setGridcolumnStart(self, gridcolumnStart):
		"""@ParamType gridcolumnStart String
		@ReturnType void"""
		self.gridcolumnStart = gridcolumnStart

	def getGridcolumnEnd(self):
		"""@ReturnType String"""
		return self.gridcolumnEnd

	def setGridcolumnEnd(self, gridcolumnEnd):
		"""@ParamType gridcolumnEnd String
		@ReturnType void"""
		self.gridcolumnEnd = gridcolumnEnd

	def getGridrowStart(self):
		"""@ReturnType String"""
		return self.gridrowStart

	def setGridrowStart(self, gridrowStart):
		"""@ParamType gridrowStart String
		@ReturnType void"""
		self.gridrowStart = gridrowStart

	def getGridrowEnd(self):
		"""@ReturnType String"""
		return self.gridrowEnd

	def setGridrowEnd(self, gridrowEnd):
		"""@ParamType gridrowEnd String
		@ReturnType void"""
		self.gridrowEnd = gridrowEnd

	def setPosition(self, position):
		"""@ParamType position String
		@ReturnType void"""
		self.position = position

	def getPosition(self):
		"""@ReturnType String"""
		return self.position

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
