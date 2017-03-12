module test(input input_bit);

  reg register;

  SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(J1[0]), .I2(J1[4]), .I3(1'b0), .O(inst0_O));

endmodule

  // never resets it.
