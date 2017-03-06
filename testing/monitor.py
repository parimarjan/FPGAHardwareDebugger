import serial
import time

serial_name = "/dev/tty.usbserial-141B"
with serial.Serial(serial_name, 9600, timeout=1) as ser:
    # print(ser.read(100))
    for char in b"Hello World":
        ser.write([char])
        print(ser.read(1))

    # for i in range(10):
        # msg = "hello, world"
        # ser.write(msg)
        # # time.sleep(.1)
        # print(ser.read(len(msg)))
