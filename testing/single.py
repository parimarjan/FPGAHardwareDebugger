import serial
import time

serial_name = "/dev/tty.usbserial-141B"
ser = serial.Serial(serial_name, "115200")
print(ser.name)

ser.close()
ser.open()

# FIXME: Why does this work with bin(1) as well
reps = 1
for i in range(reps):
    ser.write(bin(0))

ser.close()
