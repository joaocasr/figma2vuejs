#!/usr/bin/python
# -*- coding: UTF-8 -*-
import String
import Mpage
import InteractionElement
import Mcomponent

class Melement(object):
	def getIdElement(self):
		"""@ReturnType String"""
		return self.idElement

	def setIdElement(self, idElement):
		"""@ParamType idElement String
		@ReturnType void"""
		self.idElement = idElement

	def getTag(self):
		"""@ReturnType String"""
		return self.tag

	def setTag(self, tag):
		"""@ParamType tag String
		@ReturnType void"""
		self.tag = tag

	def __init__(self):
		self.idElement = None
		"""@AttributeType String"""
		self.tag = None
		"""@AttributeType String"""
		self.unnamed_Mpage_ = None
		"""@AttributeType Mpage
		# @AssociationType Mpage"""
		self.children = []
		"""@AttributeType Melement*
		# @AssociationType Melement[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Aggregation"""
		self.unnamed_Melement_ = None
		"""@AttributeType Melement
		# @AssociationType Melement"""
		self.unnamed_InteractionElement_ = []
		"""@AttributeType InteractionElement*
		# @AssociationType InteractionElement[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Aggregation"""
		self.unnamed_Mcomponent_ = None
		"""@AttributeType Mcomponent
		# @AssociationType Mcomponent"""

