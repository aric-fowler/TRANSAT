from z3 import *


def main():
	pi1 = Bool('pi1')
	pi2 = Bool('pi2')
	pi3 = Bool('pi3')
	pi6 = Bool('pi6')
	pi7 = Bool('pi7')
	po23_m1 = Bool('po23_m1')
	po22_m1 = Bool('po22_m1')
	nand3_m1 = Bool('nand3_m1')
	nand2_m1 = Bool('nand2_m1')
	nand1_m1 = Bool('nand1_m1')
	nand4_m1 = Bool('nand4_m1')
	nand6_m1 = Bool('nand6_m1')
	nand5_m1 = Bool('nand5_m1')
	po23_m2 = Bool('po23_m2')
	po22_m2 = Bool('po22_m2')
	k3_m2 = Bool('k3_m2')
	k1_m2 = Bool('k1_m2')
	k2_m2 = Bool('k2_m2')
	k0_m2 = Bool('k0_m2')
	nand3_m2 = Bool('nand3_m2')
	int2_m2 = Int('int2_m2')
	nand2_m2 = Bool('nand2_m2')
	int3_m2 = Int('int3_m2')
	nand1_m2 = Bool('nand1_m2')
	xnor1_m2 = Bool('xnor1_m2')
	xor2_m2 = Bool('xor2_m2')
	xor1_m2 = Bool('xor1_m2')
	int1_m2 = Int('int1_m2')
	and1_m2 = Bool('and1_m2')
	xnor2_m2 = Bool('xnor2_m2')
	nand4_m2 = Bool('nand4_m2')
	and2_m2 = Bool('and2_m2')

	c0 = nand1_m1 == Not(And(pi1,pi3))
	c1 = nand2_m1 == Not(And(pi3,pi6))
	c2 = nand3_m1 == Not(And(nand1_m1,nand6_m1))
	c3 = nand4_m1 == Not(And(nand6_m1,nand5_m1))
	c4 = nand5_m1 == Not(And(nand2_m1,pi7))
	c5 = nand6_m1 == Not(And(nand2_m1,pi2))
	c6 = nand3_m1 == po22_m1
	c7 = nand4_m1 == po23_m1
	c8 = xnor1_m2 == Not(Xor(Not(pi7),k0_m2))
	c9 = nand1_m2 == Not(And(pi1,pi3))
	c10 = nand2_m2 == Not(And(pi3,pi6))
	c11 = and1_m2 == And(xnor1_m2,nand2_m2)
	c12 = and2_m2 == And(nand2_m2,pi2)
	c13 = xnor2_m2 == Not(Xor(and2_m2,k1_m2))
	c14 = xor2_m2 == Xor(k2_m2,and1_m2)
	c15 = nand3_m2 == Not(And(nand1_m2,xnor2_m2))
	c16 = nand4_m2 == Not(And(xor2_m2,xnor2_m2))
	c17 = xor1_m2 == Xor(nand4_m2,k3_m2)
	c18 = And((int3_m2 > int1_m2),(int3_m2 < int2_m2))
	c19 = nand3_m2 == po22_m2
	c20 = xor1_m2 == po23_m2
	c21 = k0_m2 == False
	c22 = k1_m2 == False
	c23 = k2_m2 == True
	c24 = k3_m2 == False
	c25 = Or(Xor(po22_m1,po22_m2),Xor(po23_m1,po23_m2))     # Miter circuit

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()