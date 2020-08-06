'''
This is a simple program to test serial communication between PC and Arduino

Written and developed by: Chen Lequn. chen1189@e.ntu.edu.sg

'''

import serial
import serial.tools.list_ports, warnings

#port detection - start
ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    # if 'USB' in p.description
]

print (ports)


if len(ports) > 1:
    warnings.warn('Connected ...')

ser = serial.Serial(ports[0],9600) # to connect the first ports

while 1:
    val = input("Enter 0 or 1 to control the LED:")

    ser.write(val.encode())