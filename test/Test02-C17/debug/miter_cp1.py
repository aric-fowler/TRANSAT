from z3 import *
set_param('verbose',10)


def main():
	pi1 = Bool('pi1')
	pi2 = Bool('pi2')
	pi3 = Bool('pi3')
	pi6 = Bool('pi6')
	pi7 = Bool('pi7')
	po23_m1 = Bool('po23_m1')
	po22_m1 = Bool('po22_m1')
	xor2_m1 = Bool('xor2_m1')
	int2_m1 = Int('int2_m1')
	and1_m1 = Bool('and1_m1')
	nand2_m1 = Bool('nand2_m1')
	xor1_m1 = Bool('xor1_m1')
	nand1_m1 = Bool('nand1_m1')
	xnor2_m1 = Bool('xnor2_m1')
	int3_m1 = Int('int3_m1')
	and2_m1 = Bool('and2_m1')
	nand3_m1 = Bool('nand3_m1')
	nand4_m1 = Bool('nand4_m1')
	xnor1_m1 = Bool('xnor1_m1')
	int1_m1 = Int('int1_m1')
	k0_1 = Bool('k0_1')
	k1_1 = Bool('k1_1')
	k3_1 = Bool('k3_1')
	k2_1 = Bool('k2_1')
	po23_m2 = Bool('po23_m2')
	po22_m2 = Bool('po22_m2')
	xor2_m2 = Bool('xor2_m2')
	int2_m2 = Int('int2_m2')
	and1_m2 = Bool('and1_m2')
	nand2_m2 = Bool('nand2_m2')
	xor1_m2 = Bool('xor1_m2')
	nand1_m2 = Bool('nand1_m2')
	xnor2_m2 = Bool('xnor2_m2')
	int3_m2 = Int('int3_m2')
	and2_m2 = Bool('and2_m2')
	nand3_m2 = Bool('nand3_m2')
	nand4_m2 = Bool('nand4_m2')
	xnor1_m2 = Bool('xnor1_m2')
	int1_m2 = Int('int1_m2')
	k0_2 = Bool('k0_2')
	k1_2 = Bool('k1_2')
	k3_2 = Bool('k3_2')
	k2_2 = Bool('k2_2')

	c0 = xnor1_m1 == Not(Xor(Not(pi7),k0_1))
	c1 = nand1_m1 == Not(And(pi1,pi3))
	c2 = nand2_m1 == Not(And(pi3,pi6))
	c3 = and1_m1 == And(xnor1_m1,nand2_m1)
	c4 = and2_m1 == And(nand2_m1,pi2)
	c5 = xnor2_m1 == Not(Xor(and2_m1,k1_1))
	c6 = xor2_m1 == Xor(k2_1,and1_m1)
	c7 = nand3_m1 == Not(And(nand1_m1,xnor2_m1))
	c8 = nand4_m1 == Not(And(xor2_m1,xnor2_m1))
	c9 = xor1_m1 == Xor(nand4_m1,k3_1)
	c10 = And((int3_m1 > int1_m1),(int3_m1 < int2_m1))
	c11 = nand3_m1 == po22_m1
	c12 = xor1_m1 == po23_m1
	c13 = xnor1_m2 == Not(Xor(Not(pi7),k0_2))
	c14 = nand1_m2 == Not(And(pi1,pi3))
	c15 = nand2_m2 == Not(And(pi3,pi6))
	c16 = and1_m2 == And(xnor1_m2,nand2_m2)
	c17 = and2_m2 == And(nand2_m2,pi2)
	c18 = xnor2_m2 == Not(Xor(and2_m2,k1_2))
	c19 = xor2_m2 == Xor(k2_2,and1_m2)
	c20 = nand3_m2 == Not(And(nand1_m2,xnor2_m2))
	c21 = nand4_m2 == Not(And(xor2_m2,xnor2_m2))
	c22 = xor1_m2 == Xor(nand4_m2,k3_2)
	c23 = And((int3_m2 > int1_m2),(int3_m2 < int2_m2))
	c24 = nand3_m2 == po22_m2
	c25 = xor1_m2 == po23_m2
	c26 = Or(Xor(po22_m1,po22_m2),Xor(po23_m1,po23_m2))     # Miter comparator

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26)
	with open('debug/miter_cp1.py.txt','w') as f:
		f.write(str(s.check())+'\n\n')
		try:
			for item in sorted([(d, s.model()[d]) for d in s.model()], key = lambda x: str(x[0])):
				f.write(str(item)+'\n')
		except:
			None
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()
