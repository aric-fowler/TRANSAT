'''
File containing a simple SR latch, capable of holding state

Author:     Aric Fowler
Python:     3.10.12
Updated:    Apr 2024
'''
from z3 import *

in1 = Bool('in1')
in2 = Bool('in2')
R = Bool('R')
Q = Bool('Q')
nQ = Bool('nQ')
out = Bool('out')

c1 = (out == And(Q,in2))
c2 = (Q == Not(Or(R,nQ)))
c3 = (nQ == Not(Or(in1,Q)))

S = Solver()
S.add(c1,c2,c3)

print(S.check())
try:
    print(S.model())
except:
    print('Model unsolvable')