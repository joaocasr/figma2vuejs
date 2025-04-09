#!/usr/bin/python
# -*- coding: UTF-8 -*-
class FormStyle(object):

	def __init__(self,backgroundcolor,backgroundcolorbtn,widthinput,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.backgroundcolor = backgroundcolor
		self.widthinput = widthinput
		self.backgroundcolorbtn = backgroundcolorbtn
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

	def getwidthinput(self):
		return self.widthinput

	def setwidthinput(self, widthinput):
		self.widthinput = widthinput

	def getbackgroundcolorbtn(self):
		return self.backgroundcolorbtn

	def setbackgroundcolorbtn(self, backgroundcolorbtn):
		self.backgroundcolorbtn = backgroundcolorbtn

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

	def setPosition(self, position):
		"""@ParamType position String
		@ReturnType void"""
		self.position = position

	def getPosition(self):
		"""@ReturnType String"""
		return self.position

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
