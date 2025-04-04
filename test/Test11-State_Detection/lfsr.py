#!/usr/bin/env python3
from z3 import *

# I/O
clk = Bool('clk')
r = Bool('r')
q_5 = Bool('q_5')

# Internal nodes
d_1 = Bool('d_1')
intA_1 = Bool('intA_1')
intB_1 = Bool('intB_1')
intC_1 = Bool('intC_1')
intD_1 = Bool('intD_1')
q_1 = Bool('q_1')
intA_2 = Bool('intA_2')
intB_2 = Bool('intB_2')
intC_2 = Bool('intC_2')
intD_2 = Bool('intD_2')
q_2 = Bool('q_2')
intA_3 = Bool('intA_3')
intB_3 = Bool('intB_3')
intC_3 = Bool('intC_3')
intD_3 = Bool('intD_3')
q_3 = Bool('q_3')
intA_4 = Bool('intA_4')
intB_4 = Bool('intB_4')
intC_4 = Bool('intC_4')
intD_4 = Bool('intD_4')
q_4 = Bool('q_4')
intA_5 = Bool('intA_5')
intB_5 = Bool('intB_5')
intC_5 = Bool('intC_5')
intD_5 = Bool('intD_5')

# Combinational logic
c0 = (d_1 == Not(Xor(q_3,q_5)))

# DFF architecture - rising edge, asynchronous active-high reset
c1 = Implies(Not(clk),(intA_1 == Not(d_1)))
c2 = (intB_1 == Not(Or(r,intA_1)))
c3 = Implies(clk,(intA_1 == Not(intB_1)))
c4 = Implies(clk,(intC_1 == Not(intB_1)))
c5 = (intD_1 == Not(Or(r,intC_1)))
c6 = Implies(Not(clk),(intC_1 == Not(intD_1)))
c7 = (q_1 == Not(intC_1))

c8 = Implies(Not(clk),(intA_2 == Not(q_1)))
c9 = (intB_2 == Not(Or(r,intA_2)))
c10 = Implies(clk,(intA_2 == Not(intB_2)))
c11 = Implies(clk,(intC_2 == Not(intB_2)))
c12 = (intD_2 == Not(Or(r,intC_2)))
c13 = Implies(Not(clk),(intC_2 == Not(intD_2)))
c14 = (q_2 == Not(intC_2))

c15 = Implies(Not(clk),(intA_3 == Not(q_2)))
c16 = (intB_3 == Not(Or(r,intA_3)))
c17 = Implies(clk,(intA_3 == Not(intB_3)))
c18 = Implies(clk,(intC_3 == Not(intB_3)))
c19 = (intD_3 == Not(Or(r,intC_3)))
c20 = Implies(Not(clk),(intC_3 == Not(intD_3)))
c21 = (q_3 == Not(intC_3))

c22 = Implies(Not(clk),(intA_4 == Not(q_3)))
c23 = (intB_4 == Not(Or(r,intA_4)))
c24 = Implies(clk,(intA_4 == Not(intB_4)))
c25 = Implies(clk,(intC_4 == Not(intB_4)))
c26 = (intD_4 == Not(Or(r,intC_4)))
c27 = Implies(Not(clk),(intC_4 == Not(intD_4)))
c28 = (q_4 == Not(intC_4))

c29 = Implies(Not(clk),(intA_5 == Not(q_4)))
c30 = (intB_5 == Not(Or(r,intA_5)))
c31 = Implies(clk,(intA_5 == Not(intB_5)))
c32 = Implies(clk,(intC_5 == Not(intB_5)))
c33 = (intD_5 == Not(Or(r,intC_5)))
c34 = Implies(Not(clk),(intC_5 == Not(intD_5)))
c35 = (q_5 == Not(intC_5))

# Testing
s = Solver()
s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35)

print(s.check())
print(s.model())