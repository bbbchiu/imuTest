import smbus
import time
import math
import socket
import numpy as np

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg,address):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h << 8) + l
	return value

def read_word_2c(reg,addr):
	val = read_word(reg,addr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def read_gyro_x(addr):
	xout = read_word_2c(0x43,addr)
	yout = read_word_2c(0x45,addr)
	zout = read_word_2c(0x47,addr)
	return xout

def read_gyro_y(addr):
    xout = read_word_2c(0x43,addr)
    yout = read_word_2c(0x45,addr)
    zout = read_word_2c(0x47,addr)
    return yout

def read_gyro_z(addr):
    xout = read_word_2c(0x43,addr)
    yout = read_word_2c(0x45,addr)
    zout = read_word_2c(0x47,addr)
    return zout

def read_bes_x(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_x_ska = bes_x / 16384.0 * 9.8
	return bes_x_ska

def read_bes_y(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_y_ska = bes_y / 16384.0 * 9.8
	return bes_y_ska

def read_bes_z(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_z_ska = bes_z / 16384.0 * 9.8
	return bes_z_ska

def read_mag_x(addr):
	mag_x = read_word_2c(0x04,addr)
	mag_y = read_word_2c(0x06,addr)
	mag_z = read_word_2c(0x08,addr)

	mag_x_out = mag_x
	return mag_x_out

def read_mag_y(addr):
    mag_x = read_word_2c(0x04,addr)
    mag_y = read_word_2c(0x06,addr)
    mag_z = read_word_2c(0x08,addr)

    mag_y_out = mag_y
    return mag_y_out

def read_mag_z(addr):
    mag_x = read_word_2c(0x04,addr)
    mag_y = read_word_2c(0x06,addr)
    mag_z = read_word_2c(0x08,addr)

    mag_z_out = mag_z
    return mag_z_out


bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, 0x37,0x02)
mag_address = 0x0c
bus.write_byte_data(mag_address,0x0A, 0b0110)
start_t = 0
end_t = 0

while True:
	start_t = time.time()
	bes_x = read_bes_x(address)
	bes_y = read_bes_y(address)
	bes_z = read_bes_z(address)
	mag_x = read_mag_x(mag_address)
	mag_y = read_mag_y(mag_address)
	mag_z = read_mag_z(mag_address)

	if bes_x!=0 and bes_y!=0:
		pitch = 180.0 * math.atan2(bes_x,math.sqrt(bes_y*bes_y+bes_z*bes_z))/math.pi
		roll = 180.0 * math.atan2(bes_y,math.sqrt(bes_x*bes_x+bes_z*bes_z))/math.pi
		mag_x_out = mag_x*math.cos(pitch)+mag_y*math.sin(roll)*math.sin(pitch)+mag_z*math.cos(roll)*math.sin(pitch)
		mag_y_out = mag_y*math.cos(roll) - mag_z*math.sin(roll)
		if mag_y_out != 0:
			yaw = 180.0*math.atan2(-mag_y_out,mag_x_out)/math.pi
		else:
			yaw = 0
#		print("before bes_x: "+str(bes_x))
		print("x: "+str(roll)) #roll = x
		print("y: "+str(pitch))  #pitch = y
		print("z: "+str(yaw)) #yaw = z
#		print(math.sin(pitch*math.pi/180))
#		print("after bes_x: "+str(bes_x*math.cos(roll*math.pi/180)*-math.sin(pitch*math.pi/180)))
#		print("loss: ",str())
		print("")
	end_t = time.time()
	time_inter = end_t - start_t
#	print("time_inter: "+str(time_inter))
