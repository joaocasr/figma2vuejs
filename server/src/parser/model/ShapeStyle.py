#!/usr/bin/python
# -*- coding: UTF-8 -*-
class ShapeStyle(object):

	def __init__(self,x,y,width,height,gridcolumnStart,gridcolumnEnd,gridrowStart,gridrowEnd):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.background = None
		self.backgroundColor = None
		self.gridcolumnStart = gridcolumnStart
		self.gridcolumnEnd = gridcolumnEnd
		self.gridrowStart = gridrowStart
		self.gridrowEnd = gridrowEnd
		self.transform = None
		self.gridArea = None
		self.boxShadow = None
		self.individualStrokeweights = None
		self.display = None
		self.gridtemplatecolumns = None
		self.gridtemplaterows = None
		self.hashover = False
		self.opacity = None
		self.borderTopLeftRadius = None
		self.borderTopRightRadius = None
		self.borderBottomLeftRadius = None
		self.borderBottomRightRadius = None
		self.borderColor = None
		self.borderWidth = None
		self.borderRadius = None
		self.gap = None

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

	def getDisplay(self):
		"""@ReturnType String"""
		return self.display

	def setDisplay(self, display):
		"""@ParamType display String
		@ReturnType void"""
		self.display = display

	def getBackground(self):
		"""@ReturnType String"""
		return self.background

	def setBackground(self, background):
		"""@ParamType background String
		@ReturnType void"""
		self.background = background

	def getBackgroundColor(self):
		"""@ReturnType String"""
		return self.backgroundColor

	def setBackgroundColor(self, backgroundColor):
		"""@ParamType backgroundColor String
		@ReturnType void"""
		self.backgroundColor = backgroundColor

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

	def getBorderColor(self):
		"""@ReturnType String"""
		return self.borderColor

	def setBorderColor(self, borderColor):
		"""@ParamType borderColor String
		@ReturnType void"""
		self.borderColor = borderColor

	def getborderWidth(self):
		"""@ReturnType String"""
		return self.borderWidth

	def setborderWidth(self, borderWidth):
		"""@ParamType borderWidth String
		@ReturnType void"""
		self.borderWidth = borderWidth

	def getborderRadius(self):
		"""@ReturnType String"""
		return self.borderRadius

	def setborderRadius(self, borderRadius):
		"""@ParamType borderRadius String
		@ReturnType void"""
		self.borderRadius = borderRadius

	def getIndividualStrokeWeights(self):
		"""@ReturnType dict"""
		return self.individualStrokeweights

	def setIndividualStrokeWeights(self, individualStrokeweights):
		"""@ParamType individualStrokeweights dict
		@ReturnType void"""
		self.individualStrokeweights = individualStrokeweights

	def getOpacity(self):
		return self.opacity

	def setOpacity(self,opacity):
		self.opacity=opacity
  
	def gethashoverProperty(self):
		return self.hashover

	def sethashoverProperty(self,hashover):
		self.hashover = hashover

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

	def getGridTemplateColumns(self):
		return self.gridtemplatecolumns

	def setGridTemplateColumns(self, gridtemplatecolumns):
		self.gridtemplatecolumns = gridtemplatecolumns

	def getGridTemplateRows(self):
		return self.gridtemplaterows

	def setGridTemplateRows(self, gridtemplaterows):
		self.gridtemplaterows = gridtemplaterows

	def getTransform(self):
		"""@ReturnType String"""
		return self.transform

	def setTransform(self, transform):
		"""@ParamType transform String
		@ReturnType void"""
		self.transform = transform

