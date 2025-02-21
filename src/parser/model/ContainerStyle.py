#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import ContainerElement

class ContainerStyle(object):
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

	def getBackgroundColor(self):
		"""@ReturnType String"""
		return self.backgroundColor

	def setBackgroundColor(self, backgroundColor):
		"""@ParamType backgroundColor String
		@ReturnType void"""
		self.backgroundColor = backgroundColor

	def getBackgroundImage(self):
		"""@ReturnType String"""
		return self.backgroundImage

	def setBackgroundImage(self, backgroundImage):
		"""@ParamType backgroundImage String
		@ReturnType void"""
		self.backgroundImage = backgroundImage

	def getDisplay(self):
		"""@ReturnType String"""
		return self.display

	def setDisplay(self, display):
		"""@ParamType display String
		@ReturnType void"""
		self.display = display

	def getMargin(self):
		"""@ReturnType String"""
		return self.margin

	def setMargin(self, margin):
		"""@ParamType margin String
		@ReturnType void"""
		self.margin = margin

	def getPadding(self):
		"""@ReturnType String"""
		return self.padding

	def setPadding(self, padding):
		"""@ParamType padding String
		@ReturnType void"""
		self.padding = padding

	def getBorder(self):
		"""@ReturnType String"""
		return self.border

	def setBorder(self, border):
		"""@ParamType border String
		@ReturnType void"""
		self.border = border

	def getBorderColor(self):
		"""@ReturnType String"""
		return self.borderColor

	def setBorderColor(self, borderColor):
		"""@ParamType borderColor String
		@ReturnType void"""
		self.borderColor = borderColor

	def getBorderWidth(self):
		"""@ReturnType String"""
		return self.borderWidth

	def setBorderWidth(self, borderWidth):
		"""@ParamType borderWidth String
		@ReturnType void"""
		self.borderWidth = borderWidth

	def getBorderStyle(self):
		"""@ReturnType String"""
		return self.borderStyle

	def setBorderStyle(self, borderStyle):
		"""@ParamType borderStyle String
		@ReturnType void"""
		self.borderStyle = borderStyle

	def getBorderRadius(self):
		"""@ReturnType String"""
		return self.borderRadius

	def setBorderRadius(self, borderRadius):
		"""@ParamType borderRadius String
		@ReturnType void"""
		self.borderRadius = borderRadius

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

	def getBoxShadow(self):
		"""@ReturnType String"""
		return self.boxShadow

	def setBoxShadow(self, boxShadow):
		"""@ParamType boxShadow String
		@ReturnType void"""
		self.boxShadow = boxShadow

	def __init__(self):
		self.width = None
		"""@AttributeType int"""
		self.height = None
		"""@AttributeType int"""
		self.backgroundColor = None
		"""@AttributeType String"""
		self.backgroundImage = None
		"""@AttributeType String"""
		self.display = None
		"""@AttributeType String"""
		self.margin = None
		"""@AttributeType String"""
		self.padding = None
		"""@AttributeType String"""
		self.border = None
		"""@AttributeType String"""
		self.borderColor = None
		"""@AttributeType String"""
		self.borderWidth = None
		"""@AttributeType String"""
		self.borderStyle = None
		"""@AttributeType String"""
		self.borderRadius = None
		"""@AttributeType String"""
		self.gridcolumnStart = None
		"""@AttributeType String"""
		self.gridcolumnEnd = None
		"""@AttributeType String"""
		self.gridrowStart = None
		"""@AttributeType String"""
		self.gridrowEnd = None
		"""@AttributeType String"""
		self.boxShadow = None
		"""@AttributeType String"""
		self.unnamed_ContainerElement_ = None
		"""@AttributeType ContainerElement
		# @AssociationType ContainerElement"""

