module main (input [7:0] J1, output  D4, output  D3, output  D2, output  D1, input  CLKIN, output  TX, input  RX);
wire  inst0_TX;
wire [7:0] inst0_rx_byte;
receiver inst0 (.iCE_CLK(CLKIN), .RX(RX), .TX(inst0_TX), .rx_byte(inst0_rx_byte));
assign D4 = inst0_rx_byte[3];
assign D3 = inst0_rx_byte[2];
assign D2 = inst0_rx_byte[1];
assign D1 = inst0_rx_byte[0];
assign TX = inst0_TX;
endmodule

