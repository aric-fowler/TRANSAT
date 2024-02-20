from z3 import *


def main():
	a = Bool('a')
	b = Bool('b')
	c = Bool('c')
	o_m1 = Bool('o_m1')
	n1_m1 = Bool('n1_m1')
	n0_m1 = Bool('n0_m1')
	n2_m1 = Bool('n2_m1')
	k5_1 = Bool('k5_1')
	k1_1 = Bool('k1_1')
	k7_1 = Bool('k7_1')
	k0_1 = Bool('k0_1')
	k3_1 = Bool('k3_1')
	k4_1 = Bool('k4_1')
	k6_1 = Bool('k6_1')
	k2_1 = Bool('k2_1')
	o_m2 = Bool('o_m2')
	n1_m2 = Bool('n1_m2')
	n0_m2 = Bool('n0_m2')
	n2_m2 = Bool('n2_m2')
	k5_2 = Bool('k5_2')
	k1_2 = Bool('k1_2')
	k7_2 = Bool('k7_2')
	k0_2 = Bool('k0_2')
	k3_2 = Bool('k3_2')
	k4_2 = Bool('k4_2')
	k6_2 = Bool('k6_2')
	k2_2 = Bool('k2_2')
	n1_cp1_1 = Bool('n1_cp1_1')
	n0_cp1_1 = Bool('n0_cp1_1')
	n2_cp1_1 = Bool('n2_cp1_1')
	a_cp1 = Bool('a_cp1')
	b_cp1 = Bool('b_cp1')
	c_cp1 = Bool('c_cp1')
	o_cp1 = Bool('o_cp1')
	n1_cp1_2 = Bool('n1_cp1_2')
	n0_cp1_2 = Bool('n0_cp1_2')
	n2_cp1_2 = Bool('n2_cp1_2')
	n1_cp2_1 = Bool('n1_cp2_1')
	n0_cp2_1 = Bool('n0_cp2_1')
	n2_cp2_1 = Bool('n2_cp2_1')
	a_cp2 = Bool('a_cp2')
	b_cp2 = Bool('b_cp2')
	c_cp2 = Bool('c_cp2')
	o_cp2 = Bool('o_cp2')
	n1_cp2_2 = Bool('n1_cp2_2')
	n0_cp2_2 = Bool('n0_cp2_2')
	n2_cp2_2 = Bool('n2_cp2_2')
	n1_cp3_1 = Bool('n1_cp3_1')
	n0_cp3_1 = Bool('n0_cp3_1')
	n2_cp3_1 = Bool('n2_cp3_1')
	a_cp3 = Bool('a_cp3')
	b_cp3 = Bool('b_cp3')
	c_cp3 = Bool('c_cp3')
	o_cp3 = Bool('o_cp3')
	n1_cp3_2 = Bool('n1_cp3_2')
	n0_cp3_2 = Bool('n0_cp3_2')
	n2_cp3_2 = Bool('n2_cp3_2')
	n1_cp4_1 = Bool('n1_cp4_1')
	n0_cp4_1 = Bool('n0_cp4_1')
	n2_cp4_1 = Bool('n2_cp4_1')
	a_cp4 = Bool('a_cp4')
	b_cp4 = Bool('b_cp4')
	c_cp4 = Bool('c_cp4')
	o_cp4 = Bool('o_cp4')
	n1_cp4_2 = Bool('n1_cp4_2')
	n0_cp4_2 = Bool('n0_cp4_2')
	n2_cp4_2 = Bool('n2_cp4_2')

	c0 = (n0_m1 == If(c,k1_1,k0_1))
	c1 = (n1_m1 == If(c,k3_1,k2_1))
	c2 = (n2_m1 == If(b,n1_m1,n0_m1))
	c3 = (o_m1 == Xor(a,Xor(n2_m1,Xor(k4_1,Xor(k5_1,Xor(k6_1,k7_1))))))
	c4 = (n0_m2 == If(c,k1_2,k0_2))
	c5 = (n1_m2 == If(c,k3_2,k2_2))
	c6 = (n2_m2 == If(b,n1_m2,n0_m2))
	c7 = (o_m2 == Xor(a,Xor(n2_m2,Xor(k4_2,Xor(k5_2,Xor(k6_2,k7_2))))))
	c8 = Or(Xor(o_m1,o_m2))     # Miter comparator
	c9 = (n0_cp1_1 == If(c_cp1,k1_1,k0_1))
	c10 = (n1_cp1_1 == If(c_cp1,k3_1,k2_1))
	c11 = (n2_cp1_1 == If(b_cp1,n1_cp1_1,n0_cp1_1))
	c12 = (o_cp1 == Xor(a_cp1,Xor(n2_cp1_1,Xor(k4_1,Xor(k5_1,Xor(k6_1,k7_1))))))
	c13 = (n0_cp1_2 == If(c_cp1,k1_2,k0_2))
	c14 = (n1_cp1_2 == If(c_cp1,k3_2,k2_2))
	c15 = (n2_cp1_2 == If(b_cp1,n1_cp1_2,n0_cp1_2))
	c16 = (o_cp1 == Xor(a_cp1,Xor(n2_cp1_2,Xor(k4_2,Xor(k5_2,Xor(k6_2,k7_2))))))
	c17 = a_cp1 == False
	c18 = b_cp1 == False
	c19 = c_cp1 == True
	c20 = o_cp1 == True
	c21 = (n0_cp2_1 == If(c_cp2,k1_1,k0_1))
	c22 = (n1_cp2_1 == If(c_cp2,k3_1,k2_1))
	c23 = (n2_cp2_1 == If(b_cp2,n1_cp2_1,n0_cp2_1))
	c24 = (o_cp2 == Xor(a_cp2,Xor(n2_cp2_1,Xor(k4_1,Xor(k5_1,Xor(k6_1,k7_1))))))
	c25 = (n0_cp2_2 == If(c_cp2,k1_2,k0_2))
	c26 = (n1_cp2_2 == If(c_cp2,k3_2,k2_2))
	c27 = (n2_cp2_2 == If(b_cp2,n1_cp2_2,n0_cp2_2))
	c28 = (o_cp2 == Xor(a_cp2,Xor(n2_cp2_2,Xor(k4_2,Xor(k5_2,Xor(k6_2,k7_2))))))
	c29 = a_cp2 == False
	c30 = b_cp2 == False
	c31 = c_cp2 == False
	c32 = o_cp2 == False
	c33 = (n0_cp3_1 == If(c_cp3,k1_1,k0_1))
	c34 = (n1_cp3_1 == If(c_cp3,k3_1,k2_1))
	c35 = (n2_cp3_1 == If(b_cp3,n1_cp3_1,n0_cp3_1))
	c36 = (o_cp3 == Xor(a_cp3,Xor(n2_cp3_1,Xor(k4_1,Xor(k5_1,Xor(k6_1,k7_1))))))
	c37 = (n0_cp3_2 == If(c_cp3,k1_2,k0_2))
	c38 = (n1_cp3_2 == If(c_cp3,k3_2,k2_2))
	c39 = (n2_cp3_2 == If(b_cp3,n1_cp3_2,n0_cp3_2))
	c40 = (o_cp3 == Xor(a_cp3,Xor(n2_cp3_2,Xor(k4_2,Xor(k5_2,Xor(k6_2,k7_2))))))
	c41 = a_cp3 == False
	c42 = b_cp3 == True
	c43 = c_cp3 == True
	c44 = o_cp3 == True
	c45 = (n0_cp4_1 == If(c_cp4,k1_1,k0_1))
	c46 = (n1_cp4_1 == If(c_cp4,k3_1,k2_1))
	c47 = (n2_cp4_1 == If(b_cp4,n1_cp4_1,n0_cp4_1))
	c48 = (o_cp4 == Xor(a_cp4,Xor(n2_cp4_1,Xor(k4_1,Xor(k5_1,Xor(k6_1,k7_1))))))
	c49 = (n0_cp4_2 == If(c_cp4,k1_2,k0_2))
	c50 = (n1_cp4_2 == If(c_cp4,k3_2,k2_2))
	c51 = (n2_cp4_2 == If(b_cp4,n1_cp4_2,n0_cp4_2))
	c52 = (o_cp4 == Xor(a_cp4,Xor(n2_cp4_2,Xor(k4_2,Xor(k5_2,Xor(k6_2,k7_2))))))
	c53 = a_cp4 == False
	c54 = b_cp4 == True
	c55 = c_cp4 == False
	c56 = o_cp4 == True

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()