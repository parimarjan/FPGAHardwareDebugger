import sys
from magma import *
from mantle import Mux2
from boards.icestick import IceStick
import math

from MTest.mtest import *

icestick = IceStick()
icestick.D1.on()
icestick.D2.on()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

main = icestick.main()

test = MTest(main, num_inputs=2, num_outputs=1)

mux2 = Mux2()

# Takes 2 bits as input, and selector is the 0th bit.
output = mux2(test.receivers[0][0:2], test.receivers[1][0])
test.set_output_byte(output)

wire(main.D1, 1)

# Testing phase!

test.end_circuit()
test.test_input_file('./testing/test_mux2.txt')

