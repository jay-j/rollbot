#!/usr/bin/env python
# all position-tracking functions (encoders, imu, etc)

######################### ODOMETRY ######################### 
# combine sensor data
# store robot state in the global structure (defined in utils.py)
# TODO

######################### ENCODERS ######################### 
class encoder:
	def __init__(self, pinA, pinB):
		# TODO set pins and stuff
		self.zero()

	def zero(self):
		self.x = 0. # raw encoder position, tics
		self.v = 0. # raw encoder velocity, tics/sec

######################### IMU ######################### 
# TODO
