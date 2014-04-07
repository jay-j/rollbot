#!/usr/bin/env python
# Robot Main

######################### IMPORTS ######################### 
from utils import *
from odometry import *
from stateDriver import *
from path import *
# TODO compass?
# TODO imaging

######################### SETUP ######################### 
# motor setup
e1 = encoder()
e2 = encoder()
m1 = motor("P8_1", "P8_2", "P8_3", e1)
m2 = motor("P8_4", "P8_5", "P8_6", e2)


######################### TMP SETUP ######################### 
gotoState = G['TURN1_INIT']
goal = loc(1,1,-1)
print "Driving FROM", [robot.x, robot.y, robot.th], "TO", [goal.x, goal.y, goal.th]

######################### ROBOT MAIN ######################### 
S = {'INIT':0, 'PATH':1, 'GOTO':2, 'PHOTO':3, 'XMIT':4, 'STOP':5}
mainState = S['INIT']

def robotMain():
	while True:
		# TODO getSensorData()

		if mainState == S['INIT'];
			

		elif mainState == S['PATH']:
			# set goal = (x,y)
			# set gotoState = G['INIT']
			mainState = S['GOTO']

			# store which path index we're going to
			# grab the next index off the list for sending to goto
			# goal = path[i]

		elif mainState == S['GOTO']
			# move!
			gotoState = goto(goal, gotoState)

			# move complete!
			if gotoState == G['STOP']:
				mainState == S['PATH']

		elif mainState == 

		sleep(.05)


	print "[STATUS] REACHED MAIN END"


######################### USAGE ######################### 
#robotMain()

m1.run(6.0)
