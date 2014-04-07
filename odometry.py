#!/usr/bin/env python

######################### ODOMETRY ######################### 
class encoder:
	def __init__(self, pinA, pinB):
		# TODO set pins and stuff
		self.zero()

	def zero(self):
		self.x = 0. # raw encoder position, tics
		self.v = 0. # raw encoder velocity, tics/sec
