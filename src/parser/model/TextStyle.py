#!/usr/bin/python
# -*- coding: UTF-8 -*-
class TextStyle(object):
	def __init__(self,x,y,width,height,horizontalalign,lineheight,autoresize,font,weight,size,family,color,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.textHorizontalAlign = horizontalalign
		self.textDecoration = None
		self.textIndent = None
		self.textTransform = None
		self.fontStyle = font
		self.fontWeight = weight
		self.fontSize = size
		self.fontFamily = family
		self.lineHeight = lineheight
		self.color = color
		self.textAutoResize = autoresize
		self.letterSpacing = None
		self.cursor = None
		self.transition = None
		self.opacity = None
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd

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

	def getTextAlign(self):
		"""@ReturnType String"""
		return self.textHorizontalAlign

	def setTextAlign(self, textAlign):
		"""@ParamType textAlign String
		@ReturnType void"""
		self.textHorizontalAlign = textAlign

	def getTextDecoration(self):
		"""@ReturnType String"""
		return self.textDecoration

	def setTextDecoration(self, textDecoration):
		"""@ParamType textDecoration String
		@ReturnType void"""
		self.textDecoration = textDecoration

	def getTextIndent(self):
		"""@ReturnType String"""
		return self.textIndent

	def setTextIndent(self, textIndent):
		"""@ParamType textIndent String
		@ReturnType void"""
		self.textIndent = textIndent

	def getTextTransform(self):
		"""@ReturnType String"""
		return self.textTransform

	def setTextTransform(self, textTransform):
		"""@ParamType textTransform String
		@ReturnType void"""
		self.textTransform = textTransform

	def getFontStyle(self):
		"""@ReturnType String"""
		return self.fontStyle

	def setFontStyle(self, fontStyle):
		"""@ParamType fontStyle String
		@ReturnType void"""
		self.fontStyle = fontStyle

	def getFontWeight(self):
		"""@ReturnType String"""
		return self.fontWeight

	def setFontWeight(self, fontWeight):
		"""@ParamType fontWeight String
		@ReturnType void"""
		self.fontWeight = fontWeight

	def getFontSize(self):
		"""@ReturnType String"""
		return self.fontSize

	def setFontSize(self, fontSize):
		"""@ParamType fontSize String
		@ReturnType void"""
		self.fontSize = fontSize

	def getFontFamily(self):
		"""@ReturnType String"""
		return self.fontFamily

	def setFontFamily(self, fontFamily):
		"""@ParamType fontFamily String
		@ReturnType void"""
		self.fontFamily = fontFamily

	def getLineHeight(self):
		"""@ReturnType String"""
		return self.lineHeight

	def setLineHeight(self, lineHeight):
		"""@ParamType lineHeight String
		@ReturnType void"""
		self.lineHeight = lineHeight

	def getTextAutoResize(self):
		"""@ReturnType String"""
		return self.textAutoResize

	def setTextAutoResize(self, autoresize):
		"""@ParamType textAutoResize String
		@ReturnType void"""
		self.textAutoResize = autoresize

	def getColor(self):
		"""@ReturnType String"""
		return self.color

	def setColor(self, color):
		"""@ParamType color String
		@ReturnType void"""
		self.color = color

	def getLetterSpacing(self):
		"""@ReturnType String"""
		return self.letterSpacing

	def setLetterSpacing(self, letterSpacing):
		"""@ParamType letterSpacing String
		@ReturnType void"""
		self.letterSpacing = letterSpacing

	def getCursor(self):
		"""@ReturnType String"""
		return self.cursor

	def setCursor(self, cursor):
		"""@ParamType cursor String
		@ReturnType void"""
		self.cursor = cursor

	def getTransition(self):
		"""@ReturnType String"""
		return self.transition

	def setTransition(self, transition):
		"""@ParamType transition String
		@ReturnType void"""
		self.transition = transition

	def getOpacity(self):
		"""@ReturnType String"""
		return self.opacity

	def setOpacity(self, opacity):
		"""@ParamType opacity String
		@ReturnType void"""
		self.opacity = opacity

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

	def __str__(self):
		return "fontStyle:" + str(self.fontStyle) +",\n"+"fontWeight:" + str(self.fontWeight) +",\n"+ "fontSize:" + self.fontSize +",\n"+ "fontFamily:" + self.fontFamily +",\n"+ "color:" + self.color +",\n"+ "gridcolumnStart:" + self.gridcolumnStart +",\n"+ "gridcolumnEnd:" + str(self.gridcolumnEnd) +",\n"+ "gridrowStart:" + str(self.gridrowStart) +",\n"+ "gridrowEnd:" + str(self.gridrowEnd)