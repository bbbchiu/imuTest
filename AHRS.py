import math
import numpy as np

q0 = 1.0
q1 = 0.0
q2 = 0.0
q3 = 0.0

def ahrs(gx,gy,gz,ax,ay,az):
	global q0
	global q1
	global q2
	global q3

	recipNorm = 0
	q0q0 = q0*q0
	q0q1 = q0*q1
	q0q2 = q0*q2
	q0q3 = q0*q3
	q1q1 = q1*q1
	q1q2 = q1*q2
	q1q3 = q1*q3
	q2q2 = q2*q2
	q2q3 = q2*q3
	q3q3 = q3*q3

	halfvx = 0.0
	halfvy = 0.0
	halfvz = 0.0
	
	halfex = 0.0
	halfey = 0.0
	halfez = 0.0

	qa = 0.0
	qb = 0.0
	qc = 0.0

	if(not(ax == 0.0 and ay == 0.0 and az ==0.0)):
		recipNorm = 1/math.sqrt(ax*ax + ay*ay+az*az)
		ax = ax * recipNorm
		ay = ay * recipNorm
		az = az * recipNorm

		halfvz = q1*q3-q0*q2
		halfvy = q0*q1 + q2*q3
		halfvz = q0 *q0 -1/2+q3*q3

		halfex = (ay*halfvz-az*halfvy)
		halfey = (az*halfvx - az*halfvz)
		halfez = (az*halfvy - ay*halfvz)

#		if(twoKi > 0.0):
#			pass
#		else:
		integralFBx = 0.0
		integralFBy = 0.0
		integralFBz = 0.0


