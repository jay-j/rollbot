import gaugette.rotary_encoder
import pid
import imu
from time import sleep

B2_PIN = "P8_11"  # use wiring pin numbers here
A2_PIN = "P8_12"
B1_PIN = "P9_27"
A1_PIN = "P9_42"
pwm1 = "P9_14" 
pwm2 = "P8_19"
b1 = "P9_13"
f2 = "P8_17"
f1 = "P9_12"
b2 = "P8_18"



encoder1 = gaugette.rotary_encoder.RotaryEncoder.Worker(A1_PIN, B1_PIN)
encoder2 = gaugette.rotary_encoder.RotaryEncoder.Worker(A2_PIN, B2_PIN)
encoder1.start()
encoder2.start()


motor1 = pid.motor(pwm1, f1, b1, encoder1)
motor2 = pid.motor(pwm2, f2, b2, encoder2)


### Simple Go-ing Function ###
def go(m1goal, m2goal):
	motor1.resetPid()
	motor2.resetPid()

	while 1:
		if m1goal != 0:
			m1 = motor1.pid(m1goal,0)
		else:
			m1 = 1
		if m2goal != 0:
			m2 = motor2.pid(m2goal,0)
		else:
			m2 = 1

		if m1 and m2:
			break
		direction = imu.get_direction()	
		print motor1.dist, motor2.dist, direction 
		sleep(0.01)
	motor1.stop()
	motor2.stop()
	sleep(0.5)

### Motion ###
go(5,5)	



encoder1.isDaemon()
encoder2.isDaemon()

