import sys
from magma import *
from mantle import AndN
from boards.icestick import IceStick
import math

from MTest.mtest import *

icestick = IceStick()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

main = icestick.main()

test = MTest(main, 'andN_mtest.py', n=2, num_outputs=1)

and8 = AndN(8)
output = and8(test.receivers[0], test.receivers[1])

test.set_output_byte(output)

compile(sys.argv[1], main)
