#!/usr/bin/python
# -*- coding: UTF-8 -*-
class PaginatorStyle(object):

	def __init__(self,borderRadius,selectedColor,color,backgroundColor,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.borderRadius = borderRadius
		self.selectedColor = selectedColor
		self.color = color
		self.backgroundColor = backgroundColor
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.position = None
		self.gridArea = None

	def getborderRadius(self):
		return self.borderRadius

	def setborderRadius(self, borderRadius):
		self.borderRadius = borderRadius

	def getselectedColor(self):
		return self.selectedColor

	def setselectedColor(self, selectedColor):
		self.selectedColor = selectedColor

	def getcolor(self):
		return self.color

	def setcolor(self, color):
		self.color = color

	def getbackgroundColor(self):
		return self.backgroundColor

	def setbackgroundColor(self, backgroundColor):
		self.backgroundColor = backgroundColor

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

	def __string__(self):
		return "star-color:"+self.starColor+",background-color:"+self.unselectedStarColor