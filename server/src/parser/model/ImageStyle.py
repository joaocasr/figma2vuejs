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
		self.hashover = False
		self.opacity = None
		self.cornerRadius = None
		self.display = None
		self.borderTopLeftRadius = None
		self.borderTopRightRadius = None
		self.borderBottomLeftRadius = None
		self.borderBottomRightRadius = None
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

	def getDisplay(self):
		"""@ReturnType String"""
		return self.display

	def setDisplay(self, display):
		"""@ParamType display String
		@ReturnType void"""
		self.display = display

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
		return self.opacity

	def setOpacity(self,opacity):
		self.opacity=opacity
  
	def gethashoverProperty(self):
		return self.hashover

	def sethashoverProperty(self,hashover):
		self.hashover = hashover

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

	def getBorderTopLeftRadius(self):
		return self.borderTopLeftRadius

	def getBorderTopRightRadius(self):
		return self.borderTopRightRadius

	def getBorderBottomLeftRadius(self):
		return self.borderBottomLeftRadius

	def getBorderBottomRightRadius(self):
		return self.borderBottomRightRadius

	def setBorderTopLeftRadius(self,borderTopLeftRadius):
		self.borderTopLeftRadius = borderTopLeftRadius

	def setBorderTopRightRadius(self,borderTopRightRadius):
		self.borderTopRightRadius = borderTopRightRadius

	def setBorderBottomLeftRadius(self,borderBottomLeftRadius):
		self.borderBottomLeftRadius = borderBottomLeftRadius

	def setBorderBottomRightRadius(self,borderBottomRightRadius):
		self.borderBottomRightRadius = borderBottomRightRadius

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
