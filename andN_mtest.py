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

test = MTest(main, n=2, num_outputs=1)

and8 = AndN(8)
output = and8(test.receivers[0], test.receivers[1])

test.set_output_byte(output)

# wire(main.D1, 1)

test.end_circuit()
test.test_input_file('./testing/test_and8.txt')

# Testing phase!

