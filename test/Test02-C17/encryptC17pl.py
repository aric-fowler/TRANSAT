#!/usr/bin/env python3
'''
File containing encrypted C17 propositional logic in Z3's Python distribution syntax

Python:     3.10.6
Updated:    Apr 2023
'''
from z3 import *

# Circuit inputs
pi1 = Bool('pi1')
pi2 = Bool('pi2')
pi3 = Bool('pi3')
pi6 = Bool('pi6')
pi7 = Bool('pi7')

# Key inputs
k0 = Bool('k0')
k1 = Bool('k1')
k2 = Bool('k2')
k3 = Bool('k3')

# Circuit outputs
po22 = Bool('po22')
po23 = Bool('po23')

# Circuit nets
xnor1 = Bool('xnor1')
nand1 = Bool('nand1')
nand2 = Bool('nand2')
and1 = Bool('and1')
and2 = Bool('and2')
xnor2 = Bool('xnor2')
xor2 = Bool('xor2')
nand3 = Bool('nand3')
nand4 = Bool('nand4')
xor1 = Bool('xor1')

# Extra arbitrary goodies to ensure that integers are working
int1 = Int('int1')
int2 = Int('int2')
int3 = Int('int3')

# Circuit description (PL clauses)
c1 = xnor1 == Not(Xor(Not(pi7),k0))
c2 = nand1 == Not(And(pi1,pi3))
c3 = nand2 == Not(And(pi3,pi6))
c4 = and1 == And(xnor1,nand2)
c5 = and2 == And(nand2,pi2)
c6 = xnor2 == Not(Xor(and2,k1))
c7 = xor2 == Xor(k2,and1)
c8 = nand3 == Not(And(nand1,xnor2))
c9 = nand4 == Not(And(xor2,xnor2))
c10 = xor1 == Xor(nand4,k3)
c11 = And((int3 > int1),(int3 < int2))

# Output clauses
c_po22 = nand3 == po22
c_po23 = xor1 == po23

# Add model to solver
s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c_po22,c_po23)

print(s.check())
print(s.model())
