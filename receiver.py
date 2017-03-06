import sys
from magma import *
from mantle import *
from rom import ROM
from boards.icestick import IceStick

icestick = IceStick()
icestick.Clock.on()
# icestick.TX.output().on()
icestick.RX.input().on() #initializing rx
icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

main = icestick.main()

SIMPLE_CLOCK = False

# FIXME: How does this correspond to the baud rate / is this exact? What if we
# want another baud rate?
# Also, note for whatever reason CounterModM does not seem to have a reset
# option, or an increment option etc. Is there some way to initialize the
# counterModM only after the first bit is sent? Or start it again from 0? Might
# need to mess with magma's internals for that.
# clock = CounterModM(103, 8, incr=0)

clock = CounterModM(103, 8, ce=True)
baud = clock.COUT

# not gate is used so we invert the input of RX - will be true when RX sends
# its first 0. Then becomes 1 again immediately. Use it to set the enable bit
# of the DFF.
notter = Not()
notter(main.RX)

run = DFF(ce=True)

# This will make run true only when 0 is sent.
# wire(baud, run.CE)

# FIXME: This will keep run true until forever after the first 0. In reality,
# we only want it to be 1 until we read n bits or whatever.
wire(notter.O, run.CE)

run(notter.O)

# clock will start only after run becomes true. So baud rate should be set.
wire(clock.CE, run.O)

shift = SIPO(8, ce=True)

# If both baud and run = True, then read in will be true.
# FIXME: This should be IO&I1 - but baud never seems to be true at the right
# time for now...
read_in = LUT2(I0&I1)

# read_in.O will only be true if both run.O and at correct baud rate
read_in(baud, run.O)

# shift will only be enabled at correct baud rates
wire(read_in.O, shift.CE)

# FIXME: is this a correct way? Will keep reading in serial bits whenever it is
# enabled.
shift(main.RX)

wire(read_in.O, main.D1)
wire(baud, main.D2)
wire(run.O, main.D3)

# FIXME: We should actually not this guy and then connect it to the light so the
# default 1 doesn't turn it on.

# the default value for shift.O[n] is just 0 I guess so it turns on without any
# input?
test_not = Not()
test_not(shift.O[3])
wire(test_not.O, main.D4)

# Turn on the other LED's with shift.

compile(sys.argv[1], main)

