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
               "CE2", In(Bit),
               "REC_BYTE", Out(Array(8, Bit)),
               "RECEIVED", Out(Bit)
                )

TRANSMITTER = DeclareCircuit('transmit',
               "iCE_CLK", In(Bit),
               "RX", In(Bit),
               "transmit_byte", In(Array(8, Bit)),
               "TX", Out(Bit)
                )

