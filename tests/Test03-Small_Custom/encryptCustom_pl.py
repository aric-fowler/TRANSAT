'''
File containing encrypted custom circuit propositional logic in Z3's Python distribution syntax

Author:     Aric Fowler
Python:     3.10.6
Updated:    May 2023
'''
from z3 import *

# Circuit inputs
A = Bool('A')
B = Bool('B')
C = Bool('C')

# Key inputs
k1 = Bool('k1')
k2 = Bool('k2')
k3 = Bool('k3')
k4 = Bool('k4')

# Circuit outputs
O = Bool('O')

# Circuit nets
xnor1 = Bool('xnor1')
nand1 = Bool('nand1')
nand2 = Bool('nand2')
xnor2 = Bool('xnor2')
nand3 = Bool('nand3')
xor1 = Bool('xor1')

# Circuit description (PL clauses)
c1 = nand1 == Not(And(k1,A))
c2 = nand2 == Not(And(B,C))
c3 = xor1 == Xor(k2,nand1)
c4 = xnor1 == Not(Xor(nand2,k3))
c5 = nand3 == Not(And(xor1,xnor1))
c6 = xnor2 == Not(Xor(nand3,k4))

# Output clauses
c_O = O == xnor2

# Add model to solver
s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c_O)

print(s.check())
print(s.model())
