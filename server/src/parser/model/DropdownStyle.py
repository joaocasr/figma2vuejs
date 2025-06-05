#!/usr/bin/python
# -*- coding: UTF-8 -*-
class DropdownStyle(object):

	def __init__(self,option_hover_background_color,option_focused_background_color,menu_background_color,placeholder_color,background_color,menu_option_selected_background_color,menu_option_selected_color,
	borderRadius,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.option_hover_background_color= option_hover_background_color
		self.option_focused_background_color= option_focused_background_color
		self.menu_background_color= menu_background_color
		self.placeholder_color= placeholder_color
		self.background_color= background_color
		self.menu_option_selected_background_color = menu_option_selected_background_color
		self.menu_option_selected_color = menu_option_selected_color
		self.borderRadius = borderRadius
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.width = None
		self.height = None
		self.position = None
		self.gridArea = None

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

	def setborderRadius(self, borderRadius):
		"""@ParamType borderRadius String
		@ReturnType void"""
		self.borderRadius = borderRadius

	def getborderRadius(self):
		"""@ReturnType String"""
		return self.borderRadius

	def getgridArea(self):
		return self.gridArea

	def setgridArea(self, gridarea):
		self.gridArea = gridarea
