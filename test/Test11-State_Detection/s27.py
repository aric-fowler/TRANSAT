#!/usr/bin/env python3
from z3 import *

# Inputs
g0 = Bool('g0')
g1 = Bool('g1')
g2 = Bool('g2')
g3 = Bool('g3')
clk = Bool('clk')
r = Bool('r')
#Internal Nets
g5 = Bool('g5')
g6 = Bool('g6')
g7 = Bool('g7')
g8 = Bool('g8')
g9 = Bool('g9')
g10 = Bool('g10')
g11 = Bool('g11')
g12 = Bool('g12')
g13 = Bool('g13')
g14 = Bool('g14')
g15 = Bool('g15')
g16 = Bool('g16')
intA_0 = Bool('intA_0')
intB_0 = Bool('intB_0')
intC_0 = Bool('intC_0')
intD_0 = Bool('intD_0')
intA_1 = Bool('intA_1')
intB_1 = Bool('intB_1')
intC_1 = Bool('intC_1')
intD_1 = Bool('intD_1')
intA_2 = Bool('intA_2')
intB_2 = Bool('intB_2')
intC_2 = Bool('intC_2')
intD_2 = Bool('intD_2')

#Outputs
g17 = Bool('g17')

# Combinational Logic
c1 = (g14 == Not(g0))
c2 = (g12 == Not(Or(g1,g7)))
c3 = (g8 == And(g6,g14))
c4 = (g13 == Not(Or(g2,g12)))
c5 = (g15 == Or(g8,g12))
c6 = (g16 == Or(g3,g8))
c7 = (g9 == Not(And(g15,g16)))
c8 = (g11 == Not(Or(g5,g9)))
c9 = (g10 == Not(Or(g11,g14)))
c10 = (g17 == Not(g11))

# DFF0 - G13 to G7
c11 = Implies(Not(clk),(intA_0 == Not(g13)))
c12 = (intB_0 == Not(Or(r,intA_0)))
c13 = Implies(clk,(intA_0 == Not(intB_0)))
c14 = Implies(clk,(intC_0 == Not(intB_0)))
c15 = (intD_0 == Not(Or(r,intC_0)))
c16 = Implies(Not(clk),(intC_0 == Not(intD_0)))
c17 = (g7 == Not(intC_0))

# DFF1 - G10 to G5
c18 = Implies(Not(clk),(intA_1 == Not(g10)))
c19 = (intB_1 == Not(Or(r,intA_1)))
c20 = Implies(clk,(intA_1 == Not(intB_1)))
c21 = Implies(clk,(intC_1 == Not(intB_1)))
c22 = (intD_1 == Not(Or(r,intC_1)))
c23 = Implies(Not(clk),(intC_1 == Not(intD_1)))
c24 = (g5 == Not(intC_1))

# DFF2 - G11 to G6
c25 = Implies(Not(clk),(intA_2 == Not(g11)))
c26 = (intB_2 == Not(Or(r,intA_2)))
c27 = Implies(clk,(intA_2 == Not(intB_2)))
c28 = Implies(clk,(intC_2 == Not(intB_2)))
c29 = (intD_2 == Not(Or(r,intC_2)))
c30 = Implies(Not(clk),(intC_2 == Not(intD_2)))
c31 = (g6 == Not(intC_2))


# Z3 Solver
s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31)

# Testing
#c32 = (r == False)      # No reset
#s.add(c32)
print(s.check())
print(s.model())