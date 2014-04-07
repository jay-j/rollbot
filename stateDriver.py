#!/usr/bin/env python
from datetime import datetime as clock # interpolation
from time import sleep # for simulation (debugging)
from motorPID import *

######################### GENERAL #########################
class loc:
	def __init__(self, x, y, th):
		self.x = x
		self.y = y
		self.th = th

######################### INTERPOLATOR ######################### 
class smoothStatus:
	def __init__(self):
		self.x = 0.0 # tics
		self.v = 0.0 # tics/sec
		self.t = clock.now()
		self.goal = 0.0
		self.done = False

# calculate time difference, in secondss
def calculateDt(t0):
	delta = clock.now() - t0
	dt = delta.seconds + (1.0e-6)*delta.microseconds
	return dt

def updateSetpoint(setpoint):
	travel = setpoint.goal - setpoint.x # remaining distance (accoring to setpoints)
	dirc = sign(travel)
	travel = fabs(travel)
	dt = calculateDt(setpoint.t) # time since last setpoint was placed

	# profile parameters
	cruise = 10.0 # tics / second
	accTime = 4.0 # time to accelerate to cruise speed
	acc = dirc*cruise / accTime

	# calculate where you'd end up (wrt here) if deceleration starts now
	zeroTime = fabs(setpoint.v/acc)
	travelInc = -0.5*fabs(acc)*(zeroTime)**2 + fabs(setpoint.v)*(zeroTime)

	if travelInc < travel: # accelerate or cruise
		if fabs(setpoint.v) < cruise: # acceleration
			setpoint.x += 0.5*acc*dt**2.0 + setpoint.v*dt
			setpoint.v += acc*dt
		elif fabs(setpoint.v) > cruise:
			setpoint.x += 0.5*acc*dt**2.0 + setpoint.v*dt
			setpoint.v += (-acc*dt)
		else: # cruise
			setpoint.x += dirc*cruise*dt
			setpoint.v = dirc*cruise
	else: # getting close
		if travel > 0.1: # deacceleration or short travel TODO fix
			setpoint.x += (-0.5*acc*(dt**2.0)) + setpoint.v*dt
			setpoint.v += (-acc*dt)
		else: # done; hold position
			setpoint.x = setpoint.x
			setpoint.v = 0
			setpoint.done = True

	setpoint.t = clock.now()
	return setpoint

######################### INTERPOLATOR DEBUGGING ######################### 
def curveTester():
	# init curve
	setpoint = smoothStatus()
	setpoint.x = 0.0 # start
	setpoint.goal = 70.0 # end (goal)
	setpoint.t = clock.now()

	x = [setpoint.x] # histories for debugging
	v = [setpoint.v]
	t = [0]
	tinit = clock.now()
	import random as r

	goalList = [70.0, 0.0, 30.0, 0.0]

	for g in goalList:
		setpoint.goal = g
		setpoint.done = False
		while not setpoint.done:
			sleep(0.05*(r.random() + 0.5))
			#dtx = 0.05*(r.random() + 0.5) # vary the time delay to simulate a real system
			setpoint = updateSetpoint(setpoint)
			x += [setpoint.x]
			v += [setpoint.v]
			t += [calculateDt(tinit)]

	# check endpoint
	print "Ending Position:", x[-1]

	import matplotlib.pyplot as plt
	plt.figure(1)
	plt.plot(t,x)
	plt.xlabel('Time, t (sec)')
	plt.ylabel('Position, x (tic)')
	plt.title('Setpoint Position vs. Time')
	plt.figure(2)
	plt.plot(t,v)
	plt.xlabel('Time, t (sec)')
	plt.ylabel('Velocity, v (tic/sec)')
	plt.title('Setpoint Velocity vs. Time')
	plt.show()

######################### DRIVE SEQUENCE ######################### 
# dictionary for goto states
G = {'STOP':0, 'TURN1_INIT':1, 'TURN1':2, 'DRIVE_INIT':3, 'DRIVE':4, 'TURN2_INIT':5, 'TURN2':6}
w1 = smoothStatus()
w2 = smoothStatus()
driveType = 1

# recieve "goto" command
def goto(goal, gotoState): # goal is loc instance
	global w1
	global w2
	global driveType

	if gotoState == G['STOP']:
		m1.stop()
		m2.stop()

	elif gotoState == G['TURN1_INIT']:
		# calculate drive heading (global)
		driveHeading = atan2(goal.y-robot.y, goal.x-robot.x)
		print "Drive Heading:", driveHeading

		# calculate turn to driveHeading
		turnA = measureAngle(robot.th, driveHeading)

		# decide whether to drive fwd or rev
		if fabs(turnA) > pi/2.0:
			turnA = rotate(turnA,pi)
			driveType = -1 # reverse
		else:
			driveType = +1 # forwards
		print "Turn is", turnA, "to drive", driveType

		# generate motion profile to turn to driveHeading
		wheelTravel = (robot.WIDTH/2.0)*turnA*robot.TICS_PER_INCH # >0 means left turn
		w1.x -= wheelTravel
		w1.done = False
		w2.x += wheelTravel
		w2.done = False
		print "Turning wheel tics to go:", wheelTravel
		gotoState = G['TURN1']

	elif gotoState == G['TURN1']:
		w1 = updateSetpoint(w1) #w1 = left, w2 = right
		w2 = updateSetpoint(w2)
		m1.pid(w1.x, w1.v)
		m2.pid(w2.x, w2.v)
		if w1.done and w2.done:
			gotoState = G['DRIVE_INIT']
	
	elif gotoState == G['DRIVE_INIT']:
		# now calculate translational drive
		driveDist = sqrt((goal.x - robot.x)**2 + (goal.y - robot.y)**2)
		wheelTravel = driveDist*robot.TICS_PER_INCH*driveType
		print "Translational tics to go:", wheelTravel
		w1.x += wheelTravel
		w1.done = False
		w2.x += wheelTravel
		w2.done = False
		gotoState = G['DRIVE']

	elif gotoState == G['DRIVE']:
		w1 = updateSetpoint(w1)
		w2 = updateSetpoint(w2)
		m1.pid(w1.x, w1.v)
		m2.pid(w2.x, w2.v)
		if w1.done and w2.done:
			gotoState = G['TURN2_INIT']

	elif gotoState == G['TURN2_INIT']:
		# now turn to goal heading
		turnB = measureAngle(robot.th, goal.th)
		wheelTravel = (robot.WIDTH/2.0)*turnB*robot.TICS_PER_INCH # >0 means left turn
		print "Final turning wheel tics to go:", wheelTravel
		w1.x -= wheelTravel
		w1.done = False
		w2.x += wheelTravel
		w2.done = False
		gotoState = G['TURN2']

	elif gotoState == G['TURN2']:
		w1 = updateSetpoint(w1)
		w2 = updateSetpoint(w2)
		m1.pid(w1.x, w1.v)
		m2.pid(w2.x, w2.v)
		if w1.done and w2.done:
			print "[STATUS] MOVE COMPLETE."
			gotoState = G['STOP']

	else:
		print '[ERROR] UNRECOGNIZED GOTO STATE \"', gotoState, '\"!'
		gotoState = G['STOP']

	return gotoState

