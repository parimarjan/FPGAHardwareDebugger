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

sum, cout = Add(main.J1[0:4], main.J1[4:8])

#wire the bits to the output
wire(sum, main.J3[0:4])
wire(cout, main.J3[4])

#adding 0 to the outputs not used - will automate this

dff = DFF()
dff(0)
wire(dff.O, main.J3[5])
wire(dff.O, main.J3[6])
wire(dff.O, main.J3[7])

compile(sys.argv[1], main)
