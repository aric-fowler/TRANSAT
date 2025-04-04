from z3 import *

# Inputs
g0 = Bool('g0')
g1 = Bool('g1')
g2 = Bool('g2')
clk = Bool('clk')
r = Bool('r')

# Outputs
g66 = Bool('g66')
g67 = Bool('g67')
g117 = Bool('g117')
g118 = Bool('g118')
g132 = Bool('g132')
g133 = Bool('g133')

# Internal nets
g28 = Bool('g28')
g130 = Bool('g130')
g38 = Bool('g38')
g10 = Bool('g10')
g40 = Bool('g40')
g13 = Bool('g13')
g45 = Bool('g45')
g12 = Bool('g12')
g46 = Bool('g46')
g11 = Bool('g11')
g50 = Bool('g50')
g14 = Bool('g14')
g51 = Bool('g51')
g23 = Bool('g23')
g22 = Bool('g22')
g15 = Bool('g15')
g54 = Bool('g54')
g55 = Bool('g55')
g59 = Bool('g59')
g60 = Bool('g60')
g64 = Bool('g64')
i155 = Bool('i155')
g16 = Bool('g16')
i158 = Bool('i158')
g17 = Bool('g17')
g18 = Bool('g18')
g76 = Bool('g76')
g82 = Bool('g82')
g87 = Bool('g87')
g91 = Bool('g91')
g93 = Bool('g93')
g96 = Bool('g96')
g99 = Bool('g99')
g103 = Bool('g103')
g108 = Bool('g108')
g112 = Bool('g112')
g114 = Bool('g114')
g21 = Bool('g21')
i210 = Bool('i210')
i213 = Bool('i213')
g19 = Bool('g19')
g120 = Bool('g120')
g124 = Bool('g124')
g121 = Bool('g121')
i221 = Bool('i221')
g126 = Bool('g126')
g127 = Bool('g127')
g131 = Bool('g131')
i229 = Bool('i229')
i232 = Bool('i232')
i235 = Bool('i235')
g20 = Bool('g20')
i238 = Bool('i238')
g26 = Bool('g26')
g27 = Bool('g27')
g31 = Bool('g31')
g32 = Bool('g32')
g33 = Bool('g33')
g35 = Bool('g35')
g36 = Bool('g36')
g37 = Bool('g37')
g42 = Bool('g42')
g41 = Bool('g41')
g47 = Bool('g47')
g48 = Bool('g48')
g49 = Bool('g49')
g52 = Bool('g52')
g57 = Bool('g57')
g58 = Bool('g58')
g61 = Bool('g61')
g65 = Bool('g65')
g62 = Bool('g62')
g63 = Bool('g63')
g74 = Bool('g74')
g75 = Bool('g75')
g88 = Bool('g88')
g89 = Bool('g89')
g90 = Bool('g90')
g94 = Bool('g94')
g95 = Bool('g95')
g100 = Bool('g100')
g104 = Bool('g104')
g105 = Bool('g105')
g109 = Bool('g109')
g110 = Bool('g110')
g111 = Bool('g111')
g115 = Bool('g115')
g122 = Bool('g122')
g123 = Bool('g123')
g128 = Bool('g128')
g129 = Bool('g129')
g24 = Bool('g24')
g25 = Bool('g25')
g68 = Bool('g68')
g69 = Bool('g69')
g70 = Bool('g70')
g71 = Bool('g71')
g72 = Bool('g72')
g73 = Bool('g73')
g77 = Bool('g77')
g78 = Bool('g78')
g79 = Bool('g79')
g80 = Bool('g80')
g81 = Bool('g81')
g82 = Bool('g82')
g83 = Bool('g83')
g84 = Bool('g84')
g85 = Bool('g85')
g43 = Bool('g43')
g97 = Bool('g97')
g101 = Bool('g101')
g106 = Bool('g106')
g116 = Bool('g116')
g29 = Bool('g29')
g30 = Bool('g30')
g34 = Bool('g34')
g39 = Bool('g39')
g44 = Bool('g44')
g53 = Bool('g53')
g56 = Bool('g56')
g86 = Bool('g86')
g92 = Bool('g92')
g98 = Bool('g98')
g102 = Bool('g102')
g107 = Bool('g107')
g113 = Bool('g113')
g119 = Bool('g119')
g125 = Bool('g125')


# Combinational logic
c1 = (g28 == Not(g130))
c2 = (g38 == Not(g10))
c3 = (g40 == Not(g13))
c4 = (g45 == Not(g12))
c5 = (g46 == Not(g11))
c6 = (g50 == Not(g14))
c7 = (g51 == Not(g23))
c8 = (g54 == Not(g11))
c9 = (g55 == Not(g13))
c10 = (g59 == Not(g12))
c11 = (g60 == Not(g22))
c12 = (g64 == Not(g15))
c13 = (i155 == Not(g16))
c14 = (g66 == Not(i155))
c15 = (i158 == Not(g17))
c16 = (g67 == Not(i158))
c17 = (g76 == Not(g10))
c18 = (g82 == Not(g11))
c19 = (g87 == Not(g16))
c20 = (g91 == Not(g12))
c21 = (g93 == Not(g17))
c22 = (g96 == Not(g14))
c23 = (g99 == Not(g18))
c24 = (g103 == Not(g13))
c25 = (g108 == Not(g112))
c26 = (g114 == Not(g21))
c27 = (i210 == Not(g18))
c28 = (g117 == Not(i210))
c29 = (i213 == Not(g19))
c30 = (g118 == Not(i213))
c31 = (g120 == Not(g124))
c32 = (g121 == Not(g22))
c33 = (i221 == Not(g2))
c34 = (g124 == Not(i221))
c35 = (g126 == Not(g131))
c36 = (g127 == Not(g23))
c37 = (i229 == Not(g0))
c38 = (g130 == Not(i229))
c39 = (i232 == Not(g1))
c40 = (g131 == Not(i232))
c41 = (i235 == Not(g20))
c42 = (g132 == Not(i235))
c43 = (i238 == Not(g21))
c44 = (g133 == Not(i238))
c45 = (g26 == And(g28,g50))
c46 = (g27 == And(g51,g28))
c47 = (g31 == And(g10,g45,g13))
c48 = (g32 == And(g10,g11))
c49 = (g33 == And(g38,g46))
c50 = (g35 == And(g10,g11,g12))
c51 = (g36 == And(g38,g45))
c52 = (g37 == And(g46,g45))
c53 = (g42 == And(g40,g41))
c54 = (g48 == And(g45,g46,g10,g47))
c55 = (g49 == And(g50,g51,g52))
c56 = (g57 == And(g59,g11,g60,g61))
c57 = (g58 == And(g64,g65))
c58 = (g62 == And(g59,g11,g60,g61))
c59 = (g63 == And(g64,g65))
c60 = (g74 == And(g12,g14,g19))
c61 = (g75 == And(g82,g91,g14))
c62 = (g88 == And(g14,g87))
c63 = (g89 == And(g103,g96))
c64 = (g90 == And(g91,g103))
c65 = (g94 == And(g93,g13))
c66 = (g95 == And(g96,g13))
c67 = (g100 == And(g99,g14,g12))
c68 = (g105 == And(g103,g108,g104))
c69 = (g110 == And(g108,g109))
c70 = (g111 == And(g10,g112))
c71 = (g115 == And(g114,g14))
c72 = (g122 == And(g120,g121))
c73 = (g123 == And(g124,g22))
c74 = (g128 == And(g126,g127))
c75 = (g129 == And(g131,g23))
c76 = (g24 == Or(g38,g46,g45,g40))
c77 = (g25 == Or(g38,g11,g12))
c78 = (g68 == Or(g11,g12,g13,g96))
c79 = (g69 == Or(g103,g18))
c80 = (g70 == Or(g103,g14))
c81 = (g71 == Or(g82,g12,g13))
c82 = (g72 == Or(g91,g20))
c83 = (g73 == Or(g103,g20))
c84 = (g77 == Or(g112,g103,g96,g19))
c85 = (g78 == Or(g108,g76))
c86 = (g79 == Or(g103,g14))
c87 = (g80 == Or(g11,g14))
c88 = (g81 == Or(g12,g13))
c89 = (g83 == Or(g11,g12,g13,g96))
c90 = (g84 == Or(g82,g91,g14))
c91 = (g85 == Or(g91,g96,g17))
c92 = (g41 == Not(And(g12,g11,g10)))
c93 = (g43 == Not(And(g24,g25,g28)))
c94 = (g52 == Not(And(g13,g45,g46,g10)))
c95 = (g65 == Not(And(g59,g54,g22,g61)))
c96 = (g97 == Not(And(g83,g84,g85,g108)))
c97 = (g101 == Not(And(g68,g69,g70,g108)))
c98 = (g106 == Not(And(g77,g78)))
c99 = (g109 == Not(And(g71,g72,g73,g14)))
c100 = (g116 == Not(And(g79,g80,g81,g108)))
c101 = (g29 == Not(Or(g10,g130)))
c102 = (g30 == Not(Or(g31,g32,g33,g130)))
c103 = (g34 == Not(Or(g35,g36,g37,g130)))
c104 = (g39 == Not(Or(g42,g43)))
c105 = (g44 == Not(Or(g48,g49,g53)))
c106 = (g47 == Not(Or(g50,g40)))
c107 = (g53 == Not(Or(g26,g27)))
c108 = (g56 == Not(Or(g57,g58,g130)))
c109 = (g61 == Not(Or(g14,g55)))
c110 = (g86 == Not(Or(g88,g89,g90,g112)))
c111 = (g92 == Not(Or(g94,g95,g97)))
c112 = (g98 == Not(Or(g100,g101)))
c113 = (g102 == Not(Or(g105,g106)))
c114 = (g104 == Not(Or(g74,g75)))
c115 = (g107 == Not(Or(g110,g111)))
c116 = (g112 == Not(Or(g62,g63)))
c117 = (g113 == Not(Or(g115,g116)))
c118 = (g119 == Not(Or(g122,g123,g130)))
c119 = (g125 == Not(Or(g128,g129,g130)))


# Flip flops - asynchronous reset, rising-edge
intA_0 = Bool('intA_0')
intB_0 = Bool('intB_0')
intC_0 = Bool('intC_0')
intD_0 = Bool('intD_0')
c120 = Implies(Not(clk),(intA_0 == Not(g29)))
c121 = (intB_0 == Not(Or(r,intA_0)))
c122 = Implies(clk,(intA_0 == Not(intB_0)))
c123 = Implies(clk,(intC_0 == Not(intB_0)))
c124 = (intD_0 == Not(Or(r,intC_0)))
c125 = Implies(Not(clk),(intC_0 == Not(intD_0)))
c126 = (g10 == Not(intC_0))

intA_1 = Bool('intA_1')
intB_1 = Bool('intB_1')
intC_1 = Bool('intC_1')
intD_1 = Bool('intD_1')
c127 = Implies(Not(clk),(intA_1 == Not(g30)))
c128 = (intB_1 == Not(Or(r,intA_1)))
c129 = Implies(clk,(intA_1 == Not(intB_1)))
c130 = Implies(clk,(intC_1 == Not(intB_1)))
c131 = (intD_1 == Not(Or(r,intC_1)))
c132 = Implies(Not(clk),(intC_1 == Not(intD_1)))
c133 = (g11 == Not(intC_1))

intA_2 = Bool('intA_2')
intB_2 = Bool('intB_2')
intC_2 = Bool('intC_2')
intD_2 = Bool('intD_2')
c134 = Implies(Not(clk),(intA_2 == Not(g34)))
c135 = (intB_2 == Not(Or(r,intA_2)))
c136 = Implies(clk,(intA_2 == Not(intB_2)))
c137 = Implies(clk,(intC_2 == Not(intB_2)))
c138 = (intD_2 == Not(Or(r,intC_2)))
c139 = Implies(Not(clk),(intC_2 == Not(intD_2)))
c140 = (g12 == Not(intC_2))

intA_3 = Bool('intA_3')
intB_3 = Bool('intB_3')
intC_3 = Bool('intC_3')
intD_3 = Bool('intD_3')
c141 = Implies(Not(clk),(intA_3 == Not(g39)))
c142 = (intB_3 == Not(Or(r,intA_3)))
c143 = Implies(clk,(intA_3 == Not(intB_3)))
c144 = Implies(clk,(intC_3 == Not(intB_3)))
c145 = (intD_3 == Not(Or(r,intC_3)))
c146 = Implies(Not(clk),(intC_3 == Not(intD_3)))
c147 = (g13 == Not(intC_3))

intA_4 = Bool('intA_4')
intB_4 = Bool('intB_4')
intC_4 = Bool('intC_4')
intD_4 = Bool('intD_4')
c148 = Implies(Not(clk),(intA_4 == Not(g44)))
c149 = (intB_4 == Not(Or(r,intA_4)))
c150 = Implies(clk,(intA_4 == Not(intB_4)))
c151 = Implies(clk,(intC_4 == Not(intB_4)))
c152 = (intD_4 == Not(Or(r,intC_4)))
c153 = Implies(Not(clk),(intC_4 == Not(intD_4)))
c154 = (g14 == Not(intC_4))

intA_5 = Bool('intA_5')
intB_5 = Bool('intB_5')
intC_5 = Bool('intC_5')
intD_5 = Bool('intD_5')
c155 = Implies(Not(clk),(intA_5 == Not(g56)))
c156 = (intB_5 == Not(Or(r,intA_5)))
c157 = Implies(clk,(intA_5 == Not(intB_5)))
c158 = Implies(clk,(intC_5 == Not(intB_5)))
c159 = (intD_5 == Not(Or(r,intC_5)))
c160 = Implies(Not(clk),(intC_5 == Not(intD_5)))
c161 = (g15 == Not(intC_5))

intA_6 = Bool('intA_6')
intB_6 = Bool('intB_6')
intC_6 = Bool('intC_6')
intD_6 = Bool('intD_6')
c162 = Implies(Not(clk),(intA_6 == Not(g86)))
c163 = (intB_6 == Not(Or(r,intA_6)))
c164 = Implies(clk,(intA_6 == Not(intB_6)))
c165 = Implies(clk,(intC_6 == Not(intB_6)))
c166 = (intD_6 == Not(Or(r,intC_6)))
c167 = Implies(Not(clk),(intC_6 == Not(intD_6)))
c168 = (g16 == Not(intC_6))

intA_7 = Bool('intA_7')
intB_7 = Bool('intB_7')
intC_7 = Bool('intC_7')
intD_7 = Bool('intD_7')
c169 = Implies(Not(clk),(intA_7 == Not(g92)))
c170 = (intB_7 == Not(Or(r,intA_7)))
c171 = Implies(clk,(intA_7 == Not(intB_7)))
c172 = Implies(clk,(intC_7 == Not(intB_7)))
c173 = (intD_7 == Not(Or(r,intC_7)))
c174 = Implies(Not(clk),(intC_7 == Not(intD_7)))
c175 = (g17 == Not(intC_7))

intA_8 = Bool('intA_8')
intB_8 = Bool('intB_8')
intC_8 = Bool('intC_8')
intD_8 = Bool('intD_8')
c176 = Implies(Not(clk),(intA_8 == Not(g98)))
c177 = (intB_8 == Not(Or(r,intA_8)))
c178 = Implies(clk,(intA_8 == Not(intB_8)))
c179 = Implies(clk,(intC_8 == Not(intB_8)))
c180 = (intD_8 == Not(Or(r,intC_8)))
c181 = Implies(Not(clk),(intC_8 == Not(intD_8)))
c182 = (g18 == Not(intC_8))

intA_9 = Bool('intA_9')
intB_9 = Bool('intB_9')
intC_9 = Bool('intC_9')
intD_9 = Bool('intD_9')
c183 = Implies(Not(clk),(intA_9 == Not(g102)))
c184 = (intB_9 == Not(Or(r,intA_9)))
c185 = Implies(clk,(intA_9 == Not(intB_9)))
c186 = Implies(clk,(intC_9 == Not(intB_9)))
c187 = (intD_9 == Not(Or(r,intC_9)))
c188 = Implies(Not(clk),(intC_9 == Not(intD_9)))
c189 = (g19 == Not(intC_9))

intA_10 = Bool('intA_10')
intB_10 = Bool('intB_10')
intC_10 = Bool('intC_10')
intD_10 = Bool('intD_10')
c190 = Implies(Not(clk),(intA_10 == Not(g107)))
c191 = (intB_10 == Not(Or(r,intA_10)))
c192 = Implies(clk,(intA_10 == Not(intB_10)))
c193 = Implies(clk,(intC_10 == Not(intB_10)))
c194 = (intD_10 == Not(Or(r,intC_10)))
c195 = Implies(Not(clk),(intC_10 == Not(intD_10)))
c196 = (g20 == Not(intC_10))

intA_11 = Bool('intA_11')
intB_11 = Bool('intB_11')
intC_11 = Bool('intC_11')
intD_11 = Bool('intD_11')
c197 = Implies(Not(clk),(intA_11 == Not(g113)))
c198 = (intB_11 == Not(Or(r,intA_11)))
c199 = Implies(clk,(intA_11 == Not(intB_11)))
c200 = Implies(clk,(intC_11 == Not(intB_11)))
c201 = (intD_11 == Not(Or(r,intC_11)))
c202 = Implies(Not(clk),(intC_11 == Not(intD_11)))
c203 = (g21 == Not(intC_11))

intA_12 = Bool('intA_12')
intB_12 = Bool('intB_12')
intC_12 = Bool('intC_12')
intD_12 = Bool('intD_12')
c204 = Implies(Not(clk),(intA_12 == Not(g119)))
c205 = (intB_12 == Not(Or(r,intA_12)))
c206 = Implies(clk,(intA_12 == Not(intB_12)))
c207 = Implies(clk,(intC_12 == Not(intB_12)))
c208 = (intD_12 == Not(Or(r,intC_12)))
c209 = Implies(Not(clk),(intC_12 == Not(intD_12)))
c210 = (g22 == Not(intC_12))

intA_13 = Bool('intA_13')
intB_13 = Bool('intB_13')
intC_13 = Bool('intC_13')
intD_13 = Bool('intD_13')
c211 = Implies(Not(clk),(intA_13 == Not(g125)))
c212 = (intB_13 == Not(Or(r,intA_13)))
c213 = Implies(clk,(intA_13 == Not(intB_13)))
c214 = Implies(clk,(intC_13 == Not(intB_13)))
c215 = (intD_13 == Not(Or(r,intC_13)))
c216 = Implies(Not(clk),(intC_13 == Not(intD_13)))
c217 = (g23 == Not(intC_13))

s = Solver()
s.add(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c32,c33,c34,c35,c36,c37,c38,c39,c40,c41,c42,c43,c44,c45,c46,c47,c48,c49,c50,c51,c52,c53,c54,c55,c56,c57,c58,c59,c60,c61,c62,c63,c64,c65,c66,c67,c68,c69,c70,c71,c72,c73,c74,c75,c76,c77,c78,c79,c80,c81,c82,c83,c84,c85,c86,c87,c88,c89,c90,c91,c92,c93,c94,c95,c96,c97,c98,c99,c100,c101,c102,c103,c104,c105,c106,c107,c108,c109,c110,c111,c112,c113,c114,c115,c116,c117,c118,c119,c120,c121,c122,c123,c124,c125,c126,c127,c128,c129,c130,c131,c132,c133,c134,c135,c136,c137,c138,c139,c140,c141,c142,c143,c144,c145,c146,c147,c148,c149,c150,c151,c152,c153,c154,c155,c156,c157,c158,c159,c160,c161,c162,c163,c164,c165,c166,c167,c168,c169,c170,c171,c172,c173,c174,c175,c176,c177,c178,c179,c180,c181,c182,c183,c184,c185,c186,c187,c188,c189,c190,c191,c192,c193,c194,c195,c196,c197,c198,c199,c200,c201,c202,c203,c204,c205,c206,c207,c208,c209,c210,c211,c212,c213,c214,c215,c216,c217)

print(s.check())
