module Addcout2 (input [1:0] I0, input [1:0] I1, output [1:0] O, output  COUT);
wire  inst0_O;
wire  inst1_CO;
wire  inst2_O;
wire  inst3_CO;
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(I0[0]), .I2(I1[0]), .I3(1'b0), .O(inst0_O));
SB_CARRY inst1 (.I0(I0[0]), .I1(I1[0]), .CI(1'b0), .CO(inst1_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst2 (.I0(1'b0), .I1(I0[1]), .I2(I1[1]), .I3(inst1_CO), .O(inst2_O));
SB_CARRY inst3 (.I0(I0[1]), .I1(I1[1]), .CI(inst1_CO), .CO(inst3_CO));
assign O = {inst2_O,inst0_O};
assign COUT = inst3_CO;
endmodule

module Register2CE (input [1:0] I, output [1:0] O, input  CLK, input  CE);
wire  inst0_Q;
wire  inst1_Q;
SB_DFFE inst0 (.C(CLK), .E(CE), .D(I[0]), .Q(inst0_Q));
SB_DFFE inst1 (.C(CLK), .E(CE), .D(I[1]), .Q(inst1_Q));
assign O = {inst1_Q,inst0_Q};
endmodule

module Counter2CE (output [1:0] O, output  COUT, input  CLK, input  CE);
wire [1:0] inst0_O;
wire  inst0_COUT;
wire [1:0] inst1_O;
Addcout2 inst0 (.I0(inst1_O), .I1({1'b0,1'b1}), .O(inst0_O), .COUT(inst0_COUT));
Register2CE inst1 (.I(inst0_O), .O(inst1_O), .CLK(CLK), .CE(CE));
assign O = inst1_O;
assign COUT = inst0_COUT;
endmodule

module Decoder2 (input [1:0] I, output [3:0] O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
SB_LUT4 #(.LUT_INIT(16'h0001)) inst0 (.I0(I[0]), .I1(I[1]), .I2(1'b0), .I3(1'b0), .O(inst0_O));
SB_LUT4 #(.LUT_INIT(16'h0002)) inst1 (.I0(I[0]), .I1(I[1]), .I2(1'b0), .I3(1'b0), .O(inst1_O));
SB_LUT4 #(.LUT_INIT(16'h0004)) inst2 (.I0(I[0]), .I1(I[1]), .I2(1'b0), .I3(1'b0), .O(inst2_O));
SB_LUT4 #(.LUT_INIT(16'h0008)) inst3 (.I0(I[0]), .I1(I[1]), .I2(1'b0), .I3(1'b0), .O(inst3_O));
assign O = {inst3_O,inst2_O,inst1_O,inst0_O};
endmodule

module main (output  D2, output  D1, input  CLKIN, output  TX, input  RX);
wire [1:0] inst0_O;
wire  inst0_COUT;
wire [3:0] inst1_O;
wire [7:0] inst2_REC_BYTE;
wire  inst2_TX;
wire  inst2_RECEIVED;
wire [7:0] inst3_REC_BYTE;
wire  inst3_TX;
wire  inst3_RECEIVED;
wire  inst4_O;
wire  inst5_CO;
wire  inst6_O;
wire  inst7_CO;
wire  inst8_O;
wire  inst9_CO;
wire  inst10_O;
wire  inst11_CO;
wire  inst12_O;
wire  inst13_CO;
wire  inst14_O;
wire  inst15_CO;
wire  inst16_O;
wire  inst17_CO;
wire  inst18_O;
wire  inst19_CO;
wire  inst20_TX;
Counter2CE inst0 (.O(inst0_O), .COUT(inst0_COUT), .CLK(CLKIN), .CE(inst2_RECEIVED));
Decoder2 inst1 (.I(inst0_O), .O(inst1_O));
receiver inst2 (.iCE_CLK(CLKIN), .RX(RX), .CE2(inst1_O[0]), .REC_BYTE(inst2_REC_BYTE), .TX(inst2_TX), .RECEIVED(inst2_RECEIVED));
receiver inst3 (.iCE_CLK(CLKIN), .RX(RX), .CE2(inst1_O[1]), .REC_BYTE(inst3_REC_BYTE), .TX(inst3_TX), .RECEIVED(inst3_RECEIVED));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst4 (.I0(1'b0), .I1(inst2_REC_BYTE[0]), .I2(inst3_REC_BYTE[0]), .I3(1'b0), .O(inst4_O));
SB_CARRY inst5 (.I0(inst2_REC_BYTE[0]), .I1(inst3_REC_BYTE[0]), .CI(1'b0), .CO(inst5_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst6 (.I0(1'b0), .I1(inst2_REC_BYTE[1]), .I2(inst3_REC_BYTE[1]), .I3(inst5_CO), .O(inst6_O));
SB_CARRY inst7 (.I0(inst2_REC_BYTE[1]), .I1(inst3_REC_BYTE[1]), .CI(inst5_CO), .CO(inst7_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst8 (.I0(1'b0), .I1(inst2_REC_BYTE[2]), .I2(inst3_REC_BYTE[2]), .I3(inst7_CO), .O(inst8_O));
SB_CARRY inst9 (.I0(inst2_REC_BYTE[2]), .I1(inst3_REC_BYTE[2]), .CI(inst7_CO), .CO(inst9_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst10 (.I0(1'b0), .I1(inst2_REC_BYTE[3]), .I2(inst3_REC_BYTE[3]), .I3(inst9_CO), .O(inst10_O));
SB_CARRY inst11 (.I0(inst2_REC_BYTE[3]), .I1(inst3_REC_BYTE[3]), .CI(inst9_CO), .CO(inst11_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst12 (.I0(1'b0), .I1(inst2_REC_BYTE[4]), .I2(inst3_REC_BYTE[4]), .I3(inst11_CO), .O(inst12_O));
SB_CARRY inst13 (.I0(inst2_REC_BYTE[4]), .I1(inst3_REC_BYTE[4]), .CI(inst11_CO), .CO(inst13_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst14 (.I0(1'b0), .I1(inst2_REC_BYTE[5]), .I2(inst3_REC_BYTE[5]), .I3(inst13_CO), .O(inst14_O));
SB_CARRY inst15 (.I0(inst2_REC_BYTE[5]), .I1(inst3_REC_BYTE[5]), .CI(inst13_CO), .CO(inst15_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst16 (.I0(1'b0), .I1(inst2_REC_BYTE[6]), .I2(inst3_REC_BYTE[6]), .I3(inst15_CO), .O(inst16_O));
SB_CARRY inst17 (.I0(inst2_REC_BYTE[6]), .I1(inst3_REC_BYTE[6]), .CI(inst15_CO), .CO(inst17_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst18 (.I0(1'b0), .I1(inst2_REC_BYTE[7]), .I2(inst3_REC_BYTE[7]), .I3(inst17_CO), .O(inst18_O));
SB_CARRY inst19 (.I0(inst2_REC_BYTE[7]), .I1(inst3_REC_BYTE[7]), .CI(inst17_CO), .CO(inst19_CO));
transmit inst20 (.iCE_CLK(CLKIN), .RX(RX), .transmit_byte({inst18_O,inst16_O,inst14_O,inst12_O,inst10_O,inst8_O,inst6_O,inst4_O}), .TX(inst20_TX));
assign TX = inst20_TX;
endmodule

