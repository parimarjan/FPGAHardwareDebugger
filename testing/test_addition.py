import serial
import time

serial_name = "/dev/tty.usbserial-141B"


# input = bin(0x11)
#input = "00010001"

# input = "01010101"
#input = "\x55"
# input = "\x11"
# input = "\x21"
input = "\x22"

with serial.Serial(serial_name, 9600, timeout=1) as ser:
    
    ser.write(input)
    time.sleep(0.5)
    ser.write(input)
    print(ser.read(1))
    ret = (ser.read(1).encode("hex"))
    print(ret)
    print(bin(int(ret, 16)))

