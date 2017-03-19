module main (output  D2, output  D1, input [7:0] J3, input  CLKIN, output  TX, input  RX);
wire [7:0] inst0_rx_byte;
wire  inst1_O;
wire  inst2_CO;
wire  inst3_O;
wire  inst4_CO;
wire  inst5_O;
wire  inst6_CO;
wire  inst7_O;
wire  inst8_CO;
wire  inst9_TX;
receiver inst0 (.iCE_CLK(CLKIN), .RX(RX), .rx_byte(inst0_rx_byte));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst1 (.I0(1'b0), .I1(inst0_rx_byte[0]), .I2(inst0_rx_byte[4]), .I3(1'b0), .O(inst1_O));
SB_CARRY inst2 (.I0(inst0_rx_byte[0]), .I1(inst0_rx_byte[4]), .CI(1'b0), .CO(inst2_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst3 (.I0(1'b0), .I1(inst0_rx_byte[1]), .I2(inst0_rx_byte[5]), .I3(inst2_CO), .O(inst3_O));
SB_CARRY inst4 (.I0(inst0_rx_byte[1]), .I1(inst0_rx_byte[5]), .CI(inst2_CO), .CO(inst4_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst5 (.I0(1'b0), .I1(inst0_rx_byte[2]), .I2(inst0_rx_byte[6]), .I3(inst4_CO), .O(inst5_O));
SB_CARRY inst6 (.I0(inst0_rx_byte[2]), .I1(inst0_rx_byte[6]), .CI(inst4_CO), .CO(inst6_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst7 (.I0(1'b0), .I1(inst0_rx_byte[3]), .I2(inst0_rx_byte[7]), .I3(inst6_CO), .O(inst7_O));
SB_CARRY inst8 (.I0(inst0_rx_byte[3]), .I1(inst0_rx_byte[7]), .CI(inst6_CO), .CO(inst8_CO));
echo inst9 (.iCE_CLK(CLKIN), .RX(RX), .transmit_byte({inst7_O,inst5_O,inst3_O,inst1_O,inst7_O,inst5_O,inst3_O,inst1_O}), .TX(inst9_TX));
assign TX = inst9_TX;
endmodule

