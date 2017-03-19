# import sys
from magma import *
from mantle import *
# from boards.icestick import IceStick

# Must add these 3 for the debugger to work
# icestick.RX.input().on()
# icestick.TX.output().on()

# main = icestick.main()

RECEIVER = DeclareCircuit('receiver',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               # "TX", Out(Bit),
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

