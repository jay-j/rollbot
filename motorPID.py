#!/usr/bin/env pythone
# low-level motor handler

import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

######################### MOTOR FUNCTIONS #########################
class motor:
	def __init__(self, pin_pwm, pin_dir, pin_en, encoder_ref):
		self.pin_pwm = pin_pwm
		self.pin_dir = pin_dir
		self.pin_en = pin_en

		# startup pwm, stop
		GPIO.setup(self.pin_dir, GPIO.OUT)
		GPIO.setup(self.pin_en, GPIO.OUT)
		self.stop()
		PWM.start(self.pin_pwm, 0.0)

		# motor/pid params
		self.kv = 0.1 # TODO
		self.kp = 0.1 # TODO
		self.ki = 0.0 # TODO
		self.kd = 0.0 # TODO
		self.integralReset()

		# save encoder class link
		self.e = encoder_ref

	def stop():
		# set enable pin low
		GPIO.output(self.pin_en, GPIO.LOW)

	def setPWMFrequency(freq):
		PWM.set_frequency(pin_pwm,freq)

	def pid(xgoal, vgoal):
		# feed-forwards term
		ff = self.kv * vgoal

		# pid calcs
		error = self.e.x - xgoal
		derror = -sign(error)*e.v
		self.ierror += error

		pid_total = self.kp*error + self.ki*self.ierror + self.kd*derror + ff
	
		# stop motors if close to goal
		if fabs(error) > 5:
			self.run(pid_total)
		else:
			self.run(0)

	def run(volts):
		if volts != 0.0:
			# volts is signed, -9 to 9
			GPIO.output(self.pin_en, GPIO.HIGH)
			if volts > 0:
				GPIO.output(self.pin_dir, GPIO.HIGH)
			else:
				GPIO.output(self.pin_dir, GPIO.LOW)
		
			# rescale volts
			volts = fabs(volts)*100./9.
			PWM.set_duty_cycle(self.pin_pwm, volts)
		else:
			self.stop()

	def integralReset():
		self.ierror = 0


