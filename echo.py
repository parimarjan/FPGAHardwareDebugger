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

# FIXME: Have to add these automatically
icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

# wire(sum, main.J3[0:4])
# wire(cout, main.J3[4])
wire(main.J1, main.J3)

compile(sys.argv[1], main)
