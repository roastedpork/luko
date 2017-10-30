#!/usr/bin/env python
import serial
import sys,time
import random

hex='0123456789abcdef'

def readInput(str):
	try:
		strip = "".join([c for c in str if c in hex])	
		res = [int(strip[2*i:2*i+2],16) for i in range(5)]
	except:
 		res=[]
	return res
	



if __name__=="__main__":
	port = sys.argv[1]
	rate = int(sys.argv[2])
	print "Trying to connect to port %s @ %dHz" %(port,rate)
		
	
	ser=serial.Serial(
		port=port,
		baudrate=rate,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)

	print "Status: " + str(ser.isOpen())


	for i in range(20):
		readout = ser.readline()
		print readout
		print readInput(readout)
		time.sleep(0.01)

	target = [format(random.randint(0,180),"02x") for i in range(5)]	
	msg = '<' +  "".join(target) + '>'
	print "sending '%s'" %(msg)

	ser.write(msg)
	for i in range(20):
		readout = ser.readline()
		print readout
		print readInput(readout)
		time.sleep(0.01)
	
	target = [format(random.randint(0,180),"02x") for i in range(5)]
	msg = '<' + "".join(target) + '>'
	print "sending '%s'" %(msg)
	ser.write(msg)

	for i in range(20):
		readout = ser.readline()
		print readout
		print readInput(readout)
		time.sleep(0.01)
