import sys
from magma import *
from mantle import *
from boards.icestick import IceStick

from uart import *
import math

icestick = IceStick()
icestick.Clock.on()

icestick.D1.on()
icestick.D2.on()
icestick.D3.on()
icestick.D4.on()

# Must add these 3 for the debugger to work
icestick.RX.input().on()
icestick.TX.output().on()

main = icestick.main()

n = 2
receivers = []
dffs = []
enables = []
nots = []

for i in range(n):
    receivers.append(RECEIVER())
    dffs.append(DFF(ce=True))
    dffs[i](1)
    nots.append(Not())
    nots[i](dffs[i].O)

    receivers[i](main.CLKIN, main.RX, nots[i].O)

# receiver = RECEIVER()
# counter = Counter(2, ce=True)

counter_n = int(math.ceil(math.log(n, 2)))
print('counter n was ', counter_n)
counter = Counter(counter_n+1, ce=True)
decoder = Decoder(counter_n+1)
decoder(counter.O)
wire(counter.CE, receivers[0].RECEIVED)

for i in range(n): 
    wire(dffs[i].CE, decoder.O[i+1])

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, receivers[1].REC_BYTE)
wire(echo.TX, main.TX)

compile(sys.argv[1], main)

