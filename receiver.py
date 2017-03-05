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
if not SIMPLE_CLOCK:
    clock = CounterModM(103, 8)
    baud = clock.COUT

# Can we approximate behaviour of CounterModM with a simple counter?
if SIMPLE_CLOCK:
    clock = Counter(7, ce=True)
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

# CounterModM doesn't have any of the following ugh.
# wire(clock.CE, run.O)
# clock(CE=run.O)
# wire(clock.incr, run.CE)

if SIMPLE_CLOCK:
    wire(clock.CE, run.O)

# FIXME: reset our clock after getting the first 1 so its in sync with the baud
# rate.

siso = SIPO(8, ce=True)

# If both baud and run = True, then read in will be true.
# FIXME: This should be IO&I1 - but baud never seems to be true at the right
# time for now...
read_in = LUT2(I0&I1)
# print(read_in.interface)
read_in(baud, run.O)

wire(read_in.O, main.D1)
wire(read_in.O, siso.CE)
wire(baud, main.D2)
siso(main.RX)

# turn on light if run is true. Should stay on in this case.
wire(run.O, main.D3)
# Turn on the other LED's with siso.
# wire(siso.O[1], main.D1)
# wire(siso.O[2], main.D2)
wire(siso.O[3], main.D4)

compile(sys.argv[1], main)

