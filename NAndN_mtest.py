import sys
from magma import *
from mantle import AndN
from boards.icestick import IceStick
import math

from MTest.mtest import *

icestick = IceStick()
# icestick.D1.on()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

main = icestick.main()

test = MTest(main, num_inputs=1, num_outputs=1)

nand3 = NAnd3()
output = nand3(test.receivers[0][0], test.receivers[0][1], test.receivers[0][2])

test.set_output_byte(output)

# wire(main.D1, 1)

test.end_circuit()
test.test_input_file('./testing/test_nand3.txt')

# Testing phase!

