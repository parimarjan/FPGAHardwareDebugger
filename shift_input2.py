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

counter = Counter(2, ce=True)
wire(counter.CE, receiver.RECEIVED)

dff1 = DFF(ce=True)
dff2 = DFF(ce=True)
dff1(1)
dff2(1)

enable1 = LUT2(~I0&I1)
enable2 = LUT2(I0&~I1)

enable1(counter.O[1], counter.O[0])
enable2(counter.O[1], counter.O[0])

wire(dff1.CE, enable1.O)
wire(dff2.CE, enable2.O)

not1 = Not()
not1(dff1.O)

not2 = Not()
not2(dff2.O)

receiver(main.CLKIN, main.RX, not1.O)

receiver2 = RECEIVER()
receiver2(main.CLKIN, main.RX, not2.O)

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, receiver.REC_BYTE)
wire(echo.TX, main.TX)

wire(main.D1, receiver2.REC_BYTE[0])
wire(main.D2, receiver2.REC_BYTE[3])
wire(main.D3, receiver2.REC_BYTE[5])
wire(main.D4, receiver2.REC_BYTE[7])

compile(sys.argv[1], main)
