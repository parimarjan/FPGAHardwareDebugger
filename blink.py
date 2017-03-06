import sys
from magma import *
from mantle import *
from boards.icestick import IceStick


icestick = IceStick()

icestick.Clock.on()
icestick.D1.on()
# enable RX, TX
icestick.RX.input().on()
icestick.TX.output().on()

for i in range(8):
    icestick.J3[i].output().on()

main = icestick.main()

c = Counter(25)

wire(c.O[24], main.D1)
wire(c.O[16:24], main.J3)

compile(sys.argv[1], main)
