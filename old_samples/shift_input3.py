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

main = icestick.main()

n = 2
receivers = []
counter_n = int(math.ceil(math.log(n, 2)))
counter = Counter(counter_n+1, ce=True)

decoder = Decoder(counter_n+1)
decoder(counter.O)

for i in range(n):
    receivers.append(RECEIVER())
    receivers[i](main.CLKIN, main.RX, decoder.O[i])
    
wire(counter.CE, receivers[0].RECEIVED)

echo = TRANSMITTER()
echo(main.CLKIN, main.RX, receivers[i].REC_BYTE)
wire(echo.TX, main.TX)
