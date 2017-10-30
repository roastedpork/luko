#!/usr/bin/env python

import serial
import random



if __name__ == "__main__":

	ser = serial.Serial(
		port='dev'ttyAMA0',
		naudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)
	
	



	
