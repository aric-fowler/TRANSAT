module s27_tb();
    reg clk, r;     // Global clock & reset
    reg d;          // Testing DFF
    wire q;         // Testing DFF

    reg g0,g1,g2,g3;// Testing S27
    wire [3:0] ins;
    wire g17;       // Testing S27

    integer i;

    dff dut0(.d(d), .r(r), .clk(clk), .q(q));
    s27 dut1(.g0(g0),.g1(g1),.g2(g2),.g3(g3),.g17(g17),.clk(clk),.r(r));
    assign ins = {g3,g2,g1,g0};

    initial begin
        $dumpfile("dut_waveforms.vcd");
        $dumpvars(0,dut0,dut1);
        $display("Running testbench...");
        //$display("Resetting... \t\t\tQ = %b", q);
        $display("Resetting... \t\t\tg17 = %b", g17);
        r = 1;
        clk = 0;
        d = 0;
        {g3,g2,g1,g0} = 4'b0000;
        #5
        clk = 1;
        //$display("Reset complete:\t\t\tQ = %b",q);
        $display("Reset complete:\t\t\tg17 = %b",g17);
        //$monitor("Clk = %b\t\tD = %b,\t\tQ = %b", clk,d,q);
        $monitor("Clk = %b\tIns = %b\t\tg17 = %b",clk,ins,g17);
        r = 0;
        clk = 0;
        for(i=0; i<20; i=i+1) begin
            #5
            clk = ~clk;
            {g3,g2,g1,g0} = {g3,g2,g1,g0} + 4'b0001;
            if ((i % 3) == 0) begin
                d = ~d;
            end
        end
    end

endmodule
