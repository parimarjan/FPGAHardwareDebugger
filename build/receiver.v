module main (output  D4, output  D3, output  D2, output  D1, input  CLKIN, output  TX, input  RX);
wire  inst0_TX;
wire [7:0] inst0_rx_byte;
wire  inst1_TX;
receiver inst0 (.iCE_CLK(CLKIN), .RX(RX), .TX(inst0_TX), .rx_byte(inst0_rx_byte));
transmitter inst1 (.iCE_CLK(CLKIN), .tx_byte(inst0_rx_byte), .TX(inst1_TX));
assign D4 = inst0_rx_byte[3];
assign D3 = inst0_rx_byte[2];
assign D2 = inst0_rx_byte[1];
assign D1 = inst0_rx_byte[0];
assign TX = inst1_TX;
endmodule

