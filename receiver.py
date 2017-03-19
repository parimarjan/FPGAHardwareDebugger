import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

from uart import *

icestick = IceStick()
icestick.Clock.on()

for i in range(8):
    icestick.J1[i].input().on()
# for i in range(8):
    # icestick.J3[i].output().on()

icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()

main = icestick.main()

receiver = RECEIVER()
receiver(main.CLKIN, main.RX)

echo = ECHO()
echo(main.CLKIN, main.RX, receiver.REC_BYTE)
wire(echo.TX, main.TX)

receiver(main.CLKIN, main.RX)
# wire(receiver.TX, main.TX)
wire(receiver.REC_BYTE[0], main.D1)
wire(receiver.REC_BYTE[1], main.D2)
wire(receiver.REC_BYTE[2], main.D3)
wire(receiver.REC_BYTE[3], main.D4)

# Simply wiring all inputs to outputs (Echo-ing)
# wire(main.J1, main.J3)
compile(sys.argv[1], main)
