#!/usr/bin/env python3
from z3 import *

# I/O
d = Bool('d')
r = Bool('r')
clk = Bool('clk')
q = Bool('q')

# Internal nodes - intSt is the internal state
intA = Bool('intA')
intB = Bool('intB')
intC = Bool('intC')
intD = Bool('intD')

# DFF architecture - rising edge, asynchronous active-high reset
c1 = Implies(Not(clk),(intA == Not(d)))
c2 = (intB == Not(Or(r,intA)))
c3 = Implies(clk,(intA == Not(intB)))
c4 = Implies(clk,(intC == Not(intB)))
c5 = (intD == Not(Or(r,intC)))
c6 = Implies(Not(clk),(intC == Not(intD)))
c7 = (q == Not(intC))

# Testing
#c8 = (d == q)               # Feedback loop shouldn't prevent SAT decision since device is opaque (will fail when searching for state nets since d is input and q is output)

# Z3 solver
s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c7)

print(s.check())
print(s.model())