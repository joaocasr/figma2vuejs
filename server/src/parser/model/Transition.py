#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Transition(object):

	def __init__(self,type,direction,curve,duration):
		self.type = type
		self.direction = direction
		self.curve = curve
		self.duration = duration

	def getType(self):
		return self.type

	def setType(self,type):
		self.type = type

	def getDirection(self):
		return self.direction

	def setDirection(self,direction):
		self.direction = direction

	def getCurve(self):
		return self.curve

	def setCurve(self,curve):
		self.curve = curve

	def getDuration(self):
		return self.duration

	def setDuration(self,duration):
		self.duration = duration