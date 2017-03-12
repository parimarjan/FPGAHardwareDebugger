import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()
for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

icestick.D1.on()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

main = icestick.main()


# module top(
	# input iCE_CLK,
	# input RS232_Rx_TTL,
	# output RS232_Tx_TTL,
  # input [7:0] input_byte,
	# );

# uart_integration = DeclareCircuit('top',
               # "CLKIN", In(Bit),
               # "RS232_Rx_TTL", In(Bit),
               # "RS232_Tx_TTL", Out(Bit)
                # )

UART_TEST = DeclareCircuit('test',
                'input_bit', In(Bit))

counter = Counter(5)

uart = UART_TEST()
uart(counter.O)

# Simply wiring all inputs to outputs (Echo-ing)
wire(main.J1, main.J3)

compile(sys.argv[1], main)
