from z3 import *


def main():
	k1 = Bool('k1')
	k2 = Bool('k2')
	k3 = Bool('k3')
	k4 = Bool('k4')
	C_cp1 = Bool('C_cp1')
	A_cp1 = Bool('A_cp1')
	B_cp1 = Bool('B_cp1')
	O_cp1 = Bool('O_cp1')
	xor1_cp1 = Bool('xor1_cp1')
	nand3_cp1 = Bool('nand3_cp1')
	nand2_cp1 = Bool('nand2_cp1')
	nand1_cp1 = Bool('nand1_cp1')
	xnor1_cp1 = Bool('xnor1_cp1')
	xnor2_cp1 = Bool('xnor2_cp1')
	C_cp2 = Bool('C_cp2')
	A_cp2 = Bool('A_cp2')
	B_cp2 = Bool('B_cp2')
	O_cp2 = Bool('O_cp2')
	xor1_cp2 = Bool('xor1_cp2')
	nand3_cp2 = Bool('nand3_cp2')
	nand2_cp2 = Bool('nand2_cp2')
	nand1_cp2 = Bool('nand1_cp2')
	xnor1_cp2 = Bool('xnor1_cp2')
	xnor2_cp2 = Bool('xnor2_cp2')
	C_cp3 = Bool('C_cp3')
	A_cp3 = Bool('A_cp3')
	B_cp3 = Bool('B_cp3')
	O_cp3 = Bool('O_cp3')
	xor1_cp3 = Bool('xor1_cp3')
	nand3_cp3 = Bool('nand3_cp3')
	nand2_cp3 = Bool('nand2_cp3')
	nand1_cp3 = Bool('nand1_cp3')
	xnor1_cp3 = Bool('xnor1_cp3')
	xnor2_cp3 = Bool('xnor2_cp3')
	C_cp4 = Bool('C_cp4')
	A_cp4 = Bool('A_cp4')
	B_cp4 = Bool('B_cp4')
	O_cp4 = Bool('O_cp4')
	xor1_cp4 = Bool('xor1_cp4')
	nand3_cp4 = Bool('nand3_cp4')
	nand2_cp4 = Bool('nand2_cp4')
	nand1_cp4 = Bool('nand1_cp4')
	xnor1_cp4 = Bool('xnor1_cp4')
	xnor2_cp4 = Bool('xnor2_cp4')

	c0 = nand1_cp1 == Not(And(k1,A_cp1))    
	c1 = nand2_cp1 == Not(And(B_cp1,C_cp1))    
	c2 = xor1_cp1 == Xor(k2,nand1_cp1)    
	c3 = xnor1_cp1 == Not(Xor(nand2_cp1,k3))    
	c4 = nand3_cp1 == Not(And(xor1_cp1,xnor1_cp1))    
	c5 = xnor2_cp1 == Not(Xor(nand3_cp1,k4))    
	c6 = O_cp1 == xnor2_cp1    
	c7 = C_cp1 == False    
	c8 = A_cp1 == True    
	c9 = B_cp1 == False    
	c10 = O_cp1 == False    
	c11 = nand1_cp2 == Not(And(k1,A_cp2))   
	c12 = nand2_cp2 == Not(And(B_cp2,C_cp2))   
	c13 = xor1_cp2 == Xor(k2,nand1_cp2)   
	c14 = xnor1_cp2 == Not(Xor(nand2_cp2,k3))   
	c15 = nand3_cp2 == Not(And(xor1_cp2,xnor1_cp2))   
	c16 = xnor2_cp2 == Not(Xor(nand3_cp2,k4))   
	c17 = O_cp2 == xnor2_cp2   
	c18 = C_cp2 == True   
	c19 = A_cp2 == True   
	c20 = B_cp2 == True   
	c21 = O_cp2 == True   
	c22 = nand1_cp3 == Not(And(k1,A_cp3))  
	c23 = nand2_cp3 == Not(And(B_cp3,C_cp3))  
	c24 = xor1_cp3 == Xor(k2,nand1_cp3)  
	c25 = xnor1_cp3 == Not(Xor(nand2_cp3,k3))  
	c26 = nand3_cp3 == Not(And(xor1_cp3,xnor1_cp3))  
	c27 = xnor2_cp3 == Not(Xor(nand3_cp3,k4))  
	c28 = O_cp3 == xnor2_cp3  
	c29 = C_cp3 == True  
	c30 = A_cp3 == False  
	c31 = B_cp3 == True  
	c32 = O_cp3 == True  
	c33 = nand1_cp4 == Not(And(k1,A_cp4)) 
	c34 = nand2_cp4 == Not(And(B_cp4,C_cp4)) 
	c35 = xor1_cp4 == Xor(k2,nand1_cp4) 
	c36 = xnor1_cp4 == Not(Xor(nand2_cp4,k3)) 
	c37 = nand3_cp4 == Not(And(xor1_cp4,xnor1_cp4)) 
	c38 = xnor2_cp4 == Not(Xor(nand3_cp4,k4)) 
	c39 = O_cp4 == xnor2_cp4 
	c40 = C_cp4 == False 
	c41 = A_cp4 == False 
	c42 = B_cp4 == False 
	c43 = O_cp4 == True 

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()