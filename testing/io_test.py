import serial
import time
import sys

serial_name = "/dev/tty.usbserial-141B"

verbose = True
input = "\x11" #first number will be the first 4 bits, second will be the second 4 bits

print(len(sys.argv))
try:
    file_name = sys.argv[1]
except:
    print('provide test file name as arg')
    exit(0)

file = open(file_name)

lines = file.readlines()

for line in lines:
	
	split_line = line.split('|')
	
	assert len(split_line) == 2, "Inputs and outputs must be separated by |" 

	input_of_line = split_line[0]
	output_of_line = split_line[1]

	inputs = input_of_line.split(',')
	outputs = output_of_line.split(',')

	if verbose:
		print("Inputs:")
		for i in inputs:
			# print("\\x"+i)
                        print(i)
                
                print('')
		print("Expected Outputs:")
		for o in outputs:
			print(o)

	output_from_hardware = []

	
	with serial.Serial(serial_name, 9600, timeout=1) as ser:
                
                # ser.write("\x02")
                # ser.read(1)
                # ser.write("\x03")
                # ser.read(1)

                for i in inputs: 
                        ser.write(chr(int(i, 2)))
                        # ser.write("\\x" + i)
                        # time.sleep(0.1)
                        # output_from_hardware.append(ser.read(1).encode("hex"))
                        ser.read(1).encode("hex")

		end_of_circuit_array = []
                
                time.sleep(0.1)
                ser.write("\x00")
                ser.read(1).encode("hex")

                time.sleep(0.5)
                ser.write("\x00")
                output = ser.read(1).encode("hex")
                print(type(output))
                print(len(output))

                while output == '':
                    print('still in while loop...')
                    time.sleep(0.1)
                    ser.write("\x00")
                    output = ser.read(1).encode("hex")

                output_from_hardware.append(output)
                    

		# while(true):
			# for o in outputs:
				# output_from_hardware.append(ser.read(1).encode("hex"))
				# if end_of_circuit_array == output_from_hardware:
					# break
				# else:
					# end_of_circuit_array = output_from_hardware

	if verbose:
		print("Output from hardware:")
		for o in output_from_hardware:
			print(o)
                        print(bin(int(o, 16)))
                print('------------------------------------')

