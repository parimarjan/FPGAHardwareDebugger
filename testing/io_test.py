import serial
import time

serial_name = "/dev/tty.usbserial-141B"


verbose = False
input = "\x11" #first number will be the first 4 bits, second will be the second 4 bits

file = open("test_file.txt")
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
			print("\\x"+i)

		print("Expected Outputs:")
		for o in outputs:
			print("\\x"+o)

	output_from_hardware = []

	
	with serial.Serial(serial_name, 9600, timeout=1) as ser:
		for i in inputs:
			ser.write("\\x" + i)

		end_of_circuit_array = []

		while(true):
			for o in outputs:
				output_from_hardware.append(ser.read(1).encode("hex"))
				if end_of_circuit_array == output_from_hardware:
					break
				else:
					end_of_circuit_array = output_from_hardware

	if verbose:
		print("Output from hardware:")
		for o in output_from_hardware:
			print(o)

