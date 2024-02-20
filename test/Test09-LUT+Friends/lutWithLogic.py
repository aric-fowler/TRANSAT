#!/usr/bin/env python3

from z3 import *

# Inputs, keys, outputs, nets
a = Bool('a')
b = Bool('b')
c = Bool('c')
k0 = Bool('k0')
k1 = Bool('k1')
k2 = Bool('k2')
k3 = Bool('k3')
k4 = Bool('k4')
k5 = Bool('k5')
k6 = Bool('k6')
k7 = Bool('k7')
o = Bool('o')
n0 = Bool('n0')
n1 = Bool('n1')
n2 = Bool('n2')

c1 = (n0 == If(c,k1,k0))
c2 = (n1 == If(c,k3,k2))
c3 = (n2 == If(b,n1,n0))
c4 = (o == Xor(a,Xor(n2,Xor(k4,Xor(k5,Xor(k6,k7))))))

s = Solver()
s.add(c1,c2,c3,c4)
print(s.check())