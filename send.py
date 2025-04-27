import serial
ser = serial.Serial('/dev/cu.usbserial-0001')
print(ser.name)
ser.write(b'10,10')
ser.close()