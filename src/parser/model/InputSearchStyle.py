#!/usr/bin/python
# -*- coding: UTF-8 -*-
class InputSearchStyle(object):

	def __init__(self,backgroundcolor,color,borderradius,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.backgroundcolor = backgroundcolor
		self.color = color
		self.borderradius = borderradius
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.position = None
		self.gridArea = None

	def getbackgroundcolor(self):
		return self.backgroundcolor

	def setbackgroundcolor(self, backgroundcolor):
		self.backgroundcolor = backgroundcolor

	def getcolor(self):
		return self.color

	def setcolor(self, color):
		self.color = color

	def getborderradius(self):
		return self.borderradius

	def setborderradius(self, borderradius):
		self.borderradius = borderradius

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
