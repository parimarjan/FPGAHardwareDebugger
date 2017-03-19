import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *

icestick = IceStick()

for i in range(8):
    icestick.J3[i].input().on()

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


receiver = RECEIVER()
receiver(main.CLKIN, main.RX)

sum, cout = Add(receiver.rx_byte[0:4], receiver.rx_byte[4:8])
# result = Out(Array(4, Bit))
# reg = [DFF() for i in range(8)]
test_array = concat(sum, sum)

# O = [0]*8
# result = array(*O)

# wire(result[4], 1)

# wire(main.D1, result[0])
# wire(main.D2, result[7])

# arr = array(sum, 4)
# wire(sum, array2[0:4])
# wire(sum, result_array[0:4])
# wire(cout, result_array[4])

echo = ECHO()
echo(main.CLKIN, main.RX, test_array)
wire(echo.TX, main.TX)

compile(sys.argv[1], main)
