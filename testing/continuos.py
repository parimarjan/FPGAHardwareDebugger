import serial
import time

serial_name = "/dev/tty.usbserial-141B"
ser = serial.Serial(serial_name, "115200")
print(ser.name)

ser.close()
ser.open()
try:
    while True:
        ser.write(bin(1))

except KeyboardInterrupt:
    ser.close()
    print("finishing the serial run")

