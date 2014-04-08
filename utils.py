#!/usr/bin/env python
# Robot Utils
from math import *

class robot:
	# current (measured) state
	x = 0.0
	y = 0.0
	th = 0.0

	# key dimensions / parameters
	TICS_PER_INCH = 360.0/(pi*9.125)
	INCH_PER_TIC = 1.0 / float(TICS_PER_INCH)
	WIDTH = 11.25

# measure shortest angle from start to goal
# signs are correct, +/- pi flip is handled correctly
def measureAngle(measureStart, measureGoal):
	return atan2(sin(measureGoal-measureStart), cos(measureGoal-measureStart))

# rotate angle from initial by change
# again, signed and safe!
def rotate(rStart, rChange):
	return atan2(sin(rStart+rChange),cos(rStart+rChange))

def sign(x):
	return 1.0 if x >= 0.0 else -1.0
