module main (input [7:0] J1, output [7:0] J3);
wire  inst0_O;
wire  inst1_CO;
wire  inst2_O;
wire  inst3_CO;
wire  inst4_O;
wire  inst5_CO;
wire  inst6_O;
wire  inst7_CO;
wire  inst8_Q;
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(J1[0]), .I2(J1[4]), .I3(1'b0), .O(inst0_O));
SB_CARRY inst1 (.I0(J1[0]), .I1(J1[4]), .CI(1'b0), .CO(inst1_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst2 (.I0(1'b0), .I1(J1[1]), .I2(J1[5]), .I3(inst1_CO), .O(inst2_O));
SB_CARRY inst3 (.I0(J1[1]), .I1(J1[5]), .CI(inst1_CO), .CO(inst3_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst4 (.I0(1'b0), .I1(J1[2]), .I2(J1[6]), .I3(inst3_CO), .O(inst4_O));
SB_CARRY inst5 (.I0(J1[2]), .I1(J1[6]), .CI(inst3_CO), .CO(inst5_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst6 (.I0(1'b0), .I1(J1[3]), .I2(J1[7]), .I3(inst5_CO), .O(inst6_O));
SB_CARRY inst7 (.I0(J1[3]), .I1(J1[7]), .CI(inst5_CO), .CO(inst7_CO));
SB_DFF inst8 (.D(1'b0), .Q(inst8_Q));
assign J3 = {inst8_Q,inst8_Q,inst8_Q,inst7_CO,inst6_O,inst4_O,inst2_O,inst0_O};
endmodule

