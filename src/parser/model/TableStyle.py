#!/usr/bin/python
# -*- coding: UTF-8 -*-
class TableStyle(object):

	def __init__(self,backgroundHeader,backgroundBody,textColor,headertextColor,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.backgroundHeader = backgroundHeader
		self.backgroundBody = backgroundBody
		self.textColor = textColor
		self.headertextColor = headertextColor
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.gridArea = None

	def getbackgroundHeader(self):
		return self.backgroundHeader

	def setbackgroundHeader(self, backgroundHeader):
		self.backgroundHeader = backgroundHeader

	def getbackgroundBody(self):
		return self.backgroundBody

	def setbackgroundBody(self, backgroundBody):
		self.backgroundBody = backgroundBody

	def gettextColor(self):
		return self.textColor

	def settextColor(self, textColor):
		self.textColor = textColor

	def getheadertextColor(self):
		return self.headertextColor

	def setheadertextColor(self, headertextColor):
		self.headertextColor = headertextColor

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

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
