import sys
import os
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *

import math
import inspect
import subprocess

import serial
import time

'''
FIXME's:
    1. Fail gracefully if the output byte isn't being able to be read - maybe
    re-run the test with greater sleep times in between etc.

    2. Nice summary of failure/success rate of results - can return the boolean
    variables in a list to the caller (for input_test_file) or just return 1
    bool for input test case.

    3. enable bit stuff - this would include pasting the imported file to be
    tested on top of the testing code - and then modifying enable bits?

'''

class MTest():

    def __init__(self, main, num_inputs=1, num_outputs=1, verbose=True):
        '''
        Here we will set up the code for num_inputs and num_outputs.

        MTest.receivers will be a list of receiver arrays that you control -
        each element will be the 8 bytes that the user can wire up to whatever
        when setting up his test case

        Assumptions:
            1. test_file is in the correct directory - from where we just need
            to change the Makefile to upload it. Maybe change this and generate
            our own tmp build etc structure 

        '''

        self.main = main
        self.verbose = verbose

        self.makefile = './build/Makefile'
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        # Other config parameters, that at the moment we do not provide a way
        # to set.
        self.extra_cycles = 2
        self.timeout = 1
        self.serial_name = "/dev/tty.usbserial-141B"

        # Process the test file and deal with enable bits if required.
        # Generate a tmp .py magma file which we will upload after making all
        # the modifications

        # TODO: Can this fail sometimes?
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        file_name = module.__file__
        path = os.path.abspath(file_name)

        if 'tmp' not in file_name:
            self.generate_test_file(path)
            self._update_makefile()
        else:
            self.test_file_name = file_name
            self.test_file_path = path
 
        # Code for generating the receivers and senders on the fpga
        self.receivers = []
        # self.output_byte = In(Array(8, Bit))
        self.output = array(*[0]*8)

        receivers = []
        counter_n = int(math.ceil(math.log(num_inputs, 2))) + self.extra_cycles
        counter = Counter(counter_n, ce=True)

        decoder = Decoder(counter_n)
        decoder(counter.O)

        for i in range(num_inputs):
            receivers.append(RECEIVER())
            receivers[i](main.CLKIN, main.RX, decoder.O[i])
            
        wire(counter.CE, receivers[0].RECEIVED)
        
        for r in receivers:
            self.receivers.append(r.REC_BYTE)
    
    # FIXME: Combine these two functions together.
    def _update_makefile(self):
        '''
        FIXME: Add the receiver_helper etc stuff here itself in the makefile?
        '''

        data = _read_in_file(self.makefile)
        # f = open(self.makefile, 'w')

        name = 'NAME=' + self.test_file_name[:-3]
        
        old_len = len(data)
        for i in range(len(data)):
            if "NAME" in data[i] and data[i][0] != "#":
                del data[i]
                break

        assert len(data) == old_len-1, "only delete one line from makefile"

        data = "\n".join(data)
        
        # writes the updated data in the same file
        with file(self.makefile, 'w') as modified: 
            modified.write(name + '\n')
            modified.write(data)

        print('updated makefile!')
    
    def _update_doit(self, doit_path):
        '''
        FIXME: Add the receiver_helper etc stuff here itself in the makefile?

        NOT USING THIS ANYMORE. 
        TODO: Cleanup.
        '''

        data = _read_in_file(doit_path)
        # f = open(self.makefile, 'w')

        old_len = len(data)
        for i in range(len(data)):

            if "bake" in data[i] and "clean" not in data[i]:
                del data[i]
                break
        
        assert len(data) == old_len-1, "only delete one line from makefile"
        data.insert(i, bake)
        assert len(data) == old_len, "only delete one line from makefile"

        data = "\n".join(data)
        
        # writes the updated data in the same file
        with file(doit_path, 'w') as modified: 
            modified.write(data)

        print('updated doit file!')

    def generate_test_file(self, path):
        '''
        Generates a temporary test file and modifies it as neccessary. Might
        want to add the imported function which is to be tested - and modify
        its CE bits etc. Or not.
        '''
        #FIXME: Doesn't work on windows
        output_file_name = os.path.basename(path)
        output_file_name = 'tmp_' + output_file_name
        output_path = os.path.join(os.path.dirname(path), output_file_name)
        
        self._modify_file(path, output_path)
        
        # This will be used with the Makefile
        self.test_file_name = output_file_name

        self.test_file_path = output_path
    
    def _modify_file(self, orig_path, new_path):
        '''
        Will update the file at new path with everything from orig_path - and
        add the changes that we require there.
        '''
        input_data = _read_in_file(orig_path)

        # FIXME: We can make more complicated modifications here
        output = open(new_path, 'w')
        for line in input_data:
            if 'end_circuit' in line:
                break
            output.write(line + '\n')
        
        # Write the final compile line
        output.write('compile(sys.argv[1], main)')
        output.close()

    def set_output_byte(self, output):
        '''
        FIXME: Support multiple outputs
        '''
        
        if type(output) == Out(Bit):
            # concatenate this with the lowest bit of the output
            output_byte = array(*([output] + [0]*7))

        elif len(output) != 8:
            # TODO: Test this
            extra_bits = 8 - len(output)
            output = concat(array(*[0]*extra_bits), output)

        else:
            output_byte = output
        
        assert len(output_byte) == 8, 'output byte must have length 8'

        transmit = TRANSMITTER()
        transmit(self.main.CLKIN, self.main.RX, output_byte)
        wire(transmit.TX, self.main.TX)
 
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

    def _upload(self):
        '''
        bake + make upload etc of our tmp file - which would basically be
        exactly the same as the test file + compile command etc
        The idea is that the user can continue with 
        '''
        pass

    def test_inputs(self, inputs, outputs):
        '''
        Each element of the inputs array will be the bit pattern to send to the
        corresponding receiver.

        We will pad them to make sure that they are 8 bits long and for now, we
        won't support longer inputs?

        @ret: output_byte(s) --> which the user can use to specify his test
        '''
        assert len(self.receivers) == len(inputs), 'should specify input \
                of each receiver'

        assert 1 == len(outputs), 'only 1 output supported so far'

        if self.verbose:
            print("Inputs:")
            for i in inputs:
                print(i)
            
            print('*************************')
            print("Expected Outputs:")
            for o in outputs:
                print(o)

        output_from_hardware = []

        with serial.Serial(self.serial_name, 9600, timeout=self.timeout) as ser:

            for i in inputs: 
                ser.write(chr(int(i, 2)))
                ser.read(1)

            end_of_circuit_array = []
            
            # Hacky ugly way:
            # additional writes in order to push our decoder - so by the
            # end of these write/reads - decoder is back to 0 - for the
            # next cycle of input test cases.
            # forward - as each of them will activate received etc.

            # counter_n was used as log_n value for decoder
            counter_n = int(math.ceil(math.log(self.num_inputs, \
                2)))+self.extra_cycles
            counter_n = 2**counter_n

            # number of tries before decoder will reset for next
            # input-output cycle
            output_tries = counter_n - self.num_inputs

            i = 0 

            # FIXME: generalize this to having the same result n times?
            prev_result = ''

            while i < output_tries:
                
                ser.write("\x00")
                bytes_to_read = ser.inWaiting()
                while bytes_to_read == 0:
                    bytes_to_read = ser.inWaiting()
                    print('in while loop, bytes to read is ', bytes_to_read)
                    ser.write("\x00")
                    time.sleep(0.1)
                    i += 1

                print('after loop, bytes to read is ', bytes_to_read)

                # dummy write - which promts the module to send back bits.
                result = ser.read(bytes_to_read)
                i += 1
                if result != '' and result == prev_result:
                    break 

                prev_result = result

            output = result.encode('hex')
            
            # if output_tries are left over - here we don't have to waste
            # time by sleeping.
            for j in range(i, output_tries, 1):
                ser.write("\x00")
                ser.read(1)
            
            output_from_hardware.append(output)
                
        if self.verbose:
                print("Output from hardware:")
                for o in output_from_hardware:
                        print(o)
                        print(bin(int(o, 16)))
                print('------------------------------------')

    def test_input_file(self, file_name):
        '''
        @ret: Num pass / fail
        '''
        # Add some asserts

        # input = "\x11" #first number will be the first 4 bits, second will be the second 4 bits

        file = open(file_name)

        lines = file.readlines()

        for line in lines:
                
            split_line = line.split('|')
            
            assert len(split_line) == 2, "Inputs and outputs must be separated by |" 

            input_of_line = split_line[0]
            output_of_line = split_line[1]

            inputs = input_of_line.split(',')
            outputs = output_of_line.split(',')
            
            self.test_inputs(inputs, outputs)


        
    def end_circuit(self):
        '''
        Basically specifies that all the lines after end_circuit will be used
        for testing in the python file. Also - this appears to be the perfect
        place to uplaod the file to the icestick.

        Send back nasty errors if it fails.
        '''
        doit = os.path.dirname(self.test_file_path)
        doit = os.path.join(doit, 'doit')

        args = ['sh', doit]

        # TODO: Need to take in the password without viewing it and then pass
        # it to subprcess....ugh such a pain, maybe get pexpect to work
        # password = raw_input('password:')

        proc = subprocess.Popen(args, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

        # proc.stdin.write(password + '\n')
        proc.stdin.flush()

        stdout, stderr = proc.communicate()

        if self.verbose:
            print stdout
            print stderr

        # Since we have already uploaded the file to the icestick, we can clean
        # up now
        self._cleanup()

    def _cleanup(self):
        '''
        '''
        os.remove(self.test_file_path)
              
def _read_in_file(file_name):
    '''
    '''
    f = open(file_name, 'r')
    input_data = f.read()
    f.close()
    input_data = input_data.split('\n')
    return input_data

