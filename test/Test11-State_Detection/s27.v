// Rising edge-triggered flip-flop
module dff (d,clk,r,q);
    input d, clk, r;
    output q;
    wire int1,int2,int3,int4;   // Intermediate nodes

    // First latch
    notif0 u1_0(int1,d,clk);
    nor u1_1(int2,int1,r);
    notif1 u1_2(int1,int2,clk);

    // Second latch & output
    notif1 u2_0(int3,int2,clk);
    nor u2_1(int4,int3,r);
    notif0 u2_2(int3,int4,clk);
    not (q,int3);



endmodule

// ISCAS '89 sequential benchmark circuit s29. Modified with global reset.
module s27(g0,g1,g2,g3,g17,clk,r);
    input g0, g1, g2, g3;
    input clk, r;
    output g17;

    wire g5,g6,g7,g8,g9,g10,g11,g12,g13,g14,g15,g16;

    not(g14,g0);
    nor(g12,g1,g7);
    and(g8,g6,g14);
    nor(g13,g2,g12);
    or(g15,g8,g12);
    or(g16,g3,g8);
    nand(g9,g15,g16);
    nor(g11,g5,g9);
    nor(g10,g11,g14);
    not(g17,g11);

    dff ff0(.d(g13),.clk(clk),.r(r),.q(g7));
    dff ff1(.d(g10),.clk(clk),.r(r),.q(g5));
    dff ff2(.d(g11),.clk(clk),.r(r),.q(g6));

endmodule
