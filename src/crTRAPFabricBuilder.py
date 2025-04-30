#!/usr/bin/env python3
'''
Script for writing Z3-based propositional logic clauses of the TRAP circuit architecture with 
full custom routes (no interconnect).

Author:     Aric Fowler
Python:     3.10.6
Updated:    May 2024
'''
import os
import csv
import argparse
from z3 import *

# -------------------------------------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------------------------------------
from .globals import *       # TRANSAT common global variables

trapCustomVarTmplt = {'C1L21_{X}_{Y}':('Bool',None),
'C1L22_{X}_{Y}':('Bool',None),
'C1L23_{X}_{Y}':('Bool',None),
'C1L2Z_{X}_{Y}':('Bool',None),
'C2L21_{X}_{Y}':('Bool',None),
'C2L22_{X}_{Y}':('Bool',None),
'C2L23_{X}_{Y}':('Bool',None),
'C2L2Z_{X}_{Y}':('Bool',None),
'C3L21_{X}_{Y}':('Bool',None),
'C3L22_{X}_{Y}':('Bool',None),
'C3L23_{X}_{Y}':('Bool',None),
'C3L2Z_{X}_{Y}':('Bool',None),
'C1L11_{X}_{Y}':('Bool',None),
'C1L12_{X}_{Y}':('Bool',None),
'C1L13_{X}_{Y}':('Bool',None),
'C2L11_{X}_{Y}':('Bool',None),
'C2L12_{X}_{Y}':('Bool',None),
'C2L13_{X}_{Y}':('Bool',None),
'C3L11_{X}_{Y}':('Bool',None),
'C3L12_{X}_{Y}':('Bool',None),
'C3L13_{X}_{Y}':('Bool',None),
'M1C1P1_{X}_{Y}':('Bool',None),
'M1C1P2_{X}_{Y}':('Bool',None),
'M1C1P3_{X}_{Y}':('Bool',None),
'M1C2P1_{X}_{Y}':('Bool',None),
'M1C2P2_{X}_{Y}':('Bool',None),
'M1C2P3_{X}_{Y}':('Bool',None),
'M1C3P1_{X}_{Y}':('Bool',None),
'M1C3P2_{X}_{Y}':('Bool',None),
'M1C3P3_{X}_{Y}':('Bool',None),
'M2C1P1_{X}_{Y}':('Bool',None),
'M2C1P2_{X}_{Y}':('Bool',None),
'M2C1P3_{X}_{Y}':('Bool',None),
'M2C2P1_{X}_{Y}':('Bool',None),
'M2C2P2_{X}_{Y}':('Bool',None),
'M2C2P3_{X}_{Y}':('Bool',None),
'M2C3P1_{X}_{Y}':('Bool',None),
'M2C3P2_{X}_{Y}':('Bool',None),
'M2C3P3_{X}_{Y}':('Bool',None),
'M3C1P1_{X}_{Y}':('Bool',None),
'M3C1P2_{X}_{Y}':('Bool',None),
'M3C1P3_{X}_{Y}':('Bool',None),
'M3C2P1_{X}_{Y}':('Bool',None),
'M3C2P2_{X}_{Y}':('Bool',None),
'M3C2P3_{X}_{Y}':('Bool',None),
'M3C3P1_{X}_{Y}':('Bool',None),
'M3C3P2_{X}_{Y}':('Bool',None),
'M3C3P3_{X}_{Y}':('Bool',None),
'M4C1N1_{X}_{Y}':('Bool',None),
'M4C1N2_{X}_{Y}':('Bool',None),
'M4C1N3_{X}_{Y}':('Bool',None),
'M4C2N1_{X}_{Y}':('Bool',None),
'M4C2N2_{X}_{Y}':('Bool',None),
'M4C2N3_{X}_{Y}':('Bool',None),
'M4C3N1_{X}_{Y}':('Bool',None),
'M4C3N2_{X}_{Y}':('Bool',None),
'M4C3N3_{X}_{Y}':('Bool',None),
'M5C1N1_{X}_{Y}':('Bool',None),
'M5C1N2_{X}_{Y}':('Bool',None),
'M5C1N3_{X}_{Y}':('Bool',None),
'M5C2N1_{X}_{Y}':('Bool',None),
'M5C2N2_{X}_{Y}':('Bool',None),
'M5C2N3_{X}_{Y}':('Bool',None),
'M5C3N1_{X}_{Y}':('Bool',None),
'M5C3N2_{X}_{Y}':('Bool',None),
'M5C3N3_{X}_{Y}':('Bool',None),
'M6C1N1_{X}_{Y}':('Bool',None),
'M6C1N2_{X}_{Y}':('Bool',None),
'M6C1N3_{X}_{Y}':('Bool',None),
'M6C2N1_{X}_{Y}':('Bool',None),
'M6C2N2_{X}_{Y}':('Bool',None),
'M6C2N3_{X}_{Y}':('Bool',None),
'M6C3N1_{X}_{Y}':('Bool',None),
'M6C3N2_{X}_{Y}':('Bool',None),
'M6C3N3_{X}_{Y}':('Bool',None),
'M7C1N1_{X}_{Y}':('Bool',None),
'M7C1N2_{X}_{Y}':('Bool',None),
'M7C1N3_{X}_{Y}':('Bool',None),
'M7C2N1_{X}_{Y}':('Bool',None),
'M7C2N2_{X}_{Y}':('Bool',None),
'M7C2N3_{X}_{Y}':('Bool',None),
'M7C3N1_{X}_{Y}':('Bool',None),
'M7C3N2_{X}_{Y}':('Bool',None),
'M7C3N3_{X}_{Y}':('Bool',None),
'C1N1_{X}_{Y}':('Bool',None),
'C1N2_{X}_{Y}':('Bool',None),
'C1N3_{X}_{Y}':('Bool',None),
'C1NH_{X}_{Y}':('Bool',None),
'C1NV_{X}_{Y}':('Bool',None),
'C1P1_{X}_{Y}':('Bool',None),
'C1P2_{X}_{Y}':('Bool',None),
'C1P3_{X}_{Y}':('Bool',None),
'C2N1_{X}_{Y}':('Bool',None),
'C2N2_{X}_{Y}':('Bool',None),
'C2N3_{X}_{Y}':('Bool',None),
'C2NH_{X}_{Y}':('Bool',None),
'C2NV_{X}_{Y}':('Bool',None),
'C2P1_{X}_{Y}':('Bool',None),
'C2P2_{X}_{Y}':('Bool',None),
'C2P3_{X}_{Y}':('Bool',None),
'C3N1_{X}_{Y}':('Bool',None),
'C3N2_{X}_{Y}':('Bool',None),
'C3N3_{X}_{Y}':('Bool',None),
'C3NH_{X}_{Y}':('Bool',None),
'C3NV_{X}_{Y}':('Bool',None),
'C3P1_{X}_{Y}':('Bool',None),
'C3P2_{X}_{Y}':('Bool',None),
'C3P3_{X}_{Y}':('Bool',None),
'C1N_{X}_{Y}':('Bool',None),
'C1O_{X}_{Y}':('Bool',None),
'C1P_{X}_{Y}':('Bool',None),
'C2N_{X}_{Y}':('Bool',None),
'C2O_{X}_{Y}':('Bool',None),
'C2P_{X}_{Y}':('Bool',None),
'C3N_{X}_{Y}':('Bool',None),
'C3O_{X}_{Y}':('Bool',None),
'C3P_{X}_{Y}':('Bool',None),
'C1N_{R}_{Y}':('Bool',None),
'C1O_{R}_{Y}':('Bool',None),
'C1P_{R}_{Y}':('Bool',None),
'C3N2_{L}_{Y}':('Bool',None),
'C3NH_{L}_{Y}':('Bool',None),
'C3P2_{L}_{Y}':('Bool',None),
'VC1L21_{X}_{Y}':('Bool',None),
'VC1L22_{X}_{Y}':('Bool',None),
'VC1L23_{X}_{Y}':('Bool',None),
'VC1L2Z_{X}_{Y}':('Bool',None),
'VC2L21_{X}_{Y}':('Bool',None),
'VC2L22_{X}_{Y}':('Bool',None),
'VC2L23_{X}_{Y}':('Bool',None),
'VC2L2Z_{X}_{Y}':('Bool',None),
'VC3L21_{X}_{Y}':('Bool',None),
'VC3L22_{X}_{Y}':('Bool',None),
'VC3L23_{X}_{Y}':('Bool',None),
'VC3L2Z_{X}_{Y}':('Bool',None),
'VC1N_{X}_{Y}':('Bool',None),
'VC1O_{X}_{Y}':('Bool',None),
'VC1P_{X}_{Y}':('Bool',None),
'VC2N_{X}_{Y}':('Bool',None),
'VC2O_{X}_{Y}':('Bool',None),
'VC2P_{X}_{Y}':('Bool',None),
'VC3N_{X}_{Y}':('Bool',None),
'VC3O_{X}_{Y}':('Bool',None),
'VC3P_{X}_{Y}':('Bool',None),
'VC3N_{L}_{Y}':('Bool',None),
'VC3O_{L}_{Y}':('Bool',None),
'VC3P_{L}_{Y}':('Bool',None),
'VC1N_{R}_{Y}':('Bool',None),
'VC1O_{R}_{Y}':('Bool',None),
'VC1P_{R}_{Y}':('Bool',None),
'DC1N2_{X}_{Y}':('Bool',None),
'DC1NH_{X}_{Y}':('Bool',None),
'DC1P2_{X}_{Y}':('Bool',None),
'DC2N2_{X}_{Y}':('Bool',None),
'DC2NH_{X}_{Y}':('Bool',None),
'DC2P2_{X}_{Y}':('Bool',None),
'DC3N2_{X}_{Y}':('Bool',None),
'DC3NH_{X}_{Y}':('Bool',None),
'DC3P2_{X}_{Y}':('Bool',None),
'DC3N2_{L}_{Y}':('Bool',None),
'DC3NH_{L}_{Y}':('Bool',None),
'DC3P2_{L}_{Y}':('Bool',None),
'cntC1L21_{X}_{Y}':('Int',None),
'cntC1L22_{X}_{Y}':('Int',None),
'cntC1L23_{X}_{Y}':('Int',None),
'cntC1L2Z_{X}_{Y}':('Int',None),
'cntC2L21_{X}_{Y}':('Int',None),
'cntC2L22_{X}_{Y}':('Int',None),
'cntC2L23_{X}_{Y}':('Int',None),
'cntC2L2Z_{X}_{Y}':('Int',None),
'cntC3L21_{X}_{Y}':('Int',None),
'cntC3L22_{X}_{Y}':('Int',None),
'cntC3L23_{X}_{Y}':('Int',None),
'cntC3L2Z_{X}_{Y}':('Int',None),
'cntC1P_{X}_{Y}':('Int',None),
'cntC1O_{X}_{Y}':('Int',None),
'cntC1N_{X}_{Y}':('Int',None),
'cntC2P_{X}_{Y}':('Int',None),
'cntC2O_{X}_{Y}':('Int',None),
'cntC2N_{X}_{Y}':('Int',None),
'cntC3P_{X}_{Y}':('Int',None),
'cntC3O_{X}_{Y}':('Int',None),
'cntC3N_{X}_{Y}':('Int',None),
'cntC1P_{R}_{Y}':('Int',None),
'cntC1O_{R}_{Y}':('Int',None),
'cntC1N_{R}_{Y}':('Int',None),}

trapCustomClsTmplt = ['(Implies(M2C1P3_{X}_{Y}, (C1P3_{X}_{Y} == C1L13_{X}_{Y})))',
'(Implies(M2C1P2_{X}_{Y}, (C1P2_{X}_{Y} == C1L12_{X}_{Y})))',
'(Implies(M2C1P1_{X}_{Y}, (C1P1_{X}_{Y} == C1L11_{X}_{Y})))',
'(Implies(M4C1N1_{X}_{Y}, (C1L11_{X}_{Y} == C1N1_{X}_{Y})))',
'(Implies(M5C1N1_{X}_{Y}, (C1L12_{X}_{Y} == C1N1_{X}_{Y})))',
'(Implies(M6C1N1_{X}_{Y}, (C1L13_{X}_{Y} == C1N1_{X}_{Y})))',
'(Implies(M4C1N2_{X}_{Y}, (C1L11_{X}_{Y} == C1N2_{X}_{Y})))',
'(Implies(M5C1N2_{X}_{Y}, (C1L12_{X}_{Y} == C1N2_{X}_{Y})))',
'(Implies(M6C1N2_{X}_{Y}, (C1L13_{X}_{Y} == C1N2_{X}_{Y})))',
'(Implies(M4C1N3_{X}_{Y}, (C1L11_{X}_{Y} == C1N3_{X}_{Y})))',
'(Implies(M5C1N3_{X}_{Y}, (C1L12_{X}_{Y} == C1N3_{X}_{Y})))',
'(Implies(M6C1N3_{X}_{Y}, (C1L13_{X}_{Y} == C1N3_{X}_{Y})))',
'(Implies(M2C2P3_{X}_{Y}, (C2P3_{X}_{Y} == C2L13_{X}_{Y})))',
'(Implies(M2C2P2_{X}_{Y}, (C2P2_{X}_{Y} == C2L12_{X}_{Y})))',
'(Implies(M2C2P1_{X}_{Y}, (C2P1_{X}_{Y} == C2L11_{X}_{Y})))',
'(Implies(M4C2N1_{X}_{Y}, (C2L11_{X}_{Y} == C2N1_{X}_{Y})))',
'(Implies(M5C2N1_{X}_{Y}, (C2L12_{X}_{Y} == C2N1_{X}_{Y})))',
'(Implies(M6C2N1_{X}_{Y}, (C2L13_{X}_{Y} == C2N1_{X}_{Y})))',
'(Implies(M4C2N2_{X}_{Y}, (C2L11_{X}_{Y} == C2N2_{X}_{Y})))',
'(Implies(M5C2N2_{X}_{Y}, (C2L12_{X}_{Y} == C2N2_{X}_{Y})))',
'(Implies(M6C2N2_{X}_{Y}, (C2L13_{X}_{Y} == C2N2_{X}_{Y})))',
'(Implies(M4C2N3_{X}_{Y}, (C2L11_{X}_{Y} == C2N3_{X}_{Y})))',
'(Implies(M5C2N3_{X}_{Y}, (C2L12_{X}_{Y} == C2N3_{X}_{Y})))',
'(Implies(M6C2N3_{X}_{Y}, (C2L13_{X}_{Y} == C2N3_{X}_{Y})))',
'(Implies(M2C3P1_{X}_{Y}, (C3P1_{X}_{Y} == C3L11_{X}_{Y})))',
'(Implies(M2C3P2_{X}_{Y}, (C3P2_{X}_{Y} == C3L12_{X}_{Y})))',
'(Implies(M2C3P3_{X}_{Y}, (C3P3_{X}_{Y} == C3L13_{X}_{Y})))',
'(Implies(M4C3N1_{X}_{Y}, (C3L11_{X}_{Y} == C3N1_{X}_{Y})))',
'(Implies(M5C3N1_{X}_{Y}, (C3L12_{X}_{Y} == C3N1_{X}_{Y})))',
'(Implies(M6C3N1_{X}_{Y}, (C3L13_{X}_{Y} == C3N1_{X}_{Y})))',
'(Implies(M4C3N2_{X}_{Y}, (C3L11_{X}_{Y} == C3N2_{X}_{Y})))',
'(Implies(M5C3N2_{X}_{Y}, (C3L12_{X}_{Y} == C3N2_{X}_{Y})))',
'(Implies(M6C3N2_{X}_{Y}, (C3L13_{X}_{Y} == C3N2_{X}_{Y})))',
'(Implies(M4C3N3_{X}_{Y}, (C3L11_{X}_{Y} == C3N3_{X}_{Y})))',
'(Implies(M5C3N3_{X}_{Y}, (C3L12_{X}_{Y} == C3N3_{X}_{Y})))',
'(Implies(M6C3N3_{X}_{Y}, (C3L13_{X}_{Y} == C3N3_{X}_{Y})))',
'(Implies(M1C1P3_{X}_{Y}, (C1L13_{X}_{Y} == Not(C1L23_{X}_{Y}))))',
'(Implies(Not(M1C1P3_{X}_{Y}), (C1L13_{X}_{Y} == C1L23_{X}_{Y})))',
'(Implies(Not(M2C1P3_{X}_{Y}), (C1P3_{X}_{Y} == Not(M3C1P3_{X}_{Y}))))',
'(Implies(M1C1P2_{X}_{Y}, (C1L12_{X}_{Y} == Not(C1L22_{X}_{Y}))))',
'(Implies(Not(M1C1P2_{X}_{Y}), (C1L12_{X}_{Y} == C1L22_{X}_{Y})))',
'(Implies(Not(M2C1P2_{X}_{Y}), (C1P2_{X}_{Y} == Not(M3C1P2_{X}_{Y}))))',
'(Implies(M1C1P1_{X}_{Y}, (C1L11_{X}_{Y} == Not(C1L21_{X}_{Y}))))',
'(Implies(Not(M1C1P1_{X}_{Y}), (C1L11_{X}_{Y} == C1L21_{X}_{Y})))',
'(Implies(Not(M2C1P1_{X}_{Y}), (C1P1_{X}_{Y} == Not(M3C1P1_{X}_{Y}))))',
'(Implies(M1C2P3_{X}_{Y}, (C2L13_{X}_{Y} == Not(C2L23_{X}_{Y}))))',
'(Implies(Not(M1C2P3_{X}_{Y}), (C2L13_{X}_{Y} == C2L23_{X}_{Y})))',
'(Implies(Not(M2C2P3_{X}_{Y}), (C2P3_{X}_{Y} == Not(M3C2P3_{X}_{Y}))))',
'(Implies(M1C2P2_{X}_{Y}, (C2L12_{X}_{Y} == Not(C2L22_{X}_{Y}))))',
'(Implies(Not(M1C2P2_{X}_{Y}), (C2L12_{X}_{Y} == C2L22_{X}_{Y})))',
'(Implies(Not(M2C2P2_{X}_{Y}), (C2P2_{X}_{Y} == Not(M3C2P2_{X}_{Y}))))',
'(Implies(M1C2P1_{X}_{Y}, (C2L11_{X}_{Y} == Not(C2L21_{X}_{Y}))))',
'(Implies(Not(M1C2P1_{X}_{Y}), (C2L11_{X}_{Y} == C2L21_{X}_{Y})))',
'(Implies(Not(M2C2P1_{X}_{Y}), (C2P1_{X}_{Y} == Not(M3C2P1_{X}_{Y}))))',
'(Implies(M1C3P1_{X}_{Y}, (C3L11_{X}_{Y} == Not(C3L21_{X}_{Y}))))',
'(Implies(Not(M1C3P1_{X}_{Y}), (C3L11_{X}_{Y} == C3L21_{X}_{Y})))',
'(Implies(Not(M2C3P1_{X}_{Y}), (C3P1_{X}_{Y} == Not(M3C3P1_{X}_{Y}))))',
'(Implies(M1C3P2_{X}_{Y}, (C3L12_{X}_{Y} == Not(C3L22_{X}_{Y}))))',
'(Implies(Not(M1C3P2_{X}_{Y}), (C3L12_{X}_{Y} == C3L22_{X}_{Y})))',
'(Implies(Not(M2C3P2_{X}_{Y}), (C3P2_{X}_{Y} == Not(M3C3P2_{X}_{Y}))))',
'(Implies(M1C3P3_{X}_{Y}, (C3L13_{X}_{Y} == Not(C3L23_{X}_{Y}))))',
'(Implies(Not(M1C3P3_{X}_{Y}), (C3L13_{X}_{Y} == C3L23_{X}_{Y})))',
'(Implies(Not(M2C3P3_{X}_{Y}), (C3P3_{X}_{Y} == Not(M3C3P3_{X}_{Y}))))',
'(Implies(M4C1N1_{X}_{Y}, Not(Or(M5C1N1_{X}_{Y}, M6C1N1_{X}_{Y}))))',
'(Implies(M5C1N1_{X}_{Y}, Not(Or(M4C1N1_{X}_{Y}, M6C1N1_{X}_{Y}))))',
'(Implies(M6C1N1_{X}_{Y}, Not(Or(M5C1N1_{X}_{Y}, M4C1N1_{X}_{Y}))))',
'(Implies(M4C1N2_{X}_{Y}, Not(Or(M5C1N2_{X}_{Y}, M6C1N2_{X}_{Y}))))',
'(Implies(M5C1N2_{X}_{Y}, Not(Or(M4C1N2_{X}_{Y}, M6C1N2_{X}_{Y}))))',
'(Implies(M6C1N2_{X}_{Y}, Not(Or(M5C1N2_{X}_{Y}, M4C1N2_{X}_{Y}))))',
'(Implies(M4C1N3_{X}_{Y}, Not(Or(M5C1N3_{X}_{Y}, M6C1N3_{X}_{Y}))))',
'(Implies(M5C1N3_{X}_{Y}, Not(Or(M4C1N3_{X}_{Y}, M6C1N3_{X}_{Y}))))',
'(Implies(M6C1N3_{X}_{Y}, Not(Or(M5C1N3_{X}_{Y}, M4C1N3_{X}_{Y}))))',
'(Implies(M4C2N1_{X}_{Y}, Not(Or(M5C2N1_{X}_{Y}, M6C2N1_{X}_{Y}))))',
'(Implies(M5C2N1_{X}_{Y}, Not(Or(M4C2N1_{X}_{Y}, M6C2N1_{X}_{Y}))))',
'(Implies(M6C2N1_{X}_{Y}, Not(Or(M5C2N1_{X}_{Y}, M4C2N1_{X}_{Y}))))',
'(Implies(M4C2N2_{X}_{Y}, Not(Or(M5C2N2_{X}_{Y}, M6C2N2_{X}_{Y}))))',
'(Implies(M5C2N2_{X}_{Y}, Not(Or(M4C2N2_{X}_{Y}, M6C2N2_{X}_{Y}))))',
'(Implies(M6C2N2_{X}_{Y}, Not(Or(M5C2N2_{X}_{Y}, M4C2N2_{X}_{Y}))))',
'(Implies(M4C2N3_{X}_{Y}, Not(Or(M5C2N3_{X}_{Y}, M6C2N3_{X}_{Y}))))',
'(Implies(M5C2N3_{X}_{Y}, Not(Or(M4C2N3_{X}_{Y}, M6C2N3_{X}_{Y}))))',
'(Implies(M6C2N3_{X}_{Y}, Not(Or(M5C2N3_{X}_{Y}, M4C2N3_{X}_{Y}))))',
'(Implies(M4C3N1_{X}_{Y}, Not(Or(M5C3N1_{X}_{Y}, M6C3N1_{X}_{Y}))))',
'(Implies(M5C3N1_{X}_{Y}, Not(Or(M4C3N1_{X}_{Y}, M6C3N1_{X}_{Y}))))',
'(Implies(M6C3N1_{X}_{Y}, Not(Or(M5C3N1_{X}_{Y}, M4C3N1_{X}_{Y}))))',
'(Implies(M4C3N3_{X}_{Y}, Not(Or(M5C3N3_{X}_{Y}, M6C3N3_{X}_{Y}))))',
'(Implies(M5C3N3_{X}_{Y}, Not(Or(M4C3N3_{X}_{Y}, M6C3N3_{X}_{Y}))))',
'(Implies(M6C3N3_{X}_{Y}, Not(Or(M5C3N3_{X}_{Y}, M4C3N3_{X}_{Y}))))',
'(Implies(Not(Or(M4C1N1_{X}_{Y}, M5C1N1_{X}_{Y}, M6C1N1_{X}_{Y})), (M7C1N1_{X}_{Y} == C1N1_{X}_{Y})))',
'(Implies(Not(Or(M4C1N2_{X}_{Y}, M5C1N2_{X}_{Y}, M6C1N2_{X}_{Y})), (M7C1N2_{X}_{Y} == C1N2_{X}_{Y})))',
'(Implies(Not(Or(M4C1N3_{X}_{Y}, M5C1N3_{X}_{Y}, M6C1N3_{X}_{Y})), (M7C1N3_{X}_{Y} == C1N3_{X}_{Y})))',
'(Implies(Not(Or(M4C2N1_{X}_{Y}, M5C2N1_{X}_{Y}, M6C2N1_{X}_{Y})), (M7C2N1_{X}_{Y} == C2N1_{X}_{Y})))',
'(Implies(Not(Or(M4C2N2_{X}_{Y}, M5C2N2_{X}_{Y}, M6C2N2_{X}_{Y})), (M7C2N2_{X}_{Y} == C2N2_{X}_{Y})))',
'(Implies(Not(Or(M4C2N3_{X}_{Y}, M5C2N3_{X}_{Y}, M6C2N3_{X}_{Y})), (M7C2N3_{X}_{Y} == C2N3_{X}_{Y})))',
'(Implies(Not(Or(M4C3N1_{X}_{Y}, M5C3N1_{X}_{Y}, M6C3N1_{X}_{Y})), (M7C3N1_{X}_{Y} == C3N1_{X}_{Y})))',
'(Implies(Not(Or(M4C3N2_{X}_{Y}, M5C3N2_{X}_{Y}, M6C3N2_{X}_{Y})), (M7C3N2_{X}_{Y} == C3N2_{X}_{Y})))',
'(Implies(Not(Or(M4C3N3_{X}_{Y}, M5C3N3_{X}_{Y}, M6C3N3_{X}_{Y})), (M7C3N3_{X}_{Y} == C3N3_{X}_{Y})))',
'(Implies(Not(VC1L23_{X}_{Y}), Not(M2C1P3_{X}_{Y})))',                                                      # Invoke these if L2 wires are floating
'(Implies(Not(VC1L22_{X}_{Y}), Not(M2C1P2_{X}_{Y})))',
'(Implies(Not(VC1L21_{X}_{Y}), Not(M2C1P1_{X}_{Y})))',
'(Implies(Not(VC1L23_{X}_{Y}), And(Not(M6C1N1_{X}_{Y}), Not(M6C1N2_{X}_{Y}), Not(M6C1N3_{X}_{Y}))))',
'(Implies(Not(VC1L22_{X}_{Y}), And(Not(M5C1N1_{X}_{Y}), Not(M5C1N2_{X}_{Y}), Not(M5C1N3_{X}_{Y}))))',
'(Implies(Not(VC1L21_{X}_{Y}), And(Not(M4C1N1_{X}_{Y}), Not(M4C1N2_{X}_{Y}), Not(M4C1N3_{X}_{Y}))))',
'(Implies(Not(VC2L23_{X}_{Y}), Not(M2C2P3_{X}_{Y})))',
'(Implies(Not(VC2L22_{X}_{Y}), Not(M2C2P2_{X}_{Y})))',
'(Implies(Not(VC2L21_{X}_{Y}), Not(M2C2P1_{X}_{Y})))',
'(Implies(Not(VC2L23_{X}_{Y}), And(Not(M6C2N1_{X}_{Y}), Not(M6C2N2_{X}_{Y}), Not(M6C2N3_{X}_{Y}))))',
'(Implies(Not(VC2L22_{X}_{Y}), And(Not(M5C2N1_{X}_{Y}), Not(M5C2N2_{X}_{Y}), Not(M5C2N3_{X}_{Y}))))',
'(Implies(Not(VC2L21_{X}_{Y}), And(Not(M4C2N1_{X}_{Y}), Not(M4C2N2_{X}_{Y}), Not(M4C2N3_{X}_{Y}))))',
'(Implies(Not(VC3L23_{X}_{Y}), Not(M2C3P3_{X}_{Y})))',
'(Implies(Not(VC3L22_{X}_{Y}), Not(M2C3P2_{X}_{Y})))',
'(Implies(Not(VC3L21_{X}_{Y}), Not(M2C3P1_{X}_{Y})))',
'(Implies(Not(VC3L23_{X}_{Y}), And(Not(M6C3N1_{X}_{Y}), Not(M6C3N2_{X}_{Y}), Not(M6C3N3_{X}_{Y}))))',
'(Implies(Not(VC3L22_{X}_{Y}), And(Not(M5C3N1_{X}_{Y}), Not(M5C3N2_{X}_{Y}), Not(M5C3N3_{X}_{Y}))))',
'(Implies(Not(VC3L21_{X}_{Y}), And(Not(M4C3N1_{X}_{Y}), Not(M4C3N2_{X}_{Y}), Not(M4C3N3_{X}_{Y}))))',
'(Implies(Not(C1P3_{X}_{Y}), C1P_{X}_{Y}))',
'(Implies(Not(C1P2_{X}_{Y}), (C1P_{X}_{Y} == C2P_{X}_{Y})))',
'(Implies(Not(C1P1_{X}_{Y}), (C1P_{X}_{Y} == C1O_{X}_{Y})))',
'(Implies(C1NH_{X}_{Y}, (C1O_{X}_{Y} == C2O_{X}_{Y})))',
'(Implies(C1NV_{X}_{Y}, (C1O_{X}_{Y} == C1L2Z_{X}_{Y})))',
'(Implies(C1N1_{X}_{Y}, (C1O_{X}_{Y} == C1N_{X}_{Y})))',
'(Implies(C1N2_{X}_{Y}, (C1N_{X}_{Y} == C2N_{X}_{Y})))',
'(Implies(C1N3_{X}_{Y}, Not(C1N_{X}_{Y})))',
'(Implies(Not(C2P3_{X}_{Y}), C2P_{X}_{Y}))',
'(Implies(Not(C2P2_{X}_{Y}), (C2P_{X}_{Y} == C3P_{X}_{Y})))',
'(Implies(Not(C2P1_{X}_{Y}), (C2P_{X}_{Y} == C2O_{X}_{Y})))',
'(Implies(C2NH_{X}_{Y}, (C2O_{X}_{Y} == C3O_{X}_{Y})))',
'(Implies(C2NV_{X}_{Y}, (C2O_{X}_{Y} == C2L2Z_{X}_{Y})))',
'(Implies(C2N1_{X}_{Y}, (C2O_{X}_{Y} == C2N_{X}_{Y})))',
'(Implies(C2N2_{X}_{Y}, (C2N_{X}_{Y} == C3N_{X}_{Y})))',
'(Implies(C2N3_{X}_{Y}, Not(C2N_{X}_{Y})))',
'(Implies(Not(C3P3_{X}_{Y}), C3P_{X}_{Y}))',
'(Implies(Not(C3P2_{X}_{Y}), (C3P_{X}_{Y} == C1P_{R}_{Y})))',
'(Implies(Not(C3P1_{X}_{Y}), (C3P_{X}_{Y} == C3O_{X}_{Y})))',
'(Implies(C3NH_{X}_{Y}, (C3O_{X}_{Y} == C1O_{R}_{Y})))',
'(Implies(C3NV_{X}_{Y}, (C3O_{X}_{Y} == C3L2Z_{X}_{Y})))',
'(Implies(C3N1_{X}_{Y}, (C3O_{X}_{Y} == C3N_{X}_{Y})))',
'(Implies(C3N2_{X}_{Y}, (C3N_{X}_{Y} == C1N_{R}_{Y})))',
'(Implies(C3N3_{X}_{Y}, Not(C3N_{X}_{Y})))',
'(Implies(Not(C1P1_{X}_{Y}), And(DC3P2_{L}_{Y}, Not(DC1P2_{X}_{Y}))))',
'(Implies(Not(C2P1_{X}_{Y}), And(DC1P2_{X}_{Y}, Not(DC2P2_{X}_{Y}))))',
'(Implies(Not(C3P1_{X}_{Y}), And(DC2P2_{X}_{Y}, Not(DC3P2_{X}_{Y}))))',
'(Implies(C1N1_{X}_{Y}, And(DC3N2_{L}_{Y}, Not(DC1N2_{X}_{Y}))))',
'(Implies(C2N1_{X}_{Y}, And(DC1N2_{X}_{Y}, Not(DC2N2_{X}_{Y}))))',
'(Implies(C3N1_{X}_{Y}, And(DC2N2_{X}_{Y}, Not(DC3N2_{X}_{Y}))))',
'(VC1P_{X}_{Y} == Or(Not(C1P3_{X}_{Y}), And(VC2P_{X}_{Y}, Not(C1P2_{X}_{Y}), Not(DC1P2_{X}_{Y})), And(VC3P_{L}_{Y}, Not(C3P2_{L}_{Y}), DC3P2_{L}_{Y})))',
'(VC2P_{X}_{Y} == Or(Not(C2P3_{X}_{Y}), And(VC1P_{X}_{Y}, Not(C1P2_{X}_{Y}), DC1P2_{X}_{Y}), And(VC3P_{X}_{Y}, Not(C2P2_{X}_{Y}), Not(DC2P2_{X}_{Y}))))',
'(VC3P_{X}_{Y} == Or(Not(C3P3_{X}_{Y}), And(VC2P_{X}_{Y}, Not(C2P2_{X}_{Y}), DC2P2_{X}_{Y}), And(VC1P_{R}_{Y}, Not(C3P2_{X}_{Y}), Not(DC3P2_{X}_{Y}))))',
'(VC1O_{X}_{Y} == Or(And(VC1P_{X}_{Y}, Not(C1P1_{X}_{Y})), And(VC1N_{X}_{Y}, C1N1_{X}_{Y}), And(VC2O_{X}_{Y}, C1NH_{X}_{Y}, Not(DC1NH_{X}_{Y})), And(VC3O_{L}_{Y}, C3NH_{L}_{Y}, DC3NH_{L}_{Y})))',
'(VC2O_{X}_{Y} == Or(And(VC1O_{X}_{Y}, C1NH_{X}_{Y}, DC1NH_{X}_{Y}), And(VC2P_{X}_{Y}, Not(C2P1_{X}_{Y})), And(VC2N_{X}_{Y}, C2N1_{X}_{Y}), And(VC3O_{X}_{Y}, C2NH_{X}_{Y}, Not(DC2NH_{X}_{Y}))))',
'(VC3O_{X}_{Y} == Or(And(VC2O_{X}_{Y}, C2NH_{X}_{Y}, DC2NH_{X}_{Y}), And(VC3P_{X}_{Y}, Not(C3P1_{X}_{Y})), And(VC3N_{X}_{Y}, C3N1_{X}_{Y}), And(VC1O_{R}_{Y}, C3NH_{X}_{Y}, Not(DC3NH_{X}_{Y}))))',
'(VC1N_{X}_{Y} == Or((C1N3_{X}_{Y}), And(VC2N_{X}_{Y}, C1N2_{X}_{Y}, Not(DC1N2_{X}_{Y})), And(VC3N_{L}_{Y}, C3N2_{L}_{Y}, DC3N2_{L}_{Y})))',
'(VC2N_{X}_{Y} == Or(And(VC1N_{X}_{Y}, C1N2_{X}_{Y}, DC1N2_{X}_{Y}), (C2N3_{X}_{Y}), And(VC3N_{X}_{Y}, C2N2_{X}_{Y}, Not(DC2N2_{X}_{Y}))))',
'(VC3N_{X}_{Y} == Or(And(VC2N_{X}_{Y}, C2N2_{X}_{Y}, DC2N2_{X}_{Y}), (C3N3_{X}_{Y}), And(VC1N_{R}_{Y}, C3N2_{X}_{Y}, Not(DC3N2_{X}_{Y}))))',
'(VC1L2Z_{X}_{Y} == And(VC1O_{X}_{Y}, C1NV_{X}_{Y}))',
'(VC2L2Z_{X}_{Y} == And(VC2O_{X}_{Y}, C2NV_{X}_{Y}))',
'(VC3L2Z_{X}_{Y} == And(VC3O_{X}_{Y}, C3NV_{X}_{Y}))',
'(Implies(M2C1P3_{X}_{Y}, cntC1P_{X}_{Y} > cntC1L23_{X}_{Y}))',
'(Implies(And(M2C1P2_{X}_{Y}, DC1P2_{X}_{Y}), cntC2P_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(And(M2C1P2_{X}_{Y}, Not(DC1P2_{X}_{Y})), cntC1P_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(M2C1P1_{X}_{Y}, cntC1O_{X}_{Y} > cntC1L21_{X}_{Y}))',
'(Implies(M2C2P3_{X}_{Y}, cntC2P_{X}_{Y} > cntC2L23_{X}_{Y}))',
'(Implies(And(M2C2P2_{X}_{Y}, DC2P2_{X}_{Y}), cntC3P_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(And(M2C2P2_{X}_{Y}, Not(DC2P2_{X}_{Y})), cntC2P_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(M2C2P1_{X}_{Y}, cntC2O_{X}_{Y} > cntC2L21_{X}_{Y}))',
'(Implies(M2C3P3_{X}_{Y}, cntC3P_{X}_{Y} > cntC3L23_{X}_{Y}))',
'(Implies(And(M2C3P2_{X}_{Y}, DC3P2_{X}_{Y}), cntC1P_{R}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(And(M2C3P2_{X}_{Y}, Not(DC3P2_{X}_{Y})), cntC3P_{X}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(M2C3P1_{X}_{Y}, cntC3O_{X}_{Y} > cntC3L21_{X}_{Y}))',
'(Implies(M4C1N1_{X}_{Y}, cntC1O_{X}_{Y} > cntC1L21_{X}_{Y}))',
'(Implies(M5C1N1_{X}_{Y}, cntC1O_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(M6C1N1_{X}_{Y}, cntC1O_{X}_{Y} > cntC1L23_{X}_{Y}))',
'(Implies(And(M4C1N2_{X}_{Y}, Not(DC1N2_{X}_{Y})), cntC1N_{X}_{Y} > cntC1L21_{X}_{Y}))',
'(Implies(And(M5C1N2_{X}_{Y}, Not(DC1N2_{X}_{Y})), cntC1N_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(And(M6C1N2_{X}_{Y}, Not(DC1N2_{X}_{Y})), cntC1N_{X}_{Y} > cntC1L23_{X}_{Y}))',
'(Implies(And(M4C1N2_{X}_{Y}, DC1N2_{X}_{Y}), cntC2N_{X}_{Y} > cntC1L21_{X}_{Y}))',
'(Implies(And(M5C1N2_{X}_{Y}, DC1N2_{X}_{Y}), cntC2N_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(And(M6C1N2_{X}_{Y}, DC1N2_{X}_{Y}), cntC2N_{X}_{Y} > cntC1L23_{X}_{Y}))',
'(Implies(M4C1N3_{X}_{Y}, cntC1N_{X}_{Y} > cntC1L21_{X}_{Y}))',
'(Implies(M5C1N3_{X}_{Y}, cntC1N_{X}_{Y} > cntC1L22_{X}_{Y}))',
'(Implies(M6C1N3_{X}_{Y}, cntC1N_{X}_{Y} > cntC1L23_{X}_{Y}))',
'(Implies(M4C2N1_{X}_{Y}, cntC2O_{X}_{Y} > cntC2L21_{X}_{Y}))',
'(Implies(M5C2N1_{X}_{Y}, cntC2O_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(M6C2N1_{X}_{Y}, cntC2O_{X}_{Y} > cntC2L23_{X}_{Y}))',
'(Implies(And(M4C2N2_{X}_{Y}, Not(DC2N2_{X}_{Y})), cntC2N_{X}_{Y} > cntC2L21_{X}_{Y}))',
'(Implies(And(M5C2N2_{X}_{Y}, Not(DC2N2_{X}_{Y})), cntC2N_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(And(M6C2N2_{X}_{Y}, Not(DC2N2_{X}_{Y})), cntC2N_{X}_{Y} > cntC2L23_{X}_{Y}))',
'(Implies(And(M4C2N2_{X}_{Y}, DC2N2_{X}_{Y}), cntC3N_{X}_{Y} > cntC2L21_{X}_{Y}))',
'(Implies(And(M5C2N2_{X}_{Y}, DC2N2_{X}_{Y}), cntC3N_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(And(M6C2N2_{X}_{Y}, DC2N2_{X}_{Y}), cntC3N_{X}_{Y} > cntC2L23_{X}_{Y}))',
'(Implies(M4C2N3_{X}_{Y}, cntC2N_{X}_{Y} > cntC2L21_{X}_{Y}))',
'(Implies(M5C2N3_{X}_{Y}, cntC2N_{X}_{Y} > cntC2L22_{X}_{Y}))',
'(Implies(M6C2N3_{X}_{Y}, cntC2N_{X}_{Y} > cntC2L23_{X}_{Y}))',
'(Implies(M4C3N1_{X}_{Y}, cntC3O_{X}_{Y} > cntC3L21_{X}_{Y}))',
'(Implies(M5C3N1_{X}_{Y}, cntC3O_{X}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(M6C3N1_{X}_{Y}, cntC3O_{X}_{Y} > cntC3L23_{X}_{Y}))',
'(Implies(M4C3N3_{X}_{Y}, cntC3N_{X}_{Y} > cntC3L21_{X}_{Y}))',
'(Implies(M5C3N3_{X}_{Y}, cntC3N_{X}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(M6C3N3_{X}_{Y}, cntC3N_{X}_{Y} > cntC3L23_{X}_{Y}))',
'(Implies(And(M4C3N2_{X}_{Y}, Not(DC3N2_{X}_{Y})), cntC3N_{X}_{Y} > cntC3L21_{X}_{Y}))',
'(Implies(And(M5C3N2_{X}_{Y}, Not(DC3N2_{X}_{Y})), cntC3N_{X}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(And(M6C3N2_{X}_{Y}, Not(DC3N2_{X}_{Y})), cntC3N_{X}_{Y} > cntC3L23_{X}_{Y}))',
'(Implies(And(M4C3N2_{X}_{Y}, DC3N2_{X}_{Y}), cntC1N_{R}_{Y} > cntC3L21_{X}_{Y}))',
'(Implies(And(M5C3N2_{X}_{Y}, DC3N2_{X}_{Y}), cntC1N_{R}_{Y} > cntC3L22_{X}_{Y}))',
'(Implies(And(M6C3N2_{X}_{Y}, DC3N2_{X}_{Y}), cntC1N_{R}_{Y} > cntC3L23_{X}_{Y}))',
'(Implies(And(Not(C1P2_{X}_{Y}), DC1P2_{X}_{Y}), cntC2P_{X}_{Y} > cntC1P_{X}_{Y}))',
'(Implies(And(Not(C1P2_{X}_{Y}), Not(DC1P2_{X}_{Y})), cntC1P_{X}_{Y} > cntC2P_{X}_{Y}))',
'(Implies(Not(C1P1_{X}_{Y}), cntC1O_{X}_{Y} > cntC1P_{X}_{Y}))',
'(Implies(And(C1NH_{X}_{Y}, DC1NH_{X}_{Y}), cntC2O_{X}_{Y} > cntC1O_{X}_{Y}))',
'(Implies(And(C1NH_{X}_{Y}, Not(DC1NH_{X}_{Y})), cntC1O_{X}_{Y} > cntC2O_{X}_{Y}))',
'(Implies(C1NV_{X}_{Y}, cntC1L2Z_{X}_{Y} > cntC1O_{X}_{Y}))',
'(Implies(C1N1_{X}_{Y}, cntC1O_{X}_{Y} > cntC1N_{X}_{Y}))',
'(Implies(And(C1N2_{X}_{Y}, DC1N2_{X}_{Y}), cntC2N_{X}_{Y} > cntC1N_{X}_{Y}))',
'(Implies(And(C1N2_{X}_{Y}, Not(DC1N2_{X}_{Y})), cntC1N_{X}_{Y} > cntC2N_{X}_{Y}))',
'(Implies(And(Not(C2P2_{X}_{Y}), DC2P2_{X}_{Y}), cntC3P_{X}_{Y} > cntC2P_{X}_{Y}))',
'(Implies(And(Not(C2P2_{X}_{Y}), Not(DC2P2_{X}_{Y})), cntC2P_{X}_{Y} > cntC3P_{X}_{Y}))',
'(Implies(Not(C2P1_{X}_{Y}), cntC2O_{X}_{Y} > cntC2P_{X}_{Y}))',
'(Implies(And(C2NH_{X}_{Y}, DC2NH_{X}_{Y}), cntC3O_{X}_{Y} > cntC2O_{X}_{Y}))',
'(Implies(And(C2NH_{X}_{Y}, Not(DC2NH_{X}_{Y})), cntC2O_{X}_{Y} > cntC3O_{X}_{Y}))',
'(Implies(C2NV_{X}_{Y}, cntC2L2Z_{X}_{Y} > cntC2O_{X}_{Y}))',
'(Implies(C2N1_{X}_{Y}, cntC2O_{X}_{Y} > cntC2N_{X}_{Y}))',
'(Implies(And(C2N2_{X}_{Y}, DC2N2_{X}_{Y}), cntC3N_{X}_{Y} > cntC2N_{X}_{Y}))',
'(Implies(And(C2N2_{X}_{Y}, Not(DC2N2_{X}_{Y})), cntC2N_{X}_{Y} > cntC3N_{X}_{Y}))',
'(Implies(And(Not(C3P2_{X}_{Y}), DC3P2_{X}_{Y}), cntC1P_{R}_{Y} > cntC3P_{X}_{Y}))',
'(Implies(And(Not(C3P2_{X}_{Y}), Not(DC3P2_{X}_{Y})), cntC3P_{X}_{Y} > cntC1P_{R}_{Y}))',
'(Implies(Not(C3P1_{X}_{Y}), cntC3O_{X}_{Y} > cntC3P_{X}_{Y}))',
'(Implies(And(C3NH_{X}_{Y}, Not(DC3NH_{X}_{Y})), cntC3O_{X}_{Y} > cntC1O_{R}_{Y}))',
'(Implies(And(C3NH_{X}_{Y}, DC3NH_{X}_{Y}), cntC1O_{R}_{Y} > cntC3O_{X}_{Y}))',
'(Implies(C3NV_{X}_{Y}, cntC3L2Z_{X}_{Y} > cntC3O_{X}_{Y}))',
'(Implies(C3N1_{X}_{Y}, cntC3O_{X}_{Y} > cntC3N_{X}_{Y}))',
'(Implies(And(C3N2_{X}_{Y}, DC3N2_{X}_{Y}), cntC1N_{R}_{Y} > cntC3N_{X}_{Y}))',
'(Implies(And(C3N2_{X}_{Y}, Not(DC3N2_{X}_{Y})), cntC3N_{X}_{Y} > cntC1N_{R}_{Y}))',]

lBndClsTmplt = ['(C3P2_{L}_{Y})',
'(Not(C3N2_{L}_{Y}))',
'(Not(C3NH_{L}_{Y}))',]

rBndClsTmplt = ['(C3P2_{X}_{Y})',
'(Not(C3N2_{X}_{Y}))',
'(Not(C3NH_{X}_{Y}))',]

cntBoundClsTmplt = ['And((minCnt < cntC1L21_{X}_{Y}), (cntC1L21_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1L22_{X}_{Y}), (cntC1L22_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1L23_{X}_{Y}), (cntC1L23_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1L2Z_{X}_{Y}), (cntC1L2Z_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2L21_{X}_{Y}), (cntC2L21_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2L22_{X}_{Y}), (cntC2L22_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2L23_{X}_{Y}), (cntC2L23_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2L2Z_{X}_{Y}), (cntC2L2Z_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3L21_{X}_{Y}), (cntC3L21_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3L22_{X}_{Y}), (cntC3L22_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3L23_{X}_{Y}), (cntC3L23_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3L2Z_{X}_{Y}), (cntC3L2Z_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1P_{X}_{Y}), (cntC1P_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1O_{X}_{Y}), (cntC1O_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1N_{X}_{Y}), (cntC1N_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2P_{X}_{Y}), (cntC2P_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2O_{X}_{Y}), (cntC2O_{X}_{Y} < maxCnt))',
'And((minCnt < cntC2N_{X}_{Y}), (cntC2N_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3P_{X}_{Y}), (cntC3P_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3O_{X}_{Y}), (cntC3O_{X}_{Y} < maxCnt))',
'And((minCnt < cntC3N_{X}_{Y}), (cntC3N_{X}_{Y} < maxCnt))',
'And((minCnt < cntC1P_{R}_{Y}), (cntC1P_{R}_{Y} < maxCnt))',
'And((minCnt < cntC1O_{R}_{Y}), (cntC1O_{R}_{Y} < maxCnt))',
'And((minCnt < cntC1N_{R}_{Y}), (cntC1N_{R}_{Y} < maxCnt))',]

trapUnitKeyTmplt = ['M1C1P1_{X}_{Y}',
'M1C1P2_{X}_{Y}',
'M1C1P3_{X}_{Y}',
'M1C2P1_{X}_{Y}',
'M1C2P2_{X}_{Y}',
'M1C2P3_{X}_{Y}',
'M1C3P1_{X}_{Y}',
'M1C3P2_{X}_{Y}',
'M1C3P3_{X}_{Y}',
'M2C1P1_{X}_{Y}',
'M2C1P2_{X}_{Y}',
'M2C1P3_{X}_{Y}',
'M2C2P1_{X}_{Y}',
'M2C2P2_{X}_{Y}',
'M2C2P3_{X}_{Y}',
'M2C3P1_{X}_{Y}',
'M2C3P2_{X}_{Y}',
'M2C3P3_{X}_{Y}',
'M3C1P1_{X}_{Y}',
'M3C1P2_{X}_{Y}',
'M3C1P3_{X}_{Y}',
'M3C2P1_{X}_{Y}',
'M3C2P2_{X}_{Y}',
'M3C2P3_{X}_{Y}',
'M3C3P1_{X}_{Y}',
'M3C3P2_{X}_{Y}',
'M3C3P3_{X}_{Y}',
'M4C1N1_{X}_{Y}',
'M4C1N2_{X}_{Y}',
'M4C1N3_{X}_{Y}',
'M4C2N1_{X}_{Y}',
'M4C2N2_{X}_{Y}',
'M4C2N3_{X}_{Y}',
'M4C3N1_{X}_{Y}',
'M4C3N2_{X}_{Y}',
'M4C3N3_{X}_{Y}',
'M5C1N1_{X}_{Y}',
'M5C1N2_{X}_{Y}',
'M5C1N3_{X}_{Y}',
'M5C2N1_{X}_{Y}',
'M5C2N2_{X}_{Y}',
'M5C2N3_{X}_{Y}',
'M5C3N1_{X}_{Y}',
'M5C3N2_{X}_{Y}',
'M5C3N3_{X}_{Y}',
'M6C1N1_{X}_{Y}',
'M6C1N2_{X}_{Y}',
'M6C1N3_{X}_{Y}',
'M6C2N1_{X}_{Y}',
'M6C2N2_{X}_{Y}',
'M6C2N3_{X}_{Y}',
'M6C3N1_{X}_{Y}',
'M6C3N2_{X}_{Y}',
'M6C3N3_{X}_{Y}',
'M7C1N1_{X}_{Y}',
'M7C1N2_{X}_{Y}',
'M7C1N3_{X}_{Y}',
'M7C2N1_{X}_{Y}',
'M7C2N2_{X}_{Y}',
'M7C2N3_{X}_{Y}',
'M7C3N1_{X}_{Y}',
'M7C3N2_{X}_{Y}',
'M7C3N3_{X}_{Y}',
'C1NH_{X}_{Y}',
'C1NV_{X}_{Y}',
'C2NH_{X}_{Y}',
'C2NV_{X}_{Y}',
'C3NH_{X}_{Y}',
'C3NV_{X}_{Y}']

hiZVarMapTmplt = {'C1L21_{X}_{Y}':'VC1L21_{X}_{Y}',
'C1L22_{X}_{Y}':'VC1L22_{X}_{Y}',
'C1L23_{X}_{Y}':'VC1L23_{X}_{Y}',
'C1L2Z_{X}_{Y}':'VC1L2Z_{X}_{Y}',
'C2L21_{X}_{Y}':'VC2L21_{X}_{Y}',
'C2L22_{X}_{Y}':'VC2L22_{X}_{Y}',
'C2L23_{X}_{Y}':'VC2L23_{X}_{Y}',
'C2L2Z_{X}_{Y}':'VC2L2Z_{X}_{Y}',
'C3L21_{X}_{Y}':'VC3L21_{X}_{Y}',
'C3L22_{X}_{Y}':'VC3L22_{X}_{Y}',
'C3L23_{X}_{Y}':'VC3L23_{X}_{Y}',
'C3L2Z_{X}_{Y}':'VC3L2Z_{X}_{Y}',
}

cntVarMapTmplt = {'C1L21_{X}_{Y}':'cntC1L21_{X}_{Y}',
'C1L22_{X}_{Y}':'cntC1L22_{X}_{Y}',
'C1L23_{X}_{Y}':'cntC1L23_{X}_{Y}',
'C1L2Z_{X}_{Y}':'cntC1L2Z_{X}_{Y}',
'C2L21_{X}_{Y}':'cntC2L21_{X}_{Y}',
'C2L22_{X}_{Y}':'cntC2L22_{X}_{Y}',
'C2L23_{X}_{Y}':'cntC2L23_{X}_{Y}',
'C2L2Z_{X}_{Y}':'cntC2L2Z_{X}_{Y}',
'C3L21_{X}_{Y}':'cntC3L21_{X}_{Y}',
'C3L22_{X}_{Y}':'cntC3L22_{X}_{Y}',
'C3L23_{X}_{Y}':'cntC3L23_{X}_{Y}',
'C3L2Z_{X}_{Y}':'cntC3L2Z_{X}_{Y}',
}


# -------------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------------
def writeZ3pl(z3Vars:dict,z3Lines:list,z3Fn:str,prnt:bool) -> int:
    '''
    Writes or appends a Python Z3 script from a provided list of lines. If append is true, then
    writeZ3pl will read z3fileName and rewrite it, adding in additional clauses from z3Lines. 
    Assumes that the Python variable names and the PL variable names are identical. Returns 0 
    on success.

    prnt    -   If enabled, the written Z3 file will print its results to a text file, rather than
                return the result to the Python shell.
    '''
    clauseIndList = []

    with open(z3Fn,'w') as f:
        f.write('from z3 import *\n')
        if print:
            f.write("set_option('verbose','10')")
        f.write('\n\ndef main():\n')
        for var,varAtts in z3Vars.items():     # If the variable declaration requires arguments...
            if varAtts[1] is not None:
                f.write(f"\t{var} = {varAtts[0]}('{var}'{varAtts[1]})\n")
            else:
                f.write(f"\t{var} = {varAtts[0]}('{var}')\n")
        f.write('\n')
        for i,line in enumerate(z3Lines):
            clauseIndList.append(f'c{i}')
            f.write(f'\t{clauseIndList[i]} = {line}\n')
        f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\tprint(s.check())\n\n\nif __name__ == '__main__':\n\tmain()")
 
    return 0


def crTRAPFabricBuilder(numRows,numCols,pinMap,debug=False,outputFn='trapFabricPL',maxCount=None):

    print(f'Executing {os.path.basename(__file__)}...')

    allVars = {}
    allCls = []
    cntCls = []
    hiZVarMap = {}
    cntVarMap = {}
    ioCSVrows = []
    netHanging = {}

    for i in range(numCols):
        # Left/right boundary conditions to current unit i,j
        if (i-1) < 0:
            l = 'L'
        else:
            l = i-1
        if (i+1) >= numCols:
            r = 'R'
        else:
            r = i+1
        for j in range(numRows):
            for k,kType in trapCustomVarTmplt.items():    # Format & add variables to variable list
                allVars[k.format(X=i,Y=j,L=l,R=r)] = kType
            for k in trapCustomClsTmplt:                  # Format & add clauses to clause list
                allCls.append(k.format(X=i,Y=j,L=l,R=r))
            for k in cntBoundClsTmplt:                  # Format & add clauses to count clause list
                cntCls.append(k.format(X=i,Y=j,L=l,R=r))
            for k in trapUnitKeyTmplt:                  # Format & register key inputs with I/O CSV
                ioCSVrows.append([k.format(X=i,Y=j),'key'])
            for k,kHiZ in hiZVarMapTmplt.items():       # Format & expand map for hiZ variables with corresponding logical values (wires)
                hiZVarMap[k.format(X=i,Y=j)] = kHiZ.format(X=i,Y=j)
                netHanging[kHiZ.format(X=i,Y=j)] = True
            for k,kCnt in cntVarMapTmplt.items():       # Format & expand map for cnt variables with corresponding logical values (wires)
                cntVarMap[k.format(X=i,Y=j)] = kCnt.format(X=i,Y=j)
            if (i-1) < 0:                               # Include left/right boundary conditions in clause list
                for k in lBndClsTmplt:
                    allCls.append(k.format(X=i,Y=j,L=l,R=r))
            if (i+1) >= numCols:
                for k in rBndClsTmplt:
                    allCls.append(k.format(X=i,Y=j,L=l,R=r))

    # Add I/O pin connection clauses and custom routes to PL model & the I/O CSV
    with open(pinMap,'r') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                pinName,pinLoc,pinType = row
                if pinType == 'route':
                    allCls.append(f'({pinName} == {pinLoc})')
                    allCls.append(f'({hiZVarMap[pinName]} == {hiZVarMap[pinLoc]})')
                    allCls.append(f'({cntVarMap[pinName]} == {cntVarMap[pinLoc]})')
                    netHanging[hiZVarMap[pinLoc]] = False
                    netHanging[hiZVarMap[pinName]] = False
                else:
                    allVars[pinName] = ('Bool',None)
                    allCls.append(f'({pinName} == {pinLoc})')
                    if pinLoc not in hiZVarMap.keys() or (pinType != 'output' and pinType != 'input'):
                        raise RuntimeError(f'Designated location {pinLoc} for I/O pin {pinName} is not a valid pin location, or I/O type unrecognized Please place the pin at a valid location and set I/O type to "input" or "output".')
                    elif pinType == 'output':
                        ioCSVrows.append([pinName,pinType,hiZVarMap[pinLoc]])
                    elif pinType == 'input':
                        allCls.append(f'({hiZVarMap[pinLoc]} == True)')
                        if [pinName,pinType] not in ioCSVrows:
                            ioCSVrows.append([pinName,pinType])
                    netHanging[hiZVarMap[pinLoc]] = False

        except:
            raise RuntimeError('"pinMap" CSV input argument formatted incorrectly or contains typo.')

    # All unused interface inputs are undriven, therefore invalid
    for netV,isHanging in netHanging.items():
        if isHanging:
            allCls.append(f'({netV} == False)')

    # Insert count constraint, if applicable
    if maxCount is not None:
        allCls.extend(['minCnt == -1',f'maxCnt == {maxCount+1}'])
        allCls.extend(cntCls)
        allVars['minCnt'] = ('Int',None)
        allVars['maxCnt'] = ('Int',None)

    # Write TRAP logic model Python file
    writeZ3pl(allVars,allCls,f'{outputFn}.py',prnt=debug)

    # Write text file containing all key variables for output fabric Python file
    with open(f'{outputFn}_io.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(ioCSVrows)

    print(f'\nThe output fabric model {outputFn}.py has {allCls.__len__()} clauses and {allVars.__len__()} variables.\n')
    print(f'Script {os.path.basename(__file__)} concluded.\n')
    return os.EX_OK


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='crTRAPFabricBuilder',description='A tool for generating a model of a given size TRAP fabric with fully custom routes (no interconnect), written in Z3 for Python')
    parser.add_argument('numRows',type=int,help='The number of rows of TRAP units for the output fabric. Minimum value is 1')
    parser.add_argument('numCols',type=int,help='The number of columns of TRAP units for the output fabric. Minimum value is 1')
    parser.add_argument('pinMap',type=str,help='Path to the comma-delimited CSV file containing a list of I/O pin names, the corresponding L3 or L4 wire they are placed on, and whether the pin is an input or an output')
    parser.add_argument('-d',action='store_true',dest='debug',default=False,help='Puts verbosity in Z3 output scripts for SMT readout')
    parser.add_argument('-m',action='store',dest='maxCount',default=None,type=int,help='The maximum allotted value for count variables. A lower number may speed up SAT solver times, but could overconstrain the output model. The count will be constrained only if this variable is set')
    parser.add_argument('-o',action='store',dest='outputFileName',default='trapCRFabricPL',type=str,help='Base name of output files (no extension) to be created in the current directory')
    clArgs = parser.parse_args()

    crTRAPFabricBuilder(clArgs.numRows,clArgs.numCols,clArgs.pinMap,clArgs.debug,clArgs.outputFileName,clArgs.maxCount)
