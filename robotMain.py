#!/usr/bin/env python
# Robot Main

######################### IMPORTS ######################### 
from utils import *
from odometry import *
from stateDriver import *
from path import *
# TODO imaging

######################### SETUP ######################### 
robot = robotLoc(0.0, 0.0, 0.0)

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
prevState = S['STOP']

def robotMain():
	while True:
		# TODO getSensorData() here
		# TODO update odometry

		# TODO print state changes
		if mainState == S['INIT'];
			e1.zero()
			e2.zero()
			pathIndex = 0 # preset the first goal
			mainState = S['PATH']

		elif mainState == S['PATH']:
			# if robot is not at the location specified by its path index, drive. else, photo!
			if not robot == path[pathIndex]:
				goal = path[pathIndex]
				gotoState = G['INIT']
				mainState = S['GOTO']	
			else:
				mainState = S['PHOTO']

		elif mainState == S['GOTO']:
			# move!
			gotoState = goto(goal, gotoState)

			# move complete!
			if gotoState == G['STOP']:
				mainState == S['PATH']

		elif mainState == S['PHOTO']:
			print "[STATUS] TAKE PHOTO!"
			print "         BLANK"
			
			if pathIndex == len(path)-1: # path done!
				mainState = S['XMIT']
			else:
				pathIndex += 1
				mainState = S['PATH']

		elif mainState == S['XMIT']:
			print "[STATUS] TRANSMITTING DATA."
			print "         BLANK"

		elif mainState == S['STOP']:
			print "[STATUS] STOPPED."
			m1.stop()
			m2.stop()

		else:
			print "[ERROR] STATE", mainState, "NOT RECOGNIZED. WILL STOP."
			mainState = S['STOP']

		sleep(.01) # don't overload!
		# end of while loop

	print "[STATUS] REACHED MAIN END"


######################### USAGE ######################### 
# since robotMain() is a function, we can easily comment it
# then control the robot manually via a python terminal
#robotMain()

######################### ROBOT DEV TESTING #########################
## Test 1 ##
# check to see if raw motor commands work, if direction is as expected
# m1.run(6.0)
# m2.run(6.0)

## Test 2 ##
# test encoder raw values...

## Test 3 ##
# motor pid (position control)
# m1.pid(3.,10.)
