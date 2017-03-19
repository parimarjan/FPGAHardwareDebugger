import serial
import time

serial_name = "/dev/tty.usbserial-141B"

input = "\x11" #first number will be the first 4 bits, second will be the second 4 bits

with serial.Serial(serial_name, 9600, timeout=1) as ser:
    
    ser.write(input)
    ser.read(1) #ignore the read bit
    time.sleep(0.5) #read the circuit after 0.5 seconds
    ser.write(input)
    ret = (ser.read(1).encode("hex"))
    print("Hex: " + ret)
    print("Bin: " + bin(int(ret, 16)))

