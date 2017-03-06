import sys

UART_FILE = "./uart_integration.v"

MAKEFILE = "./Makefile"

INCLUDE_LINE = "`include \"uart_api/uart.v\""
LAST_LINE = "top t1(CLKIN, RX, TX);"

# Read in the Makefile and figure out the name of which file we are changing.

# tmp solution
name = "./blink.v"



# Append the text of UART_FILE under name file.

files_to_append = [UART_FILE]

# Write some extra stuff before pasting the contents of tmp_file.
with file(name, 'r') as original: 
    data = original.read()

data = data.split("\n")

old_len = len(data)

for i in range(len(data)-1,0,-1):
    if "endmodule" in data[i]:
        del data[i]
        break
    del data[i]

assert len(data) <= old_len-1, "test"

data = "\n".join(data)

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
