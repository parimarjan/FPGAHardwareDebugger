module main (input [7:0] J1, output  D4, output  D3, output  D2, output  D1, input  CLKIN, output  TX, input  RX);
wire [7:0] inst0_REC_BYTE;
wire  inst0_TX;
wire  inst0_RECEIVED;
wire  inst1_TX;
receiver inst0 (.iCE_CLK(CLKIN), .RX(RX), .REC_BYTE(inst0_REC_BYTE), .TX(inst0_TX), .RECEIVED(inst0_RECEIVED));
transmit inst1 (.iCE_CLK(CLKIN), .RX(RX), .transmit_byte(inst0_REC_BYTE), .TX(inst1_TX));
assign D4 = inst0_REC_BYTE[3];
assign D3 = inst0_REC_BYTE[2];
assign D2 = inst0_REC_BYTE[1];
assign D1 = inst0_REC_BYTE[0];
assign TX = inst1_TX;
endmodule

