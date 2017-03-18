import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()

icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

main = icestick.main()

# FIXME: Have to add these automatically
icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

# Can't really read back if its 20 bits yet, but lets say we just read back the
# COUT bit.
test_counter = Counter(20, ce=True)

# sum, cout = Add(main.J1[0:4], main.J1[4:8])

# For whatever reason - need to wire everything to something.
# FIXME: Should we be reading 0 or 7th bit?
wire(test_counter.COUT, main.J3[0])
wire(test_counter.CE, main.J1[0])
wire(test_counter.O[4], main.D1)
wire(test_counter.COUT, main.D2)

# dff_input = DFF()
# dff_input(0)
# for i in range(1,8):
    # wire(dff_input.O, main.J1[i])

dff_output = DFF()
dff_output(0)

for i in range(1,8):
    wire(dff_output.O, main.J3[i])

# wire(dff.O, main.J3[6])
# wire(dff.O, main.J3[7])

compile(sys.argv[1], main)
