#!/usr/bin/python
# -*- coding: UTF-8 -*-
class DatePickerStyle(object):

	def __init__(self,backgroundcolor,dropdownbackgroundcolor,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.backgroundcolor = backgroundcolor
		self.dropdownbackgroundcolor = dropdownbackgroundcolor
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.gridArea = None

	def getbackgroundcolor(self):
		return self.backgroundcolor

	def setbackgroundcolor(self, backgroundcolor):
		self.backgroundcolor = backgroundcolor

	def getdropdownbackgroundcolor(self):
		return self.dropdownbackgroundcolor

	def setdropdownbackgroundcolor(self, dropdownbackgroundcolor):
		self.dropdownbackgroundcolor = dropdownbackgroundcolor

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

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
