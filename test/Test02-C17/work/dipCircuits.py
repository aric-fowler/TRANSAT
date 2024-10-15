from z3 import *


def main():
	k0 = Bool('k0')
	k1 = Bool('k1')
	k2 = Bool('k2')
	k3 = Bool('k3')
	pi6_cp1 = Bool('pi6_cp1')
	pi7_cp1 = Bool('pi7_cp1')
	pi2_cp1 = Bool('pi2_cp1')
	pi1_cp1 = Bool('pi1_cp1')
	pi3_cp1 = Bool('pi3_cp1')
	po23_cp1 = Bool('po23_cp1')
	po22_cp1 = Bool('po22_cp1')
	xor2_cp1 = Bool('xor2_cp1')
	int2_cp1 = Int('int2_cp1')
	and1_cp1 = Bool('and1_cp1')
	nand2_cp1 = Bool('nand2_cp1')
	xor1_cp1 = Bool('xor1_cp1')
	nand1_cp1 = Bool('nand1_cp1')
	xnor2_cp1 = Bool('xnor2_cp1')
	int3_cp1 = Int('int3_cp1')
	and2_cp1 = Bool('and2_cp1')
	nand3_cp1 = Bool('nand3_cp1')
	nand4_cp1 = Bool('nand4_cp1')
	xnor1_cp1 = Bool('xnor1_cp1')
	int1_cp1 = Int('int1_cp1')
	pi6_cp2 = Bool('pi6_cp2')
	pi7_cp2 = Bool('pi7_cp2')
	pi2_cp2 = Bool('pi2_cp2')
	pi1_cp2 = Bool('pi1_cp2')
	pi3_cp2 = Bool('pi3_cp2')
	po23_cp2 = Bool('po23_cp2')
	po22_cp2 = Bool('po22_cp2')
	xor2_cp2 = Bool('xor2_cp2')
	int2_cp2 = Int('int2_cp2')
	and1_cp2 = Bool('and1_cp2')
	nand2_cp2 = Bool('nand2_cp2')
	xor1_cp2 = Bool('xor1_cp2')
	nand1_cp2 = Bool('nand1_cp2')
	xnor2_cp2 = Bool('xnor2_cp2')
	int3_cp2 = Int('int3_cp2')
	and2_cp2 = Bool('and2_cp2')
	nand3_cp2 = Bool('nand3_cp2')
	nand4_cp2 = Bool('nand4_cp2')
	xnor1_cp2 = Bool('xnor1_cp2')
	int1_cp2 = Int('int1_cp2')
	pi6_cp3 = Bool('pi6_cp3')
	pi7_cp3 = Bool('pi7_cp3')
	pi2_cp3 = Bool('pi2_cp3')
	pi1_cp3 = Bool('pi1_cp3')
	pi3_cp3 = Bool('pi3_cp3')
	po23_cp3 = Bool('po23_cp3')
	po22_cp3 = Bool('po22_cp3')
	xor2_cp3 = Bool('xor2_cp3')
	int2_cp3 = Int('int2_cp3')
	and1_cp3 = Bool('and1_cp3')
	nand2_cp3 = Bool('nand2_cp3')
	xor1_cp3 = Bool('xor1_cp3')
	nand1_cp3 = Bool('nand1_cp3')
	xnor2_cp3 = Bool('xnor2_cp3')
	int3_cp3 = Int('int3_cp3')
	and2_cp3 = Bool('and2_cp3')
	nand3_cp3 = Bool('nand3_cp3')
	nand4_cp3 = Bool('nand4_cp3')
	xnor1_cp3 = Bool('xnor1_cp3')
	int1_cp3 = Int('int1_cp3')

	c0 = xnor1_cp1 == Not(Xor(Not(pi7_cp1),k0))
	c1 = nand1_cp1 == Not(And(pi1_cp1,pi3_cp1))
	c2 = nand2_cp1 == Not(And(pi3_cp1,pi6_cp1))
	c3 = and1_cp1 == And(xnor1_cp1,nand2_cp1)
	c4 = and2_cp1 == And(nand2_cp1,pi2_cp1)
	c5 = xnor2_cp1 == Not(Xor(and2_cp1,k1))
	c6 = xor2_cp1 == Xor(k2,and1_cp1)
	c7 = nand3_cp1 == Not(And(nand1_cp1,xnor2_cp1))
	c8 = nand4_cp1 == Not(And(xor2_cp1,xnor2_cp1))
	c9 = xor1_cp1 == Xor(nand4_cp1,k3)
	c10 = And((int3_cp1 > int1_cp1),(int3_cp1 < int2_cp1))
	c11 = nand3_cp1 == po22_cp1
	c12 = xor1_cp1 == po23_cp1
	c13 = pi1_cp1 == False
	c14 = pi2_cp1 == True
	c15 = pi3_cp1 == True
	c16 = pi6_cp1 == True
	c17 = pi7_cp1 == False
	c18 = po22_cp1 == False
	c19 = po23_cp1 == False
	c20 = xnor1_cp2 == Not(Xor(Not(pi7_cp2),k0))
	c21 = nand1_cp2 == Not(And(pi1_cp2,pi3_cp2))
	c22 = nand2_cp2 == Not(And(pi3_cp2,pi6_cp2))
	c23 = and1_cp2 == And(xnor1_cp2,nand2_cp2)
	c24 = and2_cp2 == And(nand2_cp2,pi2_cp2)
	c25 = xnor2_cp2 == Not(Xor(and2_cp2,k1))
	c26 = xor2_cp2 == Xor(k2,and1_cp2)
	c27 = nand3_cp2 == Not(And(nand1_cp2,xnor2_cp2))
	c28 = nand4_cp2 == Not(And(xor2_cp2,xnor2_cp2))
	c29 = xor1_cp2 == Xor(nand4_cp2,k3)
	c30 = And((int3_cp2 > int1_cp2),(int3_cp2 < int2_cp2))
	c31 = nand3_cp2 == po22_cp2
	c32 = xor1_cp2 == po23_cp2
	c33 = pi1_cp2 == True
	c34 = pi2_cp2 == False
	c35 = pi3_cp2 == False
	c36 = pi6_cp2 == True
	c37 = pi7_cp2 == False
	c38 = po22_cp2 == False
	c39 = po23_cp2 == False
	c40 = xnor1_cp3 == Not(Xor(Not(pi7_cp3),k0))
	c41 = nand1_cp3 == Not(And(pi1_cp3,pi3_cp3))
	c42 = nand2_cp3 == Not(And(pi3_cp3,pi6_cp3))
	c43 = and1_cp3 == And(xnor1_cp3,nand2_cp3)
	c44 = and2_cp3 == And(nand2_cp3,pi2_cp3)
	c45 = xnor2_cp3 == Not(Xor(and2_cp3,k1))
	c46 = xor2_cp3 == Xor(k2,and1_cp3)
	c47 = nand3_cp3 == Not(And(nand1_cp3,xnor2_cp3))
	c48 = nand4_cp3 == Not(And(xor2_cp3,xnor2_cp3))
	c49 = xor1_cp3 == Xor(nand4_cp3,k3)
	c50 = And((int3_cp3 > int1_cp3),(int3_cp3 < int2_cp3))
	c51 = nand3_cp3 == po22_cp3
	c52 = xor1_cp3 == po23_cp3
	c53 = pi1_cp3 == True
	c54 = pi2_cp3 == True
	c55 = pi3_cp3 == False
	c56 = pi6_cp3 == True
	c57 = pi7_cp3 == False
	c58 = po22_cp3 == True
	c59 = po23_cp3 == True

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()
