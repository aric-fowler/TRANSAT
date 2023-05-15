from z3 import *


def main():
	k0 = Bool('k0')
	k1 = Bool('k1')
	k2 = Bool('k2')
	k3 = Bool('k3')
	pi1_cp1 = Bool('pi1_cp1')
	pi3_cp1 = Bool('pi3_cp1')
	pi2_cp1 = Bool('pi2_cp1')
	pi6_cp1 = Bool('pi6_cp1')
	pi7_cp1 = Bool('pi7_cp1')
	po23_cp1 = Bool('po23_cp1')
	po22_cp1 = Bool('po22_cp1')
	and2_cp1 = Bool('and2_cp1')
	xor2_cp1 = Bool('xor2_cp1')
	xnor1_cp1 = Bool('xnor1_cp1')
	nand3_cp1 = Bool('nand3_cp1')
	nand4_cp1 = Bool('nand4_cp1')
	nand1_cp1 = Bool('nand1_cp1')
	xnor2_cp1 = Bool('xnor2_cp1')
	and1_cp1 = Bool('and1_cp1')
	xor1_cp1 = Bool('xor1_cp1')
	nand2_cp1 = Bool('nand2_cp1')

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
	c10 = nand3_cp1 == po22_cp1 
	c11 = xor1_cp1 == po23_cp1 
	c12 = pi1_cp1 == False 
	c13 = pi3_cp1 == False 
	c14 = pi2_cp1 == False 
	c15 = pi6_cp1 == False 
	c16 = pi7_cp1 == True 
	c17 = po22_cp1 == False 
	c18 = po23_cp1 == True 

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()