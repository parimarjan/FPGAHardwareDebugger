`include "uart_api/uart.v"
module main (input [7:0] J1, output [4:0] J3, input CLKIN, input RX, output TX);
wire [4:0] output_byte;
wire [7:0] input_byte;
wire  inst0_O;
wire  inst1_CO;
wire  inst2_O;
wire  inst3_CO;
wire  inst4_O;
wire  inst5_CO;
wire  inst6_O;
wire  inst7_CO;
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(input_byte[0]), .I2(input_byte[4]), .I3(1'b0), .O(inst0_O));
SB_CARRY inst1 (.I0(input_byte[0]), .I1(input_byte[4]), .CI(1'b0), .CO(inst1_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst2 (.I0(1'b0), .I1(input_byte[1]), .I2(input_byte[5]), .I3(inst1_CO), .O(inst2_O));
SB_CARRY inst3 (.I0(input_byte[1]), .I1(input_byte[5]), .CI(inst1_CO), .CO(inst3_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst4 (.I0(1'b0), .I1(input_byte[2]), .I2(input_byte[6]), .I3(inst3_CO), .O(inst4_O));
SB_CARRY inst5 (.I0(input_byte[2]), .I1(input_byte[6]), .CI(inst3_CO), .CO(inst5_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst6 (.I0(1'b0), .I1(input_byte[3]), .I2(input_byte[7]), .I3(inst5_CO), .O(inst6_O));
SB_CARRY inst7 (.I0(input_byte[3]), .I1(input_byte[7]), .CI(inst5_CO), .CO(inst7_CO));
assign output_byte = {inst7_CO,inst6_O,inst4_O,inst2_O,inst0_O};
top t1(CLKIN, RX, TX, input_byte, output_byte);
endmodule
module top(
	input iCE_CLK,
	input RS232_Rx_TTL,
	output RS232_Tx_TTL,
  input [7:0] input_byte,
  output [4:0] output_byte
	);

	wire reset = 0;
	reg transmit;
	reg [7:0] tx_byte;
	wire received;
	wire [7:0] rx_byte;
	wire is_receiving;
	wire is_transmitting;
	wire recv_error;

	uart #(
		.baud_rate(9600),                 // The baud rate in kilobits/s
		.sys_clk_freq(12000000)           // The master clock frequency
	)
	uart0(
		.clk(iCE_CLK),                    // The master clock for this module
		.rst(reset),                      // Synchronous reset
		.rx(RS232_Rx_TTL),                // Incoming serial line
		.tx(RS232_Tx_TTL),                // Outgoing serial line
		.transmit(transmit),              // Signal to transmit
		.tx_byte(tx_byte),                // Byte to transmit
		.received(received),              // Indicated that a byte has been received
		.rx_byte(rx_byte),                // Byte received
		.is_receiving(is_receiving),      // Low when receive line is idle
		.is_transmitting(is_transmitting),// Low when transmit line is idle
		.recv_error(recv_error)           // Indicates error in receiving packet.
	);

	always @(posedge iCE_CLK) begin
		if (received) begin
      // FIXME: Change these numbers...
			input_byte <= rx_byte;
      tx_byte[4:0] <= output_byte[4:0];
			transmit <= 1;
		end else begin
			transmit <= 0;
		end
	end
endmodule
