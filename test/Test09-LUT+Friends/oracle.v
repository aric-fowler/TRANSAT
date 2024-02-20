module oracle (a,b,c,o);
    input a,b,c;
    output o;

    wire n1;

    or(n1,b,c);
    xor(o,n1,a);
endmodule