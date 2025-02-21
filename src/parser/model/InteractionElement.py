#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Melement
import ElementAction

class InteractionElement(object):
	def getInteractionType(self):
		"""@ReturnType String"""
		pass

	def setInteractionType(self, interactionType):
		"""@ParamType interactionType String
		@ReturnType void"""
		pass

	def __init__(self):
		self.triggerType = None
		"""@AttributeType String"""
		self.unnamed_Melement_ = None
		"""@AttributeType Melement
		# @AssociationType Melement"""
		self.action = []
		"""@AttributeType ElementAction*
		# @AssociationType ElementAction[]
		# @AssociationMultiplicity 0..*
		# @AssociationKind Composition"""

