import sys
from magma import *
from mantle import *
from rom import ROM
from boards.icestick import IceStick

icestick = IceStick()
icestick.Clock.on()
icestick.TX.output().on()
icestick.RX.input().on() #initializing rx
icestick.D1.on()
icestick.D3.on()

main = icestick.main()



valid = 1

init = [array(*int2seq(ord(c), 8)) for c in 'Hello, WOrld  \r\n']
#print init
#init = [1,1,1,1,1,1,1,1]
printf = Counter(4, ce=True)
rom = ROM(4, init, printf.O)

notter = Not()
notter(main.RX)

dff = DFF(ce=True)
dff(1)
wire(notter, dff.CE)

wire(dff.O, main.D3)
#data = array(rom.O[7], rom.O[6], rom.O[5], rom.O[4],
           #  dff.O, rom.O[2], rom.O[1], rom.O[0], 0 )

data = array(main.RX, main.RX, main.RX, main.RX, main.RX, main.RX, main.RX, main.RX, 0 )

clock = CounterModM(103, 8)
baud = clock.COUT

count = Counter(4, ce=True, r=True)
done = Decode(15, 4)(count)

run = DFF(ce=True)
run_n = LUT3([0,0,1,0, 1,0,1,0])
run_n(done, valid, run)
run(run_n)
wire(baud, run.CE)

reset = LUT2(I0&~I1)(done, run)
count(CE=baud, RESET=reset)

shift = PISO(9, ce=True)
load = LUT2(I0&~I1)(valid,run)
shift(1,data,load)
wire(baud, shift.CE)

ready = LUT2(~I0 & I1)(run, baud)
wire(ready, printf.CE)

#ander = LUT2(I0&I1)

wire(shift, main.TX)
#wire(0,main.RX)
wire(main.D1, main.RX)


compile(sys.argv[1], main)

