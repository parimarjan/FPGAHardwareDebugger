import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
from rom import ROM

icestick = IceStick()
icestick.Clock.on()

# for i in range(8):
    # icestick.J1[i].input().on()
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

receiver = RECEIVER()

receiver(main.CLKIN, main.RX)

wire(receiver.TX, main.TX)

wire(receiver.rx_byte[0], main.D1)
wire(receiver.rx_byte[1], main.D2)
wire(receiver.rx_byte[2], main.D3)
wire(receiver.rx_byte[3], main.D4)

valid = 1

init = [array(*int2seq(ord(c), 8)) for c in 'hello, World  \r\n']

printf = Counter(4, ce=True)

# logn = 4
# init = array rep of hello world
# A = printf.O (?)
rom = ROM(4, init, printf.O)

# last value is 0 because of the UART protocol?
data = array(rom.O[7], rom.O[6], rom.O[5], rom.O[4],
             rom.O[3], rom.O[2], rom.O[1], rom.O[0], 0)

# data = array(main.RX, main.RX, main.RX, main.RX,
             # main.RX, main.RX, main.RX, main.RX, 0)

# baud rate - we shouldn't have to change this.
clock = CounterModM(103, 8)
baud = clock.COUT

# r = reset? why is this true?
count = Counter(4, ce=True, r=True)

# Decode 'decodes' the 4 bit number 15 - and returns the bit representation of that,
# And returns a ROM with 4 elements. 
# count is being passed into this ROM?
done = Decode(15, 4)(count)

run = DFF(ce=True)

# what's this value?
run_n = LUT3([0,0,1,0, 1,0,1,0])

# Will have a value in it - but what?
run_n(done, valid, run)

# Will change the value of the flip flop?
run(run_n)

# Clock enable bit will be changed based on the baud speed - so will get
# enabled only when baud rate correct.
wire(baud, run.CE)

# Will reset when done and not run - so basically it is just done and its not
# running - and this should happen at the specified baud frequency.
reset = LUT2(I0&~I1)(done, run)
count(CE=baud, RESET=reset)

# What is happening at this stage?
shift = PISO(9, ce=True)
load = LUT2(I0&~I1)(valid,run)
shift(1,data,load)
wire(baud, shift.CE)

ready = LUT2(~I0 & I1)(run, baud)
wire(ready, printf.CE)


wire(shift, main.TX)


compile(sys.argv[1], main)
