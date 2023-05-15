module custom_circuit (A,B,C,O);

    input A,B,C;
    output O;

    wire net1;

    nand nand1(net1,B,C);
    nand nand2(O,A,net1);

endmodule
