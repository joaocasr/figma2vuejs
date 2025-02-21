#!/usr/bin/python
# -*- coding: UTF-8 -*-

import TableElement
import ContainerStyle

class TableStyle(ContainerStyle):
	def getBorderCollapse(self):
		"""@ReturnType String"""
		return self.borderCollapse

	def setBorderCollapse(self, borderCollapse):
		"""@ParamType borderCollapse String
		@ReturnType void"""
		self.borderCollapse = borderCollapse

	def getWidth(self):
		"""@ReturnType String"""
		return self.width

	def setWidth(self, width):
		"""@ParamType width String
		@ReturnType void"""
		self.width = width

	def getBorder(self):
		"""@ReturnType String"""
		return self.border

	def setBorder(self, border):
		"""@ParamType border String
		@ReturnType void"""
		self.border = border

	def getPadding(self):
		"""@ReturnType String"""
		return self.padding

	def setPadding(self, padding):
		"""@ParamType padding String
		@ReturnType void"""
		self.padding = padding

	def getListstylePadding(self):
		"""@ReturnType String"""
		return self.liststylePadding

	def setListstylePadding(self, liststylePadding):
		"""@ParamType liststylePadding String
		@ReturnType void"""
		self.liststylePadding = liststylePadding

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

	def setGridcolumnEnd(self, gridColumnEnd):
		"""@ParamType gridColumnEnd String
		@ReturnType void"""
		self.gridcolumnEnd = gridColumnEnd

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
		self.borderCollapse = None
		"""@AttributeType String"""
		self.width = None
		"""@AttributeType String"""
		self.border = None
		"""@AttributeType String"""
		self.padding = None
		"""@AttributeType String"""
		self.liststylePadding = None
		"""@AttributeType String"""
		self.gridcolumnStart = None
		"""@AttributeType String"""
		self.gridcolumnEnd = None
		"""@AttributeType String"""
		self.gridrowStart = None
		"""@AttributeType String"""
		self.gridrowEnd = None
		"""@AttributeType String"""
		self.unnamed_TableElement_ = None
		"""@AttributeType TableElement
		# @AssociationType TableElement"""

