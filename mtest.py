import sys
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *
import math

'''
Figure out a way to reset the receiver arrays without unloading/uploading to
fpga again
'''

class MTest():

    def __init__(self, main, test_file, test_func=None,n=1, num_outputs=1):
        '''
        Here we will set up the code for num_inputs and num_outputs.

        MTest.receivers will be a list of receiver arrays that you control -
        each element will be the 8 bytes that the user can wire up to whatever
        when setting up his test case
        '''
        self.main = main
        self.test_file = test_file
        # Process the test file and deal with enable bits if required.

        
        # Code for generating the receivers and senders on the fpga
        self.receivers = []
        # self.output_byte = In(Array(8, Bit))
        self.output = array(*[0]*8)

        receivers = []
        counter_n = int(math.ceil(math.log(n, 2)))
        counter = Counter(counter_n+1, ce=True)

        decoder = Decoder(counter_n+1)
        decoder(counter.O)

        for i in range(n):
            receivers.append(RECEIVER())
            receivers[i](main.CLKIN, main.RX, decoder.O[i])
            
        wire(counter.CE, receivers[0].RECEIVED)
        
        # echo = TRANSMITTER()
        # echo(main.CLKIN, main.RX, self.output)
        # wire(echo.TX, main.TX)
        
        for r in receivers:
            self.receivers.append(r.REC_BYTE)

        # Generate a tmp .py magma file which we will upload after making all
        # the modifications

    def set_output_byte(self, output):

        echo = TRANSMITTER()
        echo(self.main.CLKIN, self.main.RX, output)
        wire(echo.TX, self.main.TX)
 
    def add_test_lines(self, test_line):
        '''
        FIXME: Ideally this shouldn't be 
        Here the user should give us the exact lines in the test, for example:
            - mtest.outputs[0], cout = Adder(mtest.receiver[0], mtest.receiver[1])

            Basically this wiring just involves calling the function to be
            tested from the test_file specified before - and setting up the
            input/output wiring. This is probably the easiest for us, and the
            user - as there are different ways to set up input bits etc
        '''
        pass

    def upload(self):
        '''
        bake + make upload etc of our tmp file - which would basically be
        exactly the same as the test file + compile command etc
        The idea is that the user can continue with 
        '''
        pass

    def send_inputs(self, inputs):
        '''
        Each element of the inputs array will be the bit pattern to send to the
        corresponding receiver.

        We will pad them to make sure that they are 8 bits long and for now, we
        won't support longer inputs?

        @ret: output_byte(s) --> which the user can use to specify his test
        '''
        assert len(self.receivers) == len(inputs), 'should specify input \
                of each receiver'
        
              


