import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

icestick = IceStick()
icestick.Clock.on()

for i in range(8):
    icestick.J1[i].input().on()
# for i in range(8):
    # icestick.J3[i].output().on()

icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()

main = icestick.main()

RECEIVER = DeclareCircuit('receiver',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "TX", Out(Bit),
               "rx_byte", Out(Array(8, Bit))
                )

TRANSMITTER = DeclareCircuit('transmitter',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "o_byte", Out(Array(8, Bit)),
               "TX", Out(Bit)
                )

ECHO = DeclareCircuit('echo',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "transmit_byte", In(Array(8, Bit)),
               "TX", Out(Bit)
                )

receiver = RECEIVER()
receiver(main.CLKIN, main.RX)

echo = ECHO()
echo(main.CLKIN, main.RX, receiver.rx_byte)
wire(echo.TX, main.TX)


# transmitter = TRANSMITTER()
# transmitter(main.CLKIN, receiver.rx_byte)
# transmitter(main.CLKIN, main.RX)
# wire(main.TX, transmitter.TX)
#wire(main.J1, transmitter.o_byte)
# wire(dff1.O, transmitter.o_byte[0])
# wire(dff2.O, transmitter.o_byte[6])

# wire(main.J1[0], 1)
# wire(main.J1[6], 1)

receiver(main.CLKIN, main.RX)

wire(receiver.TX, main.TX)
wire(receiver.rx_byte[0], main.D1)
wire(receiver.rx_byte[1], main.D2)
wire(receiver.rx_byte[2], main.D3)
wire(receiver.rx_byte[3], main.D4)

# Simply wiring all inputs to outputs (Echo-ing)
# wire(main.J1, main.J3)

compile(sys.argv[1], main)
