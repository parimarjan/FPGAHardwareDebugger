import serial
import time

serial_name = "/dev/tty.usbserial-141B"

string = "hello, world"

for i in string:

    with serial.Serial(serial_name, 9600, timeout=0.1) as ser:
        
        ser.write(i)
        ser.read(1) #ignore the read bit
        time.sleep(0.5)
        ser.write(i)
        print(ser.read(1))

