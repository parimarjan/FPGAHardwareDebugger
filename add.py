import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *

icestick = IceStick()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

icestick.D1.on()
icestick.D2.on()

main = icestick.main()

def Add(A, B):
    n = len(A)
    # create a full adder for every bit to be added
    add = [FullAdder() for i in range(n)]

    CIN = 0
    O = []
    for i in range(n):
        wire(A[i], add[i].I0)
        wire(B[i], add[i].I1)
        wire(CIN, add[i].CIN)
        CIN = add[i].COUT
        O.append(add[i].O)
    return array(*O), CIN


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

wire(counter.CE, counter_enable.O)

sum, cout = Add(sipo.O[8:16],sipo.O[0:8])

# test_array = concat(sum, sum)

wire(sipo.O[0], main.D1)
wire(sipo.O[1], main.D2)

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, sum)
wire(echo.TX, main.TX)

compile(sys.argv[1], main)
