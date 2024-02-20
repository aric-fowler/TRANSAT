#!/usr/bin/env python3
from z3 import *

a = Bool('a')
b = Bool('b')
c = Bool('c')
o = Bool('o')
n = Bool('n')

c1 = (o == Xor(a,Or(b,c)))
