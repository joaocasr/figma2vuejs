#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Mpage
import Melement

class Mcomponent(object):
	def getIdComponent(self):
		"""@ReturnType String"""
		return self.idComponent

	def setIdComponent(self, idComponent):
		"""@ParamType idComponent String
		@ReturnType void"""
		self.idComponent = idComponent

	def __init__(self):
		self.idComponent = None
		"""@AttributeType String"""
		self.unnamed_Mpage_ = None
		"""@AttributeType Mpage
		# @AssociationType Mpage"""
		self.elements = []
		"""@AttributeType Melement*
		# @AssociationType Melement[]
		# @AssociationMultiplicity 1..*
		# @AssociationKind Composition"""

