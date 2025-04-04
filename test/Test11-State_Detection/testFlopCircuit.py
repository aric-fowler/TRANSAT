#!/usr/bin/env python3
from z3 import *

# I/O
i0 = Bool('i0')
i1 = Bool('i1')
i2 = Bool('i2')
i3 = Bool('i3')
clk = Bool('clk')
r = Bool('r')
f = Bool('f')

# Internal nodes 
n0 = Bool('n0')
n1 = Bool('n1')
n2 = Bool('n2')
q = Bool('q')
intA = Bool('intA')
intB = Bool('intB')
intC = Bool('intC')
intD = Bool('intD')

# Combinational logic
c10 = (n0 == And(i0,i1))
c11 = (n1 == Or(i1,i2))
c12 = (n2 == And(n1,i3))
c13 = (f == Xor(q,n2))

# DFF architecture - rising edge, asynchronous active-high reset
c1 = Implies(Not(clk),(intA == Not(n0)))
c2 = (intB == Not(Or(r,intA)))
c3 = Implies(clk,(intA == Not(intB)))
c4 = Implies(clk,(intC == Not(intB)))
c5 = (intD == Not(Or(r,intC)))
c6 = Implies(Not(clk),(intC == Not(intD)))
c7 = (q == Not(intC))


# Testing
s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c7,c10,c11,c12,c13)

print(s.check())
print(s.model())