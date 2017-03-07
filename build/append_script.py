import sys

UART_FILE = "./uart_integration.v"

# FIXME: Should be based on the name in the makefile
# PCF_FILE = "add.pcf"

MAKEFILE = "./Makefile"

INPUT_ARRAY_NAME = "input_byte"
OUTPUT_ARRAY_NAME = "output_byte"
EXTRA_MAIN_ARGS = ", input CLKIN, input RX, output TX);"

INPUT_SIZE = 7
OUTPUT_SIZE = 7

INPUT_ARRAY = "wire [" + str(INPUT_SIZE) + ":0] " + INPUT_ARRAY_NAME + ";"
OUTPUT_ARRAY = "wire [" + str(OUTPUT_SIZE) + ":0] " + OUTPUT_ARRAY_NAME + ";"

INCLUDE_LINE = "`include \"uart_api/uart.v\""

LAST_LINE = "\ntop t1(CLKIN, RX, TX, " + INPUT_ARRAY_NAME + ", " + \
            OUTPUT_ARRAY_NAME + ");"

# Read in the Makefile and figure out the name of which file we are changing.
# FIXME: Assuming only 1 verilog file is being uploaded
main_verilog_file = ""
make_file = open(MAKEFILE, "r")

for line in make_file:

    if line[0] != "#" and "NAME" in line:
        main_verilog_file = line.split()[-1]
        break

make_file.close()
name = main_verilog_file + ".v"

# FIXME: Can find this by checking the file first
MAIN_INPUT = "J1"
MAIN_OUTPUT = "J3"

# Append the text of UART_FILE under name file.

files_to_append = [UART_FILE]

# Write some extra stuff before pasting the contents of tmp_file.
with file(name, 'r') as original: 
    data = original.read()

data = data.split("\n")
old_len = len(data)

# Initialize input_byte / output_byte registers at the start of module main

for i, line in enumerate(data):

    if "module main" in line:
        # inserting an entry a
        data[i] = line.replace(");", EXTRA_MAIN_ARGS)
        break

data.insert(i+1, INPUT_ARRAY)
data.insert(i+1, OUTPUT_ARRAY)

# FIXME: Shouldn't go beyond the main function
for j, line in enumerate(data):
    if j <= i+1:
        continue

    data[j] = data[j].replace(MAIN_INPUT, INPUT_ARRAY_NAME)
    data[j] = data[j].replace(MAIN_OUTPUT, OUTPUT_ARRAY_NAME)

# Changing the dfinal line
for i in range(len(data)-1,0,-1):
    if "endmodule" in data[i]:
        del data[i]
        break
    del data[i]

assert len(data) <= old_len-1, "test"

data = "\n".join(data)

# writes the updated data in the same file
with file(name, 'w') as modified: 
    modified.write(INCLUDE_LINE + "\n")
    modified.write(data)
    modified.write(LAST_LINE + "\n")
    modified.write("endmodule\n")


f = open(name, "a")
for tmp_file in files_to_append:
    # open tmp_file
    tmp = open(tmp_file, "r")
    
    # write the full contents of the tmp file
    f.write(tmp.read())

f.close()

# Update the pcf file
# pcf_lines = ["set_io CLKIN 21", "set_io TX 8", "set_io RX 9"]

# f = open(PCF_FILE, "a")

# for line in pcf_lines:
    # f.write(line + "\n")

# f.close()
