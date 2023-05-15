from z3 import *


def main():
	A = Bool('A')
	B = Bool('B')
	C = Bool('C')
	O_m1 = Bool('O_m1')
	xor1_m1 = Bool('xor1_m1')
	nand3_m1 = Bool('nand3_m1')
	nand2_m1 = Bool('nand2_m1')
	nand1_m1 = Bool('nand1_m1')
	xnor1_m1 = Bool('xnor1_m1')
	xnor2_m1 = Bool('xnor2_m1')
	k4_1 = Bool('k4_1')
	k3_1 = Bool('k3_1')
	k1_1 = Bool('k1_1')
	k2_1 = Bool('k2_1')
	O_m2 = Bool('O_m2')
	xor1_m2 = Bool('xor1_m2')
	nand3_m2 = Bool('nand3_m2')
	nand2_m2 = Bool('nand2_m2')
	nand1_m2 = Bool('nand1_m2')
	xnor1_m2 = Bool('xnor1_m2')
	xnor2_m2 = Bool('xnor2_m2')
	k4_2 = Bool('k4_2')
	k3_2 = Bool('k3_2')
	k1_2 = Bool('k1_2')
	k2_2 = Bool('k2_2')
	xor1_cp1_1 = Bool('xor1_cp1_1')
	nand3_cp1_1 = Bool('nand3_cp1_1')
	nand2_cp1_1 = Bool('nand2_cp1_1')
	nand1_cp1_1 = Bool('nand1_cp1_1')
	xnor1_cp1_1 = Bool('xnor1_cp1_1')
	xnor2_cp1_1 = Bool('xnor2_cp1_1')
	C_cp1 = Bool('C_cp1')
	A_cp1 = Bool('A_cp1')
	B_cp1 = Bool('B_cp1')
	O_cp1 = Bool('O_cp1')
	xor1_cp1_2 = Bool('xor1_cp1_2')
	nand3_cp1_2 = Bool('nand3_cp1_2')
	nand2_cp1_2 = Bool('nand2_cp1_2')
	nand1_cp1_2 = Bool('nand1_cp1_2')
	xnor1_cp1_2 = Bool('xnor1_cp1_2')
	xnor2_cp1_2 = Bool('xnor2_cp1_2')
	xor1_cp2_1 = Bool('xor1_cp2_1')
	nand3_cp2_1 = Bool('nand3_cp2_1')
	nand2_cp2_1 = Bool('nand2_cp2_1')
	nand1_cp2_1 = Bool('nand1_cp2_1')
	xnor1_cp2_1 = Bool('xnor1_cp2_1')
	xnor2_cp2_1 = Bool('xnor2_cp2_1')
	C_cp2 = Bool('C_cp2')
	A_cp2 = Bool('A_cp2')
	B_cp2 = Bool('B_cp2')
	O_cp2 = Bool('O_cp2')
	xor1_cp2_2 = Bool('xor1_cp2_2')
	nand3_cp2_2 = Bool('nand3_cp2_2')
	nand2_cp2_2 = Bool('nand2_cp2_2')
	nand1_cp2_2 = Bool('nand1_cp2_2')
	xnor1_cp2_2 = Bool('xnor1_cp2_2')
	xnor2_cp2_2 = Bool('xnor2_cp2_2')
	xor1_cp3_1 = Bool('xor1_cp3_1')
	nand3_cp3_1 = Bool('nand3_cp3_1')
	nand2_cp3_1 = Bool('nand2_cp3_1')
	nand1_cp3_1 = Bool('nand1_cp3_1')
	xnor1_cp3_1 = Bool('xnor1_cp3_1')
	xnor2_cp3_1 = Bool('xnor2_cp3_1')
	C_cp3 = Bool('C_cp3')
	A_cp3 = Bool('A_cp3')
	B_cp3 = Bool('B_cp3')
	O_cp3 = Bool('O_cp3')
	xor1_cp3_2 = Bool('xor1_cp3_2')
	nand3_cp3_2 = Bool('nand3_cp3_2')
	nand2_cp3_2 = Bool('nand2_cp3_2')
	nand1_cp3_2 = Bool('nand1_cp3_2')
	xnor1_cp3_2 = Bool('xnor1_cp3_2')
	xnor2_cp3_2 = Bool('xnor2_cp3_2')
	xor1_cp4_1 = Bool('xor1_cp4_1')
	nand3_cp4_1 = Bool('nand3_cp4_1')
	nand2_cp4_1 = Bool('nand2_cp4_1')
	nand1_cp4_1 = Bool('nand1_cp4_1')
	xnor1_cp4_1 = Bool('xnor1_cp4_1')
	xnor2_cp4_1 = Bool('xnor2_cp4_1')
	C_cp4 = Bool('C_cp4')
	A_cp4 = Bool('A_cp4')
	B_cp4 = Bool('B_cp4')
	O_cp4 = Bool('O_cp4')
	xor1_cp4_2 = Bool('xor1_cp4_2')
	nand3_cp4_2 = Bool('nand3_cp4_2')
	nand2_cp4_2 = Bool('nand2_cp4_2')
	nand1_cp4_2 = Bool('nand1_cp4_2')
	xnor1_cp4_2 = Bool('xnor1_cp4_2')
	xnor2_cp4_2 = Bool('xnor2_cp4_2')

	c0 = nand1_m1 == Not(And(k1_1,A))     
	c1 = nand2_m1 == Not(And(B,C))     
	c2 = xor1_m1 == Xor(k2_1,nand1_m1)     
	c3 = xnor1_m1 == Not(Xor(nand2_m1,k3_1))     
	c4 = nand3_m1 == Not(And(xor1_m1,xnor1_m1))     
	c5 = xnor2_m1 == Not(Xor(nand3_m1,k4_1))     
	c6 = O_m1 == xnor2_m1     
	c7 = nand1_m2 == Not(And(k1_2,A))     
	c8 = nand2_m2 == Not(And(B,C))     
	c9 = xor1_m2 == Xor(k2_2,nand1_m2)     
	c10 = xnor1_m2 == Not(Xor(nand2_m2,k3_2))     
	c11 = nand3_m2 == Not(And(xor1_m2,xnor1_m2))     
	c12 = xnor2_m2 == Not(Xor(nand3_m2,k4_2))     
	c13 = O_m2 == xnor2_m2     
	c14 = O_m1 == Not(O_m2)     
	c15 = nand1_cp1_1 == Not(And(k1_1,A_cp1))    
	c16 = nand2_cp1_1 == Not(And(B_cp1,C_cp1))    
	c17 = xor1_cp1_1 == Xor(k2_1,nand1_cp1_1)    
	c18 = xnor1_cp1_1 == Not(Xor(nand2_cp1_1,k3_1))    
	c19 = nand3_cp1_1 == Not(And(xor1_cp1_1,xnor1_cp1_1))    
	c20 = xnor2_cp1_1 == Not(Xor(nand3_cp1_1,k4_1))    
	c21 = O_cp1 == xnor2_cp1_1    
	c22 = nand1_cp1_2 == Not(And(k1_2,A_cp1))    
	c23 = nand2_cp1_2 == Not(And(B_cp1,C_cp1))    
	c24 = xor1_cp1_2 == Xor(k2_2,nand1_cp1_2)    
	c25 = xnor1_cp1_2 == Not(Xor(nand2_cp1_2,k3_2))    
	c26 = nand3_cp1_2 == Not(And(xor1_cp1_2,xnor1_cp1_2))    
	c27 = xnor2_cp1_2 == Not(Xor(nand3_cp1_2,k4_2))    
	c28 = O_cp1 == xnor2_cp1_2    
	c29 = C_cp1 == False    
	c30 = A_cp1 == True    
	c31 = B_cp1 == False    
	c32 = O_cp1 == False    
	c33 = nand1_cp2_1 == Not(And(k1_1,A_cp2))   
	c34 = nand2_cp2_1 == Not(And(B_cp2,C_cp2))   
	c35 = xor1_cp2_1 == Xor(k2_1,nand1_cp2_1)   
	c36 = xnor1_cp2_1 == Not(Xor(nand2_cp2_1,k3_1))   
	c37 = nand3_cp2_1 == Not(And(xor1_cp2_1,xnor1_cp2_1))   
	c38 = xnor2_cp2_1 == Not(Xor(nand3_cp2_1,k4_1))   
	c39 = O_cp2 == xnor2_cp2_1   
	c40 = nand1_cp2_2 == Not(And(k1_2,A_cp2))   
	c41 = nand2_cp2_2 == Not(And(B_cp2,C_cp2))   
	c42 = xor1_cp2_2 == Xor(k2_2,nand1_cp2_2)   
	c43 = xnor1_cp2_2 == Not(Xor(nand2_cp2_2,k3_2))   
	c44 = nand3_cp2_2 == Not(And(xor1_cp2_2,xnor1_cp2_2))   
	c45 = xnor2_cp2_2 == Not(Xor(nand3_cp2_2,k4_2))   
	c46 = O_cp2 == xnor2_cp2_2   
	c47 = C_cp2 == True   
	c48 = A_cp2 == True   
	c49 = B_cp2 == True   
	c50 = O_cp2 == True   
	c51 = nand1_cp3_1 == Not(And(k1_1,A_cp3))  
	c52 = nand2_cp3_1 == Not(And(B_cp3,C_cp3))  
	c53 = xor1_cp3_1 == Xor(k2_1,nand1_cp3_1)  
	c54 = xnor1_cp3_1 == Not(Xor(nand2_cp3_1,k3_1))  
	c55 = nand3_cp3_1 == Not(And(xor1_cp3_1,xnor1_cp3_1))  
	c56 = xnor2_cp3_1 == Not(Xor(nand3_cp3_1,k4_1))  
	c57 = O_cp3 == xnor2_cp3_1  
	c58 = nand1_cp3_2 == Not(And(k1_2,A_cp3))  
	c59 = nand2_cp3_2 == Not(And(B_cp3,C_cp3))  
	c60 = xor1_cp3_2 == Xor(k2_2,nand1_cp3_2)  
	c61 = xnor1_cp3_2 == Not(Xor(nand2_cp3_2,k3_2))  
	c62 = nand3_cp3_2 == Not(And(xor1_cp3_2,xnor1_cp3_2))  
	c63 = xnor2_cp3_2 == Not(Xor(nand3_cp3_2,k4_2))  
	c64 = O_cp3 == xnor2_cp3_2  
	c65 = C_cp3 == True  
	c66 = A_cp3 == False  
	c67 = B_cp3 == True  
	c68 = O_cp3 == True  
	c69 = nand1_cp4_1 == Not(And(k1_1,A_cp4)) 
	c70 = nand2_cp4_1 == Not(And(B_cp4,C_cp4)) 
	c71 = xor1_cp4_1 == Xor(k2_1,nand1_cp4_1) 
	c72 = xnor1_cp4_1 == Not(Xor(nand2_cp4_1,k3_1)) 
	c73 = nand3_cp4_1 == Not(And(xor1_cp4_1,xnor1_cp4_1)) 
	c74 = xnor2_cp4_1 == Not(Xor(nand3_cp4_1,k4_1)) 
	c75 = O_cp4 == xnor2_cp4_1 
	c76 = nand1_cp4_2 == Not(And(k1_2,A_cp4)) 
	c77 = nand2_cp4_2 == Not(And(B_cp4,C_cp4)) 
	c78 = xor1_cp4_2 == Xor(k2_2,nand1_cp4_2) 
	c79 = xnor1_cp4_2 == Not(Xor(nand2_cp4_2,k3_2)) 
	c80 = nand3_cp4_2 == Not(And(xor1_cp4_2,xnor1_cp4_2)) 
	c81 = xnor2_cp4_2 == Not(Xor(nand3_cp4_2,k4_2)) 
	c82 = O_cp4 == xnor2_cp4_2 
	c83 = C_cp4 == False 
	c84 = A_cp4 == False 
	c85 = B_cp4 == False 
	c86 = O_cp4 == True 

	s = Solver()
	s.add(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60,c61,c62,c63,c64,c65,c66,c67,c68,c69,c70,c71,c72,c73,c74,c75,c76,c77,c78,c79,c80,c81,c82,c83,c84,c85,c86)
	try:
		return s.check(), s.model()
	except:
		return s.check(), None


if __name__ == '__main__':
	main()