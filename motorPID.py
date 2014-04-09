#!/usr/bin/env pythone
# low-level motor handler

import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import math
######################### MOTOR FUNCTIONS #########################
class motor:
	def __init__(self, pin_pwm, pin_for, pin_back, encoder_ref):
		self.pin_pwm = pin_pwm
		self.pin_for = pin_for
		self.pin_back = pin_back

		# startup pwm, stop
		GPIO.setup(self.pin_for, GPIO.OUT)
		GPIO.setup(self.pin_back, GPIO.OUT)
		#self.stop()
		PWM.start(self.pin_pwm, 0.0)

		# motor/pid params
		self.kv = 0.1 # TODO
		self.kp = 10.0 # TODO
		self.ki = 0.0 # TODO
		self.kd = 0.0 # TODO

		# save encoder class link
		self.e = encoder_ref
		self.dist = 0;
		self.ierror = 0
	def stop(self):
		PWM.set_duty_cycle(self.pin_pwm, 0)
		# set enable pin low
		#GPIO.output(self.pin_en, GPIO.LOW)

	def setPWMFrequency(self,freq):
		PWM.set_frequency(pin_pwm,freq)

	def resetPid(self):
		self.dist = 0
		self.integralReset()

	def pid(self,xgoal, vgoal):
		# feed-forwards term
		ff = self.kv * vgoal
		self.dist += self.e.get_delta() * .0203
			
		# pid calcs
		error = xgoal-self.dist
		derror = 0#-sign(error)*e.v
		self.ierror += error

		pid_total = self.kp*error + self.ki*self.ierror + self.kd*derror + ff

		if pid_total > 9:
			pid_total = 9
		elif pid_total < -9:
			pid_total = -9
		
		# stop motors if close to goal
		if math.fabs(error) > 0.25:
			self.run(pid_total)
			return 0
		else:
			self.run(0)
			return 1
		

	def run(self,volts):
		if volts != 0.0:
			# volts is signed, -9 to 9
			#GPIO.output(self.pin_en, GPIO.HIGH)
			if volts > 0:
				GPIO.output(self.pin_back, GPIO.HIGH)
				GPIO.output(self.pin_for, GPIO.LOW)
			else:
				GPIO.output(self.pin_back, GPIO.LOW)
				GPIO.output(self.pin_for, GPIO.HIGH)

			# rescale volts
			volts = math.fabs(volts)*100./9.
			if (volts > 100):
				volts = 100
			PWM.set_duty_cycle(self.pin_pwm, volts)
		else:
			self.stop()

	def integralReset(self):
		self.ierror = 0


