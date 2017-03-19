// `include "uart_api/uart2.v"
module receiver(
  // clk name doesn't matter I guess?
	input iCE_CLK,
  // RX and TX pins
  input RX,
  output [7:0] REC_BYTE,
  output TX,
	);

  // never resets it.
	wire reset = 0;

  reg transmit;
  reg [7:0] tx_byte;
	wire received;
	wire is_receiving;

  // never using these
	wire is_transmitting;
	wire recv_error;

	uart #(
		.baud_rate(9600),                 // The baud rate in kilobits/s
		.sys_clk_freq(12000000)           // The master clock frequency
	)
	uart0(
		.clk(iCE_CLK),                    // The master clock for this module
		.rst(reset),                      // Synchronous reset
		.rx(RX),                // Incoming serial line
    .tx(TX),                // Outgoing serial line
		.transmit(transmit),              // Signal to transmit
		.tx_byte(tx_byte),                // Byte to transmit
		.received(received),              // Indicated that a byte has been received
		.rx_byte(REC_BYTE),                // Byte received
		.is_receiving(is_receiving),      // Low when receive line is idle
		.is_transmitting(is_transmitting),// Low when transmit line is idle
		.recv_error(recv_error)           // Indicates error in receiving packet.
	);

  always @(posedge iCE_CLK) begin
    if (received) begin
      //tx_byte <= output_byte;
      transmit <= 1;
    end else begin
      transmit <= 0;
    end
  end
endmodule
