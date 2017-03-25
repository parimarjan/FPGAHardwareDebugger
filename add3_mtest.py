import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
import math

from MTest.mtest import *
# from Mtest.uart import *

icestick = IceStick()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

icestick.D5.on()

main = icestick.main()

def Add(A, B, CIN):
    n = len(A)
    # create a full adder for every bit to be added
    add = [FullAdder() for i in range(n)]

    #CIN = 0
    O = []
    for i in range(n):
        wire(A[i], add[i].I0)
        wire(B[i], add[i].I1)
        wire(CIN, add[i].CIN)
        CIN = add[i].COUT
        O.append(add[i].O)
    return array(*O), CIN

test = MTest(main, num_inputs=3, num_outputs=1)

sum_temp, cout_temp = Add(test.receivers[0], test.receivers[1], 0)

sum, cout = Add(sum_temp, test.receivers[2], cout_temp)


test.set_output_byte(sum)

test.end_circuit()

test.test_input_file('testing/test_add3.txt')

# Testing phase:

# No need for compile call here - since this file itself won't be compiled.
# compile(sys.argv[1], main)
