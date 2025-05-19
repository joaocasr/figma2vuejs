#!/usr/bin/python
# -*- coding: UTF-8 -*-
class CheckboxStyle(object):

	def __init__(self,colortxt,colorbackground,boxRadius,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.colortxt = colortxt
		self.colorbackground = colorbackground
		self.gridcolumnStart = gridcolumnStart
		self.boxRadius = boxRadius
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.width = None
		self.height = None
		self.x = None
		self.y = None
		self.position = None
		self.gridArea = None

	def getColortxt(self):
		"""@ReturnType String"""
		return self.colortxt

	def setColortxt(self, colortxt):
		"""@ParamType colortxt String
		@ReturnType void"""
		self.colortxt = colortxt

	def getColorBackground(self):
		"""@ReturnType String"""
		return self.colorbackground

	def setColorBackground(self, color):
		"""@ParamType colorbackground String
		@ReturnType void"""
		self.colorbackground = color

	def getboxRadius(self):
		"""@ReturnType String"""
		return self.boxRadius

	def setboxRadius(self, boxRadius):
		"""@ParamType boxRadius String
		@ReturnType void"""
		self.boxRadius = boxRadius

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

	def getWidth(self):
		"""@ReturnType int"""
		return self.width

	def setWidth(self, width):
		"""@ParamType width int
		@ReturnType void"""
		self.width = width

	def getHeight(self):
		"""@ReturnType int"""
		return self.height

	def setHeight(self, height):
		"""@ParamType height int
		@ReturnType void"""
		self.height = height

	def getX(self):
		"""@ReturnType int"""
		return self.x

	def setX(self, x):
		"""@ParamType width int
		@ReturnType void"""
		self.x = x

	def getY(self):
		"""@ReturnType int"""
		return self.y

	def setY(self, y):
		"""@ParamType width int
		@ReturnType void"""
		self.y = y
  
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
