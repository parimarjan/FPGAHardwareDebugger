import sys
from magma import *
from mantle import *
from rom import ROM
from boards.icestick import IceStick

icestick = IceStick()
icestick.Clock.on()
icestick.TX.output().on()
icestick.RX.input().on() #initializing rx
icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

main = icestick.main()

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

count_bits = Counter(3, ce=True)
not_over = Not()
not_over(count_bits.COUT)

# FIXME: This will keep run true until forever after the first 0. In reality,
# we only want it to be 1 until we read n bits or whatever.
wire(notter.O, run.CE)
run(notter.O)

# clock will start only after run becomes true. So baud rate should be set.
wire(clock.CE, run.O)

shift = SIPO(8, ce=True)
print("after sipo")
# If both baud and run = True, then read in will be true.
# FIXME: This should be IO&I1 - but baud never seems to be true at the right
# time for now...
read_in = LUT2(I0&I1)

# read_in.O will only be true if both run.O and at correct baud rate

run_and_not_over = LUT2(I0&I1)
# run_and_not_over = And(2)

run_and_not_over(run.O, not_over.O)
read_in(baud, run_and_not_over.O)

# shift will only be enabled at correct baud rates
wire(read_in.O, shift.CE)

# FIXME: is this a correct way? Will keep reading in serial bits whenever it is
# enabled.
shift(main.RX)

wire(read_in.O, main.D1)
wire(baud, main.D2)
wire(run_and_not_over.O, main.D3)

# This should incr counter only when baud rate is on.
wire(read_in.O, count_bits.CE)

# FIXME: We should actually not this guy and then connect it to the light so the
# default 1 doesn't turn it on.

# the default value for shift.O[n] is just 0 I guess so it turns on without any
# input?
test_not = Not()
test_not(shift.O[3])
wire(test_not.O, main.D4)

# Turn on the other LED's with shift.
valid = 1

printf = Counter(4, ce=True)
data = array(shift.O[0], shift.O[1], shift.O[2], shift.O[3], shift.O[4],
        shift.O[5], shift.O[6], shift.O[7], 0 )

clock2 = CounterModM(103, 8)

baud2 = clock.COUT

count2 = Counter(4, ce=True, r=True)
done2 = Decode(15, 4)(count2)

run2 = DFF(ce=True)
run_n = LUT3([0,0,1,0, 1,0,1,0])
run_n(done2, valid, run2)
run2(run_n)
wire(baud2, run2.CE)

reset = LUT2(I0&~I1)(done2, run2)
count2(CE=baud2, RESET=reset)

shift2 = PISO(9, ce=True)

# load data when we are not running...
load = LUT2(I0&~I1)(valid,run2)
shift2(1,data,load)
wire(baud2, shift2.CE)

ready2 = LUT2(~I0 & I1)(run2, baud2)
wire(ready2, printf.CE)

#ander = LUT2(I0&I1)

wire(shift2, main.TX)
#wire(0,shift.O)
# wire(main.D1, shift.O)

compile(sys.argv[1], main)

