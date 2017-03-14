import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()
icestick.Clock.on()

for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

icestick.D1.on()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()

main = icestick.main()


# module top(
	# input iCE_CLK,
	# input RS232_Rx_TTL,
	# output RS232_Tx_TTL,
  # input [7:0] input_byte,
	# );

RECEIVER = DeclareCircuit('receiver',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "TX", Out(Bit)
                )

receiver = RECEIVER()

receiver(main.CLKIN, main.RX)
wire(receiver.TX, main.TX)

# Simply wiring all inputs to outputs (Echo-ing)
# wire(main.J1, main.J3)

compile(sys.argv[1], main)
