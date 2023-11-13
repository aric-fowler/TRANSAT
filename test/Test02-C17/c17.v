module c17 (pi1, pi2, pi3, pi6, pi7, po22, po23);
    input pi1, pi2, pi3;
    input pi6, pi7;
    output po22;
    output po23;

    wire pi10, pi11, pi16, pi19;

    nand nand1(pi10,pi1,pi3);
    nand nand2(pi11,pi3,pi6);
    nand nand6(pi16,pi2,pi11);
    nand nand5(pi19,pi11,pi7);
    nand nand3(po22,pi16,pi10);
    nand nand4(po23,pi16,pi19);

endmodule

module encrypted_c17 (pi1,pi2,pi3,pi6,pi7,k0,k1,k2,k3,po22_enc,po23_enc);
    input pi1,pi2,pi3,pi6,pi7;
    input k3,k2,k1,k0;
    output po22_enc,po23_enc;

    wire net1,net2,net3,net4,net5,net6,net7,net8;

    xnor xnor1(net1,k0,pi7);
    nand nand1(net2,pi1,pi3);
    nand nand2(net3,pi3,pi6);
    and and1(net4,net1,net3);
    and and2(net5,net3,pi2);
    xor xor2(net6,k2,net4);
    xnor xnor2(net7,net5,k1);
    nand nand3(po22_enc,net2,net7);
    nand nand4(net8,net7,net6);
    xor xor1(po23_enc,net8,k3);

endmodule
