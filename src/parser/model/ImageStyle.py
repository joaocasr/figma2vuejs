#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ImageElement

class ImageStyle(object):
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

	def getCornerRadius(self):
		"""@ReturnType String"""
		return self.cornerRadius

	def setCornerRadius(self, cornerRadius):
		"""@ParamType cornerRadius String
		@ReturnType void"""
		self.cornerRadius = cornerRadius

	def __init__(self):
		self.height = None
		"""@AttributeType String"""
		self.width = None
		"""@AttributeType String"""
		self.gridcolumnStart = None
		"""@AttributeType String"""
		self.gridcolumnEnd = None
		"""@AttributeType String"""
		self.gridrowStart = None
		"""@AttributeType String"""
		self.gridrowEnd = None
		"""@AttributeType String"""
		self.opacity = None
		"""@AttributeType String"""
		self.cornerRadius = None
		"""@AttributeType String"""
		self.unnamed_ImageElement_ = None
		"""@AttributeType ImageElement
		# @AssociationType ImageElement"""

