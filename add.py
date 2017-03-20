import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *
import math

icestick = IceStick()

icestick.RX.input().on()
icestick.TX.output().on()
icestick.Clock.on()

icestick.D1.on()
icestick.D2.on()

main = icestick.main()

def Add(A, B):
    n = len(A)
    # create a full adder for every bit to be added
    add = [FullAdder() for i in range(n)]

    CIN = 0
    O = []
    for i in range(n):
        wire(A[i], add[i].I0)
        wire(B[i], add[i].I1)
        wire(CIN, add[i].CIN)
        CIN = add[i].COUT
        O.append(add[i].O)
    return array(*O), CIN

n = 2
receivers = []
# dffs = []
# enables = []
# nots = []

# freeze_byte = RECEIVER()
# freeze_dff = DFF(ce=True, r=True)
# freeze_dff(1)

# reset_bit = freeze_byte.REC_BYTE[0]
# reset_bit = Not()
# reset_bit(freeze_byte.REC_BYTE[0])

counter_n = int(math.ceil(math.log(n, 2)))
print('counter n was ', counter_n)
counter = Counter(counter_n+1, ce=True)
# wire(counter.RESET, reset_bit)

decoder = Decoder(counter_n+1)
decoder(counter.O)

for i in range(n):
    receivers.append(RECEIVER())
    # dffs.append(DFF(ce=True, r=True))
    # dffs[i](1)
    # nots.append(Not())
    # nots[i](dffs[i].O)

    # receivers[i](main.CLKIN, main.RX, nots[i].O)
    receivers[i](main.CLKIN, main.RX, decoder.O[i])
    
    # wire(dffs[i].RESET, reset_bit)

# freeze_byte(main.CLKIN, main.RX, dffs[-1].O)

wire(counter.CE, receivers[0].RECEIVED)

# for i in range(n): 
    # wire(dffs[i].CE, decoder.O[i+1])
    # wire(

sum, cout = Add(receivers[0].REC_BYTE, receivers[1].REC_BYTE)

# test_array = concat(sum, sum)

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, sum)
wire(echo.TX, main.TX)

compile(sys.argv[1], main)
