import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()

icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

main = icestick.main()

# Can't really read back if its 20 bits yet, but lets say we just read back the
# COUT bit.
test_counter = Counter(5, ce=True)

RECEIVER = DeclareCircuit('receiver',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "TX", Out(Bit),
               "rx_byte", Out(Array(8, Bit))
                )

receiver = RECEIVER()
receiver(main.CLKIN, main.RX)

wire(test_counter.COUT, main.D4)
wire(test_counter.CE, receiver.rx_byte[0])

# wire(test_counter.CE, main.J1[0])
# wire(test_counter.O[4], main.D1)
# wire(test_counter.COUT, main.D2)


compile(sys.argv[1], main)
