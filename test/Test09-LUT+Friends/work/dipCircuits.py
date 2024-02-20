from z3 import *


def main():
	k0 = Bool('k0')
	k1 = Bool('k1')
	k2 = Bool('k2')
	k3 = Bool('k3')
	k4 = Bool('k4')
	k5 = Bool('k5')
	k6 = Bool('k6')
	k7 = Bool('k7')
	a_cp1 = Bool('a_cp1')
	b_cp1 = Bool('b_cp1')
	c_cp1 = Bool('c_cp1')
	o_cp1 = Bool('o_cp1')
	n1_cp1 = Bool('n1_cp1')
	n0_cp1 = Bool('n0_cp1')
	n2_cp1 = Bool('n2_cp1')
	a_cp2 = Bool('a_cp2')
	b_cp2 = Bool('b_cp2')
	c_cp2 = Bool('c_cp2')
	o_cp2 = Bool('o_cp2')
	n1_cp2 = Bool('n1_cp2')
	n0_cp2 = Bool('n0_cp2')
	n2_cp2 = Bool('n2_cp2')
	a_cp3 = Bool('a_cp3')
	b_cp3 = Bool('b_cp3')
	c_cp3 = Bool('c_cp3')
	o_cp3 = Bool('o_cp3')
	n1_cp3 = Bool('n1_cp3')
	n0_cp3 = Bool('n0_cp3')
	n2_cp3 = Bool('n2_cp3')
	a_cp4 = Bool('a_cp4')
	b_cp4 = Bool('b_cp4')
	c_cp4 = Bool('c_cp4')
	o_cp4 = Bool('o_cp4')
	n1_cp4 = Bool('n1_cp4')
	n0_cp4 = Bool('n0_cp4')
	n2_cp4 = Bool('n2_cp4')

	c0 = (n0_cp1 == If(c_cp1,k1,k0))
	c1 = (n1_cp1 == If(c_cp1,k3,k2))
	c2 = (n2_cp1 == If(b_cp1,n1_cp1,n0_cp1))
	c3 = (o_cp1 == Xor(a_cp1,Xor(n2_cp1,Xor(k4,Xor(k5,Xor(k6,k7))))))
	c4 = a_cp1 == False
	c5 = b_cp1 == False
	c6 = c_cp1 == True
	c7 = o_cp1 == True
	c8 = (n0_cp2 == If(c_cp2,k1,k0))
	c9 = (n1_cp2 == If(c_cp2,k3,k2))
	c10 = (n2_cp2 == If(b_cp2,n1_cp2,n0_cp2))
	c11 = (o_cp2 == Xor(a_cp2,Xor(n2_cp2,Xor(k4,Xor(k5,Xor(k6,k7))))))
	c12 = a_cp2 == False
	c13 = b_cp2 == False
	c14 = c_cp2 == False
	c15 = o_cp2 == False
	c16 = (n0_cp3 == If(c_cp3,k1,k0))
	c17 = (n1_cp3 == If(c_cp3,k3,k2))
	c18 = (n2_cp3 == If(b_cp3,n1_cp3,n0_cp3))
	c19 = (o_cp3 == Xor(a_cp3,Xor(n2_cp3,Xor(k4,Xor(k5,Xor(k6,k7))))))
	c20 = a_cp3 == False
	c21 = b_cp3 == True
	c22 = c_cp3 == True
	c23 = o_cp3 == True
	c24 = (n0_cp4 == If(c_cp4,k1,k0))
	c25 = (n1_cp4 == If(c_cp4,k3,k2))
	c26 = (n2_cp4 == If(b_cp4,n1_cp4,n0_cp4))
	c27 = (o_cp4 == Xor(a_cp4,Xor(n2_cp4,Xor(k4,Xor(k5,Xor(k6,k7))))))
	c28 = a_cp4 == False
	c29 = b_cp4 == True
	c30 = c_cp4 == False
	c31 = o_cp4 == True

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()