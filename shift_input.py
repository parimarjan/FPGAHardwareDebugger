import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

from uart import *

icestick = IceStick()
icestick.Clock.on()

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

counter = Counter(3, ce=True)

dff_dummy = DFF(ce=True)
dff_dummy(1)
and_dummy = LUT2(I0&~I1)
and_dummy(dff_dummy.O, counter.COUT)
wire(dff_dummy.CE, receiver.RECEIVED)

counter_enable = LUT2(I0|I1)
counter_enable(and_dummy.O, receiver.RECEIVED)

# wire(counter.RESET, counter_disable.O)

piso = PISO(8, ce=True)
sipo = SIPO(32, ce=True)
sipo(piso.O)

receiver(main.CLKIN, main.RX)

piso(1, receiver.REC_BYTE, 1)
wire(piso.CE, counter_enable.O)
wire(sipo.CE, counter_enable.O)

# wire(main.D1, piso.O)
wire(main.D1, counter_enable.O)
# wire(main.D2, fuck_this.O)
# wire(main.D3, receiver.RECEIVED)
wire(main.D3, sipo.O[12])
wire(main.D4, sipo.O[23])

wire(counter.CE, counter_enable.O)

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, sipo.O[16:24])
wire(echo.TX, main.TX)

compile(sys.argv[1], main)
