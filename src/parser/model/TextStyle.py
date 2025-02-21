#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import TextElement

class TextStyle(object):
	def getTextAlign(self):
		"""@ReturnType String"""
		return self.textAlign

	def setTextAlign(self, textAlign):
		"""@ParamType textAlign String
		@ReturnType void"""
		self.textAlign = textAlign

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

	def __init__(self):
		self.textAlign = None
		"""@AttributeType String"""
		self.textDecoration = None
		"""@AttributeType String"""
		self.textIndent = None
		"""@AttributeType String"""
		self.textTransform = None
		"""@AttributeType String"""
		self.fontStyle = None
		"""@AttributeType String"""
		self.fontWeight = None
		"""@AttributeType String"""
		self.fontSize = None
		"""@AttributeType String"""
		self.fontFamily = None
		"""@AttributeType String"""
		self.lineHeight = None
		"""@AttributeType String"""
		self.color = None
		"""@AttributeType String"""
		self.letterSpacing = None
		"""@AttributeType String"""
		self.cursor = None
		"""@AttributeType String"""
		self.transition = None
		"""@AttributeType String"""
		self.opacity = None
		"""@AttributeType String"""
		self.gridcolumnStart = None
		"""@AttributeType String"""
		self.gridcolumnEnd = None
		"""@AttributeType String"""
		self.gridrowStart = None
		"""@AttributeType String"""
		self.gridrowEnd = None
		"""@AttributeType String"""
		self.unnamed_TextElement_ = None
		"""@AttributeType TextElement
		# @AssociationType TextElement"""

