#!/usr/bin/python
# -*- coding: UTF-8 -*-
class ImageStyle(object):

	def __init__(self,x,y,height,width,gridcolumnstart,gridcolumnend,gridrowstart,gridrowend):
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.gridcolumnStart = gridcolumnstart
		self.gridcolumnEnd = gridcolumnend
		self.gridrowStart = gridrowstart
		self.gridrowEnd = gridrowend
		self.boxShadow = None
		self.opacity = None
		self.cornerRadius = None
		self.gridArea = None

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

	def getHeight(self):
		"""@ReturnType String"""
		return self.height

	def setHeight(self, height):
		"""@ParamType height String
		@ReturnType void"""
		self.height = height

	def getWidth(self):
		"""@ReturnType String"""
		return self.width

	def setWidth(self, width):
		"""@ParamType width String
		@ReturnType void"""
		self.width = width

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

	def getOpacity(self):
		"""@ReturnType String"""
		return self.opacity

	def setOpacity(self, opacity):
		"""@ParamType opacity String
		@ReturnType void"""
		self.opacity = opacity

	def getBoxShadow(self):
		"""@ReturnType String"""
		return self.boxShadow

	def setBoxShadow(self, boxShadow):
		"""@ParamType boxShadow String
		@ReturnType void"""
		self.boxShadow = boxShadow

	def getCornerRadius(self):
		"""@ReturnType String"""
		return self.cornerRadius

	def setCornerRadius(self, cornerRadius):
		"""@ParamType cornerRadius String
		@ReturnType void"""
		self.cornerRadius = cornerRadius

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
