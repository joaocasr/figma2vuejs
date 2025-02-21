#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import Melement
import Mcomponent
import Entity

class Mpage(object):
	def getPagename(self):
		"""@ReturnType String"""
		return self.pagename

	def setPagename(self, pagename):
		"""@ParamType pagename String
		@ReturnType void"""
		self.pagename = pagename

	def getPagepath(self):
		"""@ReturnType String"""
		return self.pagepath

	def setPagepath(self, pagepath):
		"""@ParamType pagepath String
		@ReturnType void"""
		self.pagepath = pagepath

	def getIdpage(self):
		"""@ReturnType String"""
		return self.idpage

	def setIdpage(self, idpage):
		"""@ParamType idpage String
		@ReturnType void"""
		self.idpage = idpage

	def __init__(self):
		self.pagename = None
		"""@AttributeType String"""
		self.pagepath = None
		"""@AttributeType String"""
		self.idpage = None
		"""@AttributeType String"""
		self.elements = []
		"""@AttributeType Melement*
		# @AssociationType Melement[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Aggregation"""
		self.components = []
		"""@AttributeType Mcomponent*
		# @AssociationType Mcomponent[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Aggregation"""
		self.data = []
		"""@AttributeType Entity*
		# @AssociationType Entity[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Aggregation"""

