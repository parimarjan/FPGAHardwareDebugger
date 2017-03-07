import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()
for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

main = icestick.main()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

# Simply wiring all inputs to outputs (Echo-ing)
wire(main.J1, main.J3)

compile(sys.argv[1], main)
