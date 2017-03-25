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

def Subtract(A, B):
    n = len(A)
    # create a full adder for every bit to be subtracted
    add = [FullAdder() for i in range(n)]

    CIN = 1 #CIN for subtractor is 1
    O = []
    for i in range(n):
        b_not = Not() #invert the bit of the second number
        b_not(B[i])

        wire(A[i], add[i].I0)
        wire(b_not, add[i].I1)
        wire(CIN, add[i].CIN)
        CIN = add[i].COUT
        O.append(add[i].O)
    return array(*O), CIN

test = MTest(main, num_inputs=2, num_outputs=1)

sum, cout = Subtract(test.receivers[0], test.receivers[1])
test.set_output_byte(sum)

test.end_circuit()

# Testing phase:
test.test_input_file('testing/test_sub.txt')

