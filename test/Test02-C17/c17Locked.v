module c17Locked (pi1,pi2,pi3,pi6,pi7,k0,k1,k2,k3,po22,po23);
    input pi1,pi2,pi3,pi6,pi7;
    input k0,k1,k2,k3;      // Key inputs (you need to place this comment for ABC attack)
    output po22,po23;

    wire net0,net1,net2,net3,net4,net5,net6,net7,net8;

    not(net0,pi7);
    xnor(net1,k0,net0);
    nand(net2,pi1,pi3);
    nand(net3,pi3,pi6);
    and(net4,net1,net3);
    and(net5,net3,pi2);
    xor(net6,k2,net4);
    xnor(net7,net5,k1);
    nand(po22,net2,net7);
    nand(net8,net7,net6);
    xor(po23,net8,k3);

endmodule