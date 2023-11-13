#!/usr/bin/env python3
'''
Script for running a SAT-based verification on encrypted circuits,
described in Z3  for Python, with an oracle described in Verilog HDL.

Author:     Aric Fowler
Python:     3.10.6
Updated:    Oct 2023
'''
import os
import sys
import csv
import shutil
import glob
import re
import argparse
import logging
import datetime
import importlib
from typing import Tuple
from z3 import *
from .globals import *       # STRAPT common global variables

# -------------------------------------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------------------------------------
logName = 'satVerify'
miterName = 'verMiter'
miterSuffix = '_m'
dipCircuitsName = 'dipCircuits'

miterFile = os.path.join(here,workDir) + miterName + '.py'
dipCircuitsFile = os.path.join(here,workDir) + dipCircuitsName + '.py'


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


def initDirs(outDir:str,logDir:str,outDirName='',freshDirs=False):
    '''
    Initialize output and log directories. Relies on information stored in satAttackConfig (cfg) Python file

    outDir      - String. Desired output directory name
    logDir      - String. Desired logs directory name
    outDirName  - String. Output directory name without any dates or anything that may be added on
                    to make it unique. If not set, it will be set to to outDir
    '''
    try:
        if freshDirs:
            # For loop removes any old output directories
            for item in glob.glob(os.path.join(os.getcwd(),outDirName)+'*'):
                if not os.path.isdir(item):
                    continue
                shutil.rmtree(item)
            shutil.rmtree(logDir)
        os.makedirs(outDir)
        os.makedirs(logDir)

    except:
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        if not os.path.exists(logDir):
            os.makedirs(logDir)


def readZ3pl(trgtZ3:str) -> Tuple[dict,dict,list]:
    '''
    Read a Python Z3 script and parse the variable and function declarations, leaving out any 
    comment lines or Z3 Solver information. Returns dict of variables and their corresponding
    arguments, and a string of functions.

    varsDict values are a tuple. varsDict[key][0] = varType, varsDict[key][1] = varArgs
    '''
    varsDict = {}
    funList = []
    with open(trgtZ3,'r') as f:
        f.seek(0)
        lines = f.readlines()

    # Search for variables
    for line in lines:
        mtchObj = re.match(r'^\s*(?P<varID>\w+)\s*=\s*(?P<varType>(Bool)|(Int)|(BitVec))\([\',\"](?P<varName>\w+)[\',\"](?P<varArgs>\s*,.*)?\).*$',line)
        if mtchObj:
            if (mtchObj.group('varID') != mtchObj.group('varName')):
                logging.error(f'Variable {mtchObj.group("varName")} is given a different identifier ("{mtchObj.group("varID")}") in the source Z3 Python script "{trgtZ3}". Change this so they are identical.')
                raise RuntimeError(f'Variable mismatch name in "{trgtZ3}". See log file for details.')
            else:
                varsDict[mtchObj.group('varID')] = (mtchObj.group('varType'),mtchObj.group('varArgs'))

    # Search for functions (logic clauses)
    for line in lines:
        mtchObj = re.match(r'^\s*(?P<funID>\w+)\s*=\s*(?P<fun>[^\'\"]*)\n$',line)     # Future work: there's gotta be a better RE to exclude "Solver"
        if mtchObj:
            if mtchObj.group('fun') != 'Solver()':
                funList.append(mtchObj.group('fun'))

    return varsDict,funList


def writeZ3pl(z3Vars:dict,z3Lines:list,z3Fn:str,append=False,prnt=False) -> int:
    '''
    Writes or appends a Python Z3 script from a provided list of lines. If append is true, then
    writeZ3pl will read z3fileName and rewrite it, adding in additional clauses from z3Lines. 
    Assumes that the Python variable names and the PL variable names are identical. Returns 0 
    on success.

    prnt    -   If enabled, the written Z3 file will print its results to a text file, rather than
                return the result to the Python shell.
    '''
    varList = {}
    clauseList = []
    clauseIndList = []

    if append:
        prxstVars,prxstClauses = readZ3pl(z3Fn)
        varList = varList | prxstVars
        clauseList.extend(prxstClauses)
    varList = varList | z3Vars
    clauseList.extend(z3Lines)

    with open(z3Fn,'w') as f:
        f.write('from z3 import *\n')
        if prnt:
            f.write("set_param('verbose',10)\n")
        f.write('\n\ndef main():\n')
        for var,varAtts in varList.items():     # If the variable declaration requires arguments...
            if varAtts[1] is not None:
                f.write(f"\t{var} = {varAtts[0]}('{var}'{varAtts[1]})\n")
            else:
                f.write(f"\t{var} = {varAtts[0]}('{var}')\n")
        f.write('\n')
        for i,line in enumerate(clauseList):
            clauseIndList.append('c{}'.format(i))
            f.write(f'\t{clauseIndList[i]} = {line}\n')
        if not prnt:
            f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\ttry:\n\t\treturn s.check(), s.model()\n\texcept:\n\t\treturn s.check(), None\n\n\nif __name__ == '__main__':\n\tmain()")
        else:
            f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\twith open('{z3Fn}.txt','w') as f:\n\t\tf.write(str(s.check())+'\\n\\n')\n\t\ttry:\n\t\t\tm = s.model()\n\t\t\tfor item in sorted([(d, m[d]) for d in m], key = lambda x: str(x[0])):\n\t\t\t\tf.write(str(item)+'\\n')\n\t\texcept:\n\t\t\tNone\n\n\nif __name__ == '__main__':\n\tmain()")
 
    return 0


def m2dict(model:z3.Model) -> dict:
    '''
    Given a Z3 Model object, convert all variables and their interpreted values to a Python dict.
    '''
    z3Dict = {}
    for d in model:
        try:
            z3Dict[str(d)] = bool(model[d])
        except:
            z3Dict[str(d)] = model[d].as_long()
    return z3Dict


def setup(plLogicFile,fresh,quiet):
    '''
    Parses input arguments, creates output and log directories, sets up logging, and elevates select
    variables to global scope.
    '''
    if quiet: blockPrint()
    print(f'Executing {os.path.basename(__file__)}...')

    # Setup logging & output directories
    initDirs(workDir,logDir,freshDirs=fresh)
    logging.basicConfig(
        filename= os.path.join(here,logDir)+logName+now+'.log',
        format=logFormat,
        datefmt=logDateFormat,
        level=logging.DEBUG)
    logging.info(f'SAT attack script called at: {datetime.datetime.now()}')
    logging.info(f'Target PL file: {plLogicFile}')
    logging.info('Output directories created.')

    sys.path.append(workDir)

    # Do a one-time check to ensure the I/O listed in the I/O text lists match the names 
    # found in the encrypted logic and the decrypted oracle netlist.
    logging.warning('Code does not currently support cross-checking I/O names found in text lists against netlist files. Please check manually.')


def copyCircuit(plClauses:list,allVars:dict,inList:list,keyList:list,outList:list,suffix='',modIns=True,modKeys=True,modOuts=True,modNets=True) -> Tuple[dict,list]:
    '''
    Create a copy of some lines of PL clauses, and modify the end suffixes of variables. If using
    this function multiple times on the same plClauses, be sure that you modify the nets in the 
    FIRST copy step, then set modNets=False for the rest of the calls. Returns modified list of 
    clauses and a new dictionary of all variables in the copy.

    plClauses       - List containing lines of a PL file
    allVars         - Dict of all variables in plClauses and their corresponding Z3 type (e.g., 'Bool', etc.)
    inList          - List containing names of each input variable
    keyList         - List containing names of each key input variable
    outList         - List containing names of each output variable
    suffix          - String containing suffix to be appended to 
    '''
    # Compile list of variables to be copied with new names
    changeList = {}
    if modIns:
        changeList = changeList | {k: allVars[k] for k in set(inList).intersection(allVars.keys())}
    if modOuts:
        changeList = changeList | {k: allVars[k] for k in set(outList).intersection(allVars.keys())}
    if modKeys:
        changeList = changeList | {k: allVars[k] for k in set(keyList).intersection(allVars.keys())}
    if modNets:
        netsList = [x for x in allVars if x not in (inList+outList+keyList)]
        changeList = changeList | {k: allVars[k] for k in set(netsList).intersection(allVars.keys())}

    # Create variable and clause copies
    clauses = plClauses
    clauseVars = {k:v for k,v in allVars.items() if k not in changeList}
    for var in changeList.keys():
        newVar = var+suffix
        clauses = [re.sub(r'\b{}\b'.format(var),newVar,i) for i in clauses]
        clauseVars = clauseVars | {newVar: allVars[var]}

    return clauses,clauseVars


def buildVerMiter(trgtEncPL:str,trgtFunPL:str,inVars:list,keyVars:dict,outVars:list,miterFile:str,mSuff='_m',hiZVars={}):
    '''
    Create verification miter circuit for two given input CNF files. Returns a list of input variable names and a list key variable 
    names for convenience.

    trgtFunPL   - Path to Z3 Python file containing PL clauses to create a miter circuit out of
    trgtEncPL   - Path to Z3 Python file containing PL clauses to create a miter circuit out of
    inVars      - List of variables designated as inputs in targetPL
    keyVars     - List of variables designated as key inputs in targetPL
    outVars     - List of variables designated as outputs in targetPL
    miterFile   - Desired path, filename, and extension for output Z3 file
    mSuff       - Desired suffix to be added to net names for each miter circuit (do not include copy number)
    hiZVars     - List of variables designates as outputs in targetPL
    '''
    # Read in encrypted & functional PL
    funPLVars,funPLClauses = readZ3pl(trgtFunPL)
    encPLVars,encPLClauses = readZ3pl(trgtEncPL)

    miterVars = {}
    miterClauses = []

    # Create copy of functional netlist
    copy,copyVars = copyCircuit(funPLClauses,funPLVars,inVars,[],outVars,suffix=f'{mSuff}1',modIns=False,modKeys=False)
    miterVars = miterVars | {k:v for k,v in copyVars.items() if k not in miterClauses}
    miterClauses.extend(copy)

    # Create copy of encypted netlist & hard-code keys
    copy,copyVars = copyCircuit(encPLClauses,encPLVars,inVars,list(keyVars.keys()),outVars,suffix=f'{mSuff}2',modIns=False)
    miterVars = miterVars | {k:v for k,v in copyVars.items() if k not in miterClauses}
    miterClauses.extend(copy)
    for var,val in keyVars.items():
        miterClauses.append(f'{var}{mSuff}2 == {val}')

    # Miter circuit - for all output pairs, at least one logical pair must differ. If hiZ variables are present only
    # within the encryptedPL, hardwire them to '1' (non-HiZ state). If complimentary hiZ variables are present within 
    # both the encryptedPL and functionalPL files, then equate them as though they were normal outputs.
    outSubclauses = []
    if hiZVars != {}:
        for outVar, hiZVar in hiZVars.items():
            if hiZVar in funPLVars:
                outSubclauses.append(f'Xor({outVar+mSuff+"1"},{outVar+mSuff+"2"})')
                miterClauses.append(f'({hiZVar}{mSuff}2 == {hiZVar}{mSuff}1)')
            else:
                outSubclauses.append(f'Xor({outVar+mSuff+"1"},{outVar+mSuff+"2"})')
                miterClauses.append(f'({hiZVar}{mSuff}2 == True)')
    else:
        for var in outVars:
            outSubclauses.append(f'Xor({var+mSuff+"1"},{var+mSuff+"2"})')
    miterClauses.append(f'Or({",".join(outSubclauses)})     # Miter circuit')

    writeZ3pl(miterVars,miterClauses,miterFile)


def runSAT(trgtZ3:str,voi=[]) -> Tuple[bool,list]:
    '''
    Run target Z3 file. Target file should contain all code necessary to run itself and return a
    SAT/UNSAT decision. If SAT, it should also return a list of values for variables of interest.
    Returns True if the SAT solver returns SAT (satisfied).

    trgtZ3      - Name Python module (file name with no ".py") containing PL clauses
    voi         - "Variables of interest": a list of all variable names you desire to be returned.
    '''

    # Import trgtZ3
    if trgtZ3 in sys.modules:
        importlib.reload(sys.modules[trgtZ3])
    else:
        importlib.import_module(trgtZ3)
    
    # Run trgtZ3
    decision, model = sys.modules[trgtZ3].main()

    # Extract Z3 result
    if re.match(r'\bsat\b',str(decision)):
        satisfied = True
        modelVals = m2dict(model)
        if voi != []:
            voiVals = dict(sorted({k: modelVals[k] for k in set(voi).intersection(modelVals.keys())}.items()))
        else:
            voiVals = dict(sorted(modelVals.items()))
    else:
        satisfied = False
        voiVals = None

    return satisfied,voiVals


def satVerify(plEncryptedFile:str,plFunctionFile:str,ioCSV:str,keyValueCSV:str,fresh=False,quiet=False,highImpedance=None):

    # Run argument parsing, directory creation, and logging setup
    startTime = datetime.datetime.now()
    setup(plEncryptedFile,fresh,quiet)

    # Read in input list, key value CSV, output list, and hiZVar list (if applicable)
    inVars = []
    outVars = []
    hiZVars = {}
    with open(ioCSV,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ioNm,ioAtts = row[0],row[1:]
            if ioAtts[0] == 'input':
                inVars.append(ioNm)
            elif ioAtts[0] == 'key':
                continue
            elif (ioAtts[0] == 'output') and highImpedance:
                outVars.append(ioNm)
                try:
                    hiZVars[ioNm] = ioAtts[1]
                except:
                    raise RuntimeError(f'I/O file {ioCSV} not formatted correctly to indicate a matching HiZ variable to output variable {ioNm}')
            elif (ioAtts[0] == 'output') and not highImpedance:
                outVars.append(ioNm)
            else:
                raise RuntimeError(f'I/O {ioNm} has unrecognized data type "{ioAtts[0]}". Please revise I/O file {ioCSV}')

    with open(keyValueCSV,'r') as f:
        reader = csv.reader(f,delimiter=',')
        keyVals = {}
        for row in reader:
            keyVals[row[0]] = row[1]

    # Build verification Z3 clauses
    logging.info(f'Creating SAT verification script, here: {miterFile}')
    buildVerMiter(plEncryptedFile,plFunctionFile,inVars,keyVals,outVars,miterFile,hiZVars=hiZVars)

    # Run SAT verification script
    logging.info('Running SAT verification script...')
    decision,voiVals = runSAT(miterName,inVars)
    if decision:
        logging.info(f'Verification failed! Programmed circuit working improperly for the input pattern: {voiVals}')
        print('\nSAT VERIFICATION FAILED! See log for details.')
    else:
        logging.info('Verification successful! Programmed circuit works correctly for all input patterns.')
        print('\nSAT VERIFICATION SUCCESSFUL!')

    # Wrap-up
    logging.info(f'{os.path.basename(__file__)} concluded. Total runtime: {datetime.datetime.now()-startTime} seconds')
    print(f'\nScript {os.path.basename(__file__)} concluded\n')
    if quiet: enablePrint()
    return decision,voiVals


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tool for running SAT verification on a programmable netlist written in Z3 for Python')
    parser.add_argument('plEncryptedFile',type=str,help='Path to a Python file containing propositional logic clauses that require key inputs. Clauses must be written in the Z3 Python format. For help, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('plFunctionFile',type=str,help='Path to a Python file containing the counterpart non-encrypted functionality to plEncryptedFile. Clauses must be written in the Z3 Python format. For help, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('keyValueCSV',type=str,help='Path to the CSV file containing a list of key input names and values to the plEncryptedFile')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-q','--quiet',default=False,action='store_true',help='Prevent printing of SAT attack progress to terminal')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs=parser.parse_args()

    satVerify(clArgs.plEncryptedFile,clArgs.plFunctionFile,clArgs.ioCSV,clArgs.keyValueCSV,clArgs.fresh,clArgs.quiet,clArgs.tristate)
