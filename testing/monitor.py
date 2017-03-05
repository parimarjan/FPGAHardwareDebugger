import serial
import time

serial_name = "/dev/tty.usbserial-141B"
with serial.Serial(serial_name, 28800, timeout=1) as ser:
    # print(ser.read(100))
    # for char in b"Hello World":
    #     ser.write([char])
    for i in range(10):
        msg = b"Hello World"
        ser.write(msg)
        time.sleep(.1)
        print(ser.read(5))
        # print(ser.read(len(msg)))
