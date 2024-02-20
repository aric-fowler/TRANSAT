from z3 import *


def main():
	a = Bool('a')
	b = Bool('b')
	c = Bool('c')
	o_m1 = Bool('o_m1')
	n_m1 = Bool('n_m1')
	o_m2 = Bool('o_m2')
	k1_m2 = Bool('k1_m2')
	k2_m2 = Bool('k2_m2')
	k5_m2 = Bool('k5_m2')
	k4_m2 = Bool('k4_m2')
	k6_m2 = Bool('k6_m2')
	k7_m2 = Bool('k7_m2')
	k3_m2 = Bool('k3_m2')
	k0_m2 = Bool('k0_m2')
	n2_m2 = Bool('n2_m2')
	n1_m2 = Bool('n1_m2')
	n0_m2 = Bool('n0_m2')

	c0 = (o_m1 == Xor(a,Or(b,c)))
	c1 = (n0_m2 == If(c,k1_m2,k0_m2))
	c2 = (n1_m2 == If(c,k3_m2,k2_m2))
	c3 = (n2_m2 == If(b,n1_m2,n0_m2))
	c4 = (o_m2 == Xor(a,Xor(n2_m2,Xor(k4_m2,Xor(k5_m2,Xor(k6_m2,k7_m2))))))
	c5 = k0_m2 == True
	c6 = k1_m2 == False
	c7 = k2_m2 == False
	c8 = k3_m2 == False
	c9 = k4_m2 == True
	c10 = k5_m2 == True
	c11 = k6_m2 == True
	c12 = k7_m2 == False
	c13 = Or(Xor(o_m1,o_m2))     # Miter circuit

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()