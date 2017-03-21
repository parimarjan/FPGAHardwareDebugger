import sys
import os
from magma import *
from mantle import *
from boards.icestick import IceStick
from uart import *

import math
import inspect
import subprocess

# import sys
# import pexpect
# import getpass

'''
Figure out a way to reset the receiver arrays without unloading/uploading to
fpga again
'''

class MTest():

    def __init__(self, main, n=1, num_outputs=1):
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

        self.makefile = './build/Makefile'
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
            print('tmp file being run now')
 
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
        '''

        data = _read_in_file(doit_path)
        # f = open(self.makefile, 'w')

        # name = 'NAME=' + self.test_file_name[:-3]
        bake = './bake ' + self.test_file_name + '\n'
        
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
        print('self.test_file_name = ', self.test_file_name)

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
            print('output is a single bit!')
            # concatenate this with the lowest bit of the output
            output_byte = array(*([output] + [0]*7))

        elif len(output) != 8:
            # TODO: Test this
            extra_bits = 8 - len(output)
            output = concat(array(*[0]*extra_bits), output)

        else:
            output_byte = output
        
        assert len(output_byte) == 8, 'output byte must have length 8'

        echo = TRANSMITTER()
        echo(self.main.CLKIN, self.main.RX, output_byte)
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
        
    def end_circuit(self):
        '''
        Basically specifies that all the lines after end_circuit will be used
        for testing in the python file. Also - this appears to be the perfect
        place to uplaod the file to the icestick.

        Send back nasty errors if it fails.
        '''
        print('in end circuit!')

        doit = os.path.dirname(self.test_file_path)
        doit = os.path.join(doit, 'doit')

        # commands = ['export PYTHONPATH=$PYTHONPATH:~/CS/cs448h/CS448H/magma',
                    # 'export MANTLE=lattice',
                    # 'export MANTLE_TARGET=ice40',
                    # './bake clean',
                    # './bake FILE_NAME', 
                    # 'sudo kextunload -b com.apple.driver.AppleUSBFTDI',
                    # 'build/make upload',
                    # 'sudo kextload -b com.apple.driver.AppleUSBFTDI']
        
        # self._update_doit(doit)

        args = ['sh', doit]
        print('command is ', ' '.join(args))

        # TODO: Need to take in the password without viewing it and then pass
        # it to subprcess....ugh such a pain, maybe get pexpect to work
        # password = raw_input('password:')

        proc = subprocess.Popen(args, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

        print('subprocess.popen done')
        # proc.stdin.write(password + '\n')
        proc.stdin.flush()

        stdout, stderr = proc.communicate()
        print stdout
        print stderr

        # Since we have already uploaded the file to the icestick, we can clean
        # up now
        self._cleanup()

        # FIXME: This should technically work too...figure it out.
        # password = getpass.getpass("Enter password: ")

        # child = pexpect.spawn ('/bin/bash')
        # child.sendline('sudo ls')
        # #If you are using pxssh you can use this
        # #child.prompt()
        # child.expect("password")
        # print(child.before)

        # child = pexpect.spawn(command)
        # i = child.expect([pexpect.TIMEOUT, "password:"])
        # if i == 0:
            # print("Got unexpected output: %s %s" % (child.before, child.after))
            # sys.exit()
        # else:
            # child.sendline(password)

        # print(child.read())
        
    def _cleanup(self):
        '''
        '''
        pass
        # os.remove(self.test_file_path)
              
def _read_in_file(file_name):
    '''
    '''
    f = open(file_name, 'r')
    input_data = f.read()
    f.close()
    input_data = input_data.split('\n')
    return input_data

