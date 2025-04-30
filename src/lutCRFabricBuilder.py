#!/usr/bin/env python3
'''
Script for writing Z3-based propositional logic clauses of the TRAP circuit architecture.

Author:     Aric Fowler
Python:     3.10.6
Updated:    Feb 2024
'''
import os
import csv
import argparse
from z3 import *

# -------------------------------------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------------------------------------
from .globals import *       # TRANSAT common global variables

# P5 = LUT out, P4, P3, P2, P1 = LUT ins, M00-M15 = LUT mask
lutVarTmplt = {'P1_{X}':('Bool',None),
'P2_{X}':('Bool',None),
'P3_{X}':('Bool',None),
'P4_{X}':('Bool',None),
'P5_{X}':('Bool',None),
'M00_{X}':('Bool',None),
'M01_{X}':('Bool',None),
'M02_{X}':('Bool',None),
'M03_{X}':('Bool',None),
'M04_{X}':('Bool',None),
'M05_{X}':('Bool',None),
'M06_{X}':('Bool',None),
'M07_{X}':('Bool',None),
'M08_{X}':('Bool',None),
'M09_{X}':('Bool',None),
'M10_{X}':('Bool',None),
'M11_{X}':('Bool',None),
'M12_{X}':('Bool',None),
'M13_{X}':('Bool',None),
'M14_{X}':('Bool',None),
'M15_{X}':('Bool',None)
}

lutClsTmplt= ['(Implies(And(Not(P1_{X}), Not(P2_{X}), Not(P3_{X}), Not(P4_{X})), (P5_{X} == M00_{X})))',
'(Implies(And(Not(P1_{X}), Not(P2_{X}), Not(P3_{X}) , P4_{X}), (P5_{X} == M01_{X})))',
'(Implies(And(Not(P1_{X}), Not(P2_{X}), P3_{X}, Not(P4_{X})), (P5_{X} == M02_{X})))',
'(Implies(And(Not(P1_{X}), Not(P2_{X}), P3_{X}, P4_{X}), (P5_{X} == M03_{X})))',
'(Implies(And(Not(P1_{X}), P2_{X}, Not(P3_{X}), Not(P4_{X})), (P5_{X} == M04_{X})))',
'(Implies(And(Not(P1_{X}), P2_{X}, Not(P3_{X}), P4_{X}), (P5_{X} == M05_{X})))',
'(Implies(And(Not(P1_{X}), P2_{X}, P3_{X}, Not(P4_{X})), (P5_{X} == M06_{X})))',
'(Implies(And(Not(P1_{X}), P2_{X}, P3_{X}, P4_{X}), (P5_{X} == M07_{X})))',
'(Implies(And(P1_{X}, Not(P2_{X}), Not(P3_{X}), Not(P4_{X})), (P5_{X} == M08_{X})))',
'(Implies(And(P1_{X}, Not(P2_{X}), Not(P3_{X}), P4_{X}), (P5_{X} == M09_{X})))',
'(Implies(And(P1_{X}, Not(P2_{X}), P3_{X}, Not(P4_{X})), (P5_{X} == M10_{X})))',
'(Implies(And(P1_{X}, Not(P2_{X}), P3_{X}, P4_{X}), (P5_{X} == M11_{X})))',
'(Implies(And(P1_{X}, P2_{X}, Not(P3_{X}), Not(P4_{X})), (P5_{X} == M12_{X})))',
'(Implies(And(P1_{X}, P2_{X}, Not(P3_{X}), P4_{X}), (P5_{X} == M13_{X})))',
'(Implies(And(P1_{X}, P2_{X}, P3_{X}, Not(P4_{X})), (P5_{X} == M14_{X})))',
'(Implies(And(P1_{X}, P2_{X}, P3_{X}, P4_{X}), (P5_{X} == M15_{X})))'
]

'''cntBoundClsTmplt = ['And((minCnt < cntC1L21_{X}_{Y}), (cntC1L21_{X}_{Y} < maxCnt))',
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
'And((minCnt < cntL31_{X}_{Y}), (cntL31_{X}_{Y} < maxCnt))',
'And((minCnt < cntL32_{X}_{Y}), (cntL32_{X}_{Y} < maxCnt))',
'And((minCnt < cntL33_{X}_{Y}), (cntL33_{X}_{Y} < maxCnt))',
'And((minCnt < cntL34_{X}_{Y}), (cntL34_{X}_{Y} < maxCnt))',
'And((minCnt < cntL35_{X}_{Y}), (cntL35_{X}_{Y} < maxCnt))',
'And((minCnt < cntL36_{X}_{Y}), (cntL36_{X}_{Y} < maxCnt))',
'And((minCnt < cntL37_{X}_{Y}), (cntL37_{X}_{Y} < maxCnt))',
'And((minCnt < cntL38_{X}_{Y}), (cntL38_{X}_{Y} < maxCnt))',
'And((minCnt < cntL39_{X}_{Y}), (cntL39_{X}_{Y} < maxCnt))',
'And((minCnt < cntL41_{X}_{Y}), (cntL41_{X}_{Y} < maxCnt))',
'And((minCnt < cntL42_{X}_{Y}), (cntL42_{X}_{Y} < maxCnt))',
'And((minCnt < cntL43_{X}_{Y}), (cntL43_{X}_{Y} < maxCnt))',
'And((minCnt < cntL44_{X}_{Y}), (cntL44_{X}_{Y} < maxCnt))',
'And((minCnt < cntL45_{X}_{Y}), (cntL45_{X}_{Y} < maxCnt))',
'And((minCnt < cntL46_{X}_{Y}), (cntL46_{X}_{Y} < maxCnt))',
'And((minCnt < cntL47_{X}_{Y}), (cntL47_{X}_{Y} < maxCnt))',
'And((minCnt < cntL48_{X}_{Y}), (cntL48_{X}_{Y} < maxCnt))',
'And((minCnt < cntL49_{X}_{Y}), (cntL49_{X}_{Y} < maxCnt))',
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
'And((minCnt < cntC1N_{R}_{Y}), (cntC1N_{R}_{Y} < maxCnt))',
'Implies(isInpL31_{X}_{Y}, (cntL31_{X}_{Y} == 0))',
'Implies(isInpL32_{X}_{Y}, (cntL32_{X}_{Y} == 0))',
'Implies(isInpL33_{X}_{Y}, (cntL33_{X}_{Y} == 0))',
'Implies(isInpL34_{X}_{Y}, (cntL34_{X}_{Y} == 0))',
'Implies(isInpL35_{X}_{Y}, (cntL35_{X}_{Y} == 0))',
'Implies(isInpL36_{X}_{Y}, (cntL36_{X}_{Y} == 0))',
'Implies(isInpL37_{X}_{Y}, (cntL37_{X}_{Y} == 0))',
'Implies(isInpL38_{X}_{Y}, (cntL38_{X}_{Y} == 0))',
'Implies(isInpL39_{X}_{Y}, (cntL39_{X}_{Y} == 0))',
'Implies(isInpL41_{X}_{Y}, (cntL41_{X}_{Y} == 0))',
'Implies(isInpL42_{X}_{Y}, (cntL42_{X}_{Y} == 0))',
'Implies(isInpL43_{X}_{Y}, (cntL43_{X}_{Y} == 0))',
'Implies(isInpL44_{X}_{Y}, (cntL44_{X}_{Y} == 0))',
'Implies(isInpL45_{X}_{Y}, (cntL45_{X}_{Y} == 0))',
'Implies(isInpL46_{X}_{Y}, (cntL46_{X}_{Y} == 0))',
'Implies(isInpL47_{X}_{Y}, (cntL47_{X}_{Y} == 0))',
'Implies(isInpL48_{X}_{Y}, (cntL48_{X}_{Y} == 0))',
'Implies(isInpL49_{X}_{Y}, (cntL49_{X}_{Y} == 0))']'''

lutKeyTmplt = ['M00_{X}',
'M01_{X}',
'M02_{X}',
'M03_{X}',
'M04_{X}',
'M05_{X}',
'M06_{X}',
'M07_{X}',
'M08_{X}',
'M09_{X}',
'M10_{X}',
'M11_{X}',
'M12_{X}',
'M13_{X}',
'M14_{X}',
'M15_{X}']

inVarTmplt = ['P1_{X}',
'P2_{X}',
'P3_{X}',
'P4_{X}'
]


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
        if prnt:
            f.write("set_option('verbose','10')")
        f.write('\n\ndef main():\n')
        for var,varAtts in z3Vars.items():
            if varAtts[1] is not None:      # If the variable declaration requires arguments, include them
                f.write(f"\t{var} = {varAtts[0]}('{var}'{varAtts[1]})\n")
            else:
                f.write(f"\t{var} = {varAtts[0]}('{var}')\n")
        f.write('\n')
        for i,line in enumerate(z3Lines):
            clauseIndList.append(f'c{i}')
            f.write(f'\t{clauseIndList[i]} = {line}\n')
        f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\tprint(s.check())\n\n\nif __name__ == '__main__':\n\tmain()")
 
    return 0


def lutCRFabricBuilder(numLUTs,pinMap,debug=False,outputFn='lutCRFabricPL',maxCount=None):

    print(f'Executing {os.path.basename(__file__)}...')

    allVars = {}
    allCls = []
    cntCls = []
    ioCSVrows = []
    lutInHanging = {}
    for i in range(numLUTs):
        for k,kType in lutVarTmplt.items():         # Format & add variables to variable list
            allVars[k.format(X=i)] = kType
        for k in lutClsTmplt:                       # Format & add clauses to clause list
            allCls.append(k.format(X=i))
        for k in lutKeyTmplt:                       # Format & register key inputs with I/O CSV
            ioCSVrows.append([k.format(X=i),'key'])
        for k in inVarTmplt:
            lutInHanging[k.format(X=i)] = True

    # Add I/O pin connection clauses and custom routes to PL model & the I/O CSV
    with open(pinMap,'r') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                pinName,pinLoc,pinType = row
                if pinType == 'route':
                    allCls.append(f'({pinName} == {pinLoc})')
                    #allCls.append(f'({cntVarMap[pinName]} == {cntVarMap[pinLoc]})')
                    lutInHanging[pinName] = False
                    lutInHanging[pinLoc] = False
                else:
                    allVars[pinName] = ('Bool',None)
                    allCls.append(f'({pinName} == {pinLoc})')
                    if pinType != 'output' and pinType != 'input':
                        raise RuntimeError(f'Designated location {pinLoc} for I/O pin {pinName} is not a valid pin location, or I/O type unrecognized Please place the pin at a valid location and set I/O type to "input" or "output".')
                    elif pinType == 'output':
                        ioCSVrows.append([pinName,pinType])
                    elif pinType == 'input':
                        ioCSVrows.append([pinName,pinType])
                        lutInHanging[pinLoc] = False
        except:
            raise RuntimeError('"pinMap" CSV input argument formatted incorrectly or contains typo.')

    # All unused interface inputs are undriven, therefore invalid
    for netV,isHanging in lutInHanging.items():
        if isHanging:
            allCls.append(f'({netV} == False)')

    # Insert count constraint, if applicable
    if maxCount is not None:
        allCls.extend(['minCnt == -1',f'maxCnt == {maxCount+1}'])
        allCls.extend(cntCls)
        allVars['minCnt'] = ('Int',None)
        allVars['maxCnt'] = ('Int',None)

    # Write LUT logic model Python file
    writeZ3pl(allVars,allCls,f'{outputFn}.py',prnt=debug)

    # Write text file containing all key variables for output fabric Python file
    with open(f'{outputFn}_io.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(ioCSVrows)

    print(f'\nThe output fabric model {outputFn}.py has {allCls.__len__()} clauses and {allVars.__len__()} variables.\n')
    print(f'Script {os.path.basename(__file__)} concluded.\n')
    return os.EX_OK


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='lutCRFabricBuilder',description='A tool for generating islands of LUTs hardwired together, written in Z3 for Python')
    parser.add_argument('numLUTs',type=int,help='The number of LUTs for the output fabric. Minimum value is 1')
    parser.add_argument('pinMap',type=str,help='Path to the comma-delimited CSV file containing a list of I/O pin names, the corresponding input wires they are placed on, and whether the pin is an input, output, or route')
    parser.add_argument('-d',action='store_true',dest='debug',default=False,help='Puts verbosity in Z3 output scripts for SMT readout')
    parser.add_argument('-m',action='store',dest='maxCount',default=None,type=int,help='The maximum allotted value for count variables. A lower number may speed up SAT solver times, but could overconstrain the output model. The count will be constrained only if this variable is set')
    parser.add_argument('-o',action='store',dest='outputFileName',default='lutCRFabricPL',type=str,help='Base name of output files (no extension) to be created in the current directory')
    clArgs = parser.parse_args()

    lutCRFabricBuilder(clArgs.numLUTs,clArgs.pinMap,clArgs.debug,clArgs.outputFileName,clArgs.maxCount)
