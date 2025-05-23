#!/usr/bin/env python3
'''
Script for running a SAT attack on encrypted circuits, described in Z3 
for Python, with an unencrypted oracle described in Verilog HDL.

Author:     Aric Fowler
Python:     3.10.6
Updated:    Feb 2024
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

# -------------------------------------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------------------------------------
from .globals import *       # TRANSAT common global variables
logName = 'satAttack'
miterName = 'miter'
miterSuffix = '_m'
dipCircuitsName = 'dipCircuits'
tbName = 'tb.v'
tbOutputFile = 'vOut'

defMiterFile = os.path.join(here,workDir) + miterName + '.py'
dipCircuitsFile = os.path.join(here,workDir) + dipCircuitsName + '.py'
tb = os.path.join(here,workDir) + tbName
extractedKeyCSV = os.path.join(here,workDir) + 'extracted_key.csv'


# -------------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------------


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__


def initDirs(outDir:str,logDir:str,outDirName='',freshDirs=False,debug=False):
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
            shutil.rmtree(debugDir)
        os.makedirs(outDir)
        os.makedirs(logDir)
        if debug:
            os.makedirs(debugDir)

    except:
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        if (not os.path.exists(debugDir)) and debug:
            os.makedirs(debugDir)


def readLastLine(file:str) -> str:
    '''
    Read only last line of a file. With this function, the contents of an entire file are
    not stored in memory. Efficient for large files.

    file    - Path to file to return the final line of
    '''
    with open(file,'rb') as f:
        try:
            f.seek(-2,os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2,os.SEEK_CUR)
        except OSError:
            f.seek(0)
        lastLine = f.readline().decode()

    return lastLine


def editLastLine(file:str,newLine:str):
    '''
    Replace the last line of a file with a new line. With this function, the contents of an entire 
    file are not stored in memory. Efficient for large files.

    file    - Path to file to return the final line of
    newLine - Replacement for last line
    '''
    with open(file,'r+b') as f:
        try:
            f.seek(-2,os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2,os.SEEK_CUR)
        except OSError:
            f.seek(0)
        # Delete old line
        f.truncate()
        # Write new line
        f.write(str.encode(newLine))


def setup(plLogicFile,fresh,pythonOracle,quiet,debug):
    '''
    Parses input arguments, creates output and log directories, sets up logging, and elevates select
    variables to global scope.
    '''
    if quiet: blockPrint()
    print(f'Executing {os.path.basename(__file__)}...')

    # Setup logging & output directories
    initDirs(workDir,logDir,freshDirs=fresh,debug=debug)
    logging.basicConfig(
        filename= os.path.join(here,logDir)+logName+'_'+now+'.log',
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

    # Check to see if iVerilog is installed if "-po" argument is not provided
    if pythonOracle is None:
        if shutil.which('iverilog') is not None:
            pass
        else:
            print('It appears iVerilog is not installed. Running installation now...')
            returnCode = os.system('sudo apt install iverilog')
            if returnCode != 0:
                raise OSError('iVerilog was not successfully installed. Exiting SAT attack.')
            else:
                print('iVerilog was installed correctly. Proceeding with SAT attack...\n')


def readZ3pl(trgtZ3:str) -> Tuple[dict,list]:
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
            clauseIndList.append(f'c{i}')
            f.write(f'\t{clauseIndList[i]} = {line}\n')
        if not prnt:
            f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\ttry:\n\t\treturn s.check(), s.model()\n\texcept:\n\t\treturn s.check(), None\n\n\nif __name__ == '__main__':\n\tmain()\n")
        else:
            f.write(f"\n\ts = Solver()\n\ts.add({','.join(clauseIndList)})\n\twith open('{z3Fn}.txt','w') as f:\n\t\tf.write(str(s.check())+'\\n\\n')\n\t\ttry:\n\t\t\tfor item in sorted([(d, s.model()[d]) for d in s.model()], key = lambda x: str(x[0])):\n\t\t\t\tf.write(str(item)+'\\n')\n\t\texcept:\n\t\t\tNone\n\ttry:\n\t\treturn s.check(), s.model()\n\texcept:\n\t\treturn s.check(), None\n\n\nif __name__ == '__main__':\n\tmain()\n")
 
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


def copyCircuit(plClauses:list,allVars:dict,inList:list,keyList:list,outList:list,suffix='',modIns=True,modKeys=True,modOuts=True,modNets=True) -> Tuple[list,dict]:
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


def buildMiter(trgtPL:str,inVars:list,keyVars:list,outVars:list,miterFile:str,mSuff='_m',hiZVars={},hiZOracle=True,debug=False):
    '''
    Create miter circuit for a given input Z3Py file. Returns a list of input variable names and a list key variable names for convenience.

    trgtPL      - Path to Z3 Python file containing PL clauses to create a miter circuit out of
    inVars      - List of variables designated as inputs in targetPL
    keyVars     - List of variables designated as key inputs in targetPL
    outVars     - List of variables designated as outputs in targetPL
    miterFile   - Desired path, filename, and extension for output Z3 file
    mSuff       - Desired suffix to be added to net names for each miter circuit (do not include copy number)
    hiZVars     - List of variables designates as outputs in targetPL
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)

    # Create two copies of one circuit with identical inputs
    miterVars = {}
    miterClauses = []
    for i in range(1,3):
        copy,copyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=f'{mSuff}{i}',modIns=False,modKeys=False)
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=f'_{i}',modIns=False,modOuts=False,modNets=False)  # This "recopy" step creates unique keys
        miterVars = miterVars | {k:v for k,v in copyVars.items() if k not in miterClauses}
        miterClauses.extend(copy)

    # Make the miter comparator
    outSubclauses = []
    if hiZVars == {}:
        # Traditional comparator
        for var in outVars:
                outSubclauses.append(f'Xor({var+mSuff+"1"},{var+mSuff+"2"})')
    elif hiZOracle:
        # "BLUE" miter comparator - for all output pairs, at least one logical pair must differ with at least one
        # of the two corresponding hiZ variables being true.
        for outVar, hiZVar in hiZVars.items():
            outSubclauses.append(f'And(Xor({outVar+mSuff+"1"},{outVar+mSuff+"2"}),Or({hiZVar+mSuff+"1"},{hiZVar+mSuff+"2"}))')
        
        # "GREEN" miter comparator - for all output pairs, at least one logical pair must differ with both of those
        # valids being valid, or the validity variables of the one output pair must differ
        # for outVar, hiZVar in hiZVars.items():
        #     outSubclauses.append(f'And(Xor({outVar+mSuff+"1"},{outVar+mSuff+"2"}),And({hiZVar+mSuff+"1"},{hiZVar+mSuff+"2"}))')
        #     outSubclauses.append(f'Xor({hiZVar+mSuff+"1"},{hiZVar+mSuff+"2"})')
    else:
        # "BLACK" miter comparator - for all output pairs, at least one logical pair must differ or at least one the 
        # validity variables that output pair must be false (works only when the oracle cannot express HiZ outputs but the netlist can)
        for outVar, hiZVar in hiZVars.items():
            outSubclauses.append(f'Not(And(Not(Xor({outVar+mSuff+"1"},{outVar+mSuff+"2"})),{hiZVar+mSuff+"1"},{hiZVar+mSuff+"2"}))')
    miterClauses.append(f'Or({",".join(outSubclauses)})     # Miter comparator')

    writeZ3pl(miterVars,miterClauses,miterFile,prnt=debug)


def runZ3(trgtZ3:str,voi=[]) -> Tuple[bool,dict]:
    '''
    Run target Z3 file. Target file should contain all code necessary to run itself and return a
    SAT/UNSAT decision. If SAT, it should also return a list of values for variables of interest.
    Returns True if the SAT solver returns SAT (satisfied).

    trgtZ3      - Name Python module (file name with no ".py") containing PL clauses
    voi         - "Variables of interest": a list of all variable names you desire to be returned. If
                    left blank, all variables are returned
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


def extractVerilogModule(netlistFile:str,modName:str) -> Tuple[str,list]:
    '''
    Extract a module from a netlist by name. Returns extracted netlist lines and a list of module I/O.

    netlistFile - Path and name of Verilog netlist file
    modName     - Name of Verilog module to be returned
    '''
    with open(netlistFile,'r') as f:
        netlistLines = f.readlines()
    startLine = 0

    # Parse for top-level module
    modIO = []
    for i,line in enumerate(netlistLines):
        mtchObj1 = re.match(r'^\s*module\s+(?P<modName>\w+)\s*\((?P<portList>.*)\).*$',line,re.S)
        mtchObj2 = re.match(r'^\s*endmodule\s*$',line,re.S)
        if mtchObj1 and (mtchObj1.group('modName') == modName):
            startLine = i
            modIO = ''.join(mtchObj1.group('portList').split()).split(',')  # Remove whitespace, convert to list using comma delimiting
        #if mtchObj2 and (i > startLine):
        if mtchObj2 and modIO:
            break

    return ''.join(netlistLines[startLine:i+1]), modIO


def buildTestbench(inputStim:list,tb:str,inList:list,outList:list,topLevelMod='top',simOutFile=tbOutputFile):
    '''
    Create Verilog testbench to query netlist for a specific input set.

    As of 12/6/2022, I can't guarantee that the Verilog I/O declaration style of declaring inputs and
    outputs within the module declaration line will work properly. Declaring inputs and outputs in the
    same line probably does not work either.

    inputStim   - 
    tb          - Desired filename and path for HDL testbench to be created
    inList      -
    outList     -
    inList      - 
    outList     -
    topLevelMod -
    '''

    # Create explicit port declaration
    portDec = []
    for var in (inList + outList):
        portDec.append(f'.{var}({var})')
    portDec = ','.join(portDec)

    ins = ','.join(inList)
    outs = ','.join(outList)


    # Format input assignment (for input assignment in testbench body)
    inputAssigns = []
    for var,val in inputStim.items():
        if val:
            inputAssigns.append(f"\t\t{var} <= 1'b1;\n")
        else:
            inputAssigns.append(f"\t\t{var} <= 1'b0;\n")


    # Format output value write
    outputWrites = []
    for var in outs.replace(' ','').split(','):
        outputWrites.append(f'\t\t$fwrite(f,"{var} : %b\\n",{var});\n')
        
    # Write the testbench file
    tbTemplate = f'''// Testbench for iVerilog oracle. Automatically generated by SAT attack script.
`timescale 10ms/1ms

module tb();
    reg {ins};
    wire {outs};
    integer f;

    {topLevelMod} dut({portDec});

    initial begin
        f = $fopen("{simOutFile}","w");
        #1
        // Input assignment - DIP
{''.join(inputAssigns)}
        #1
{''.join(outputWrites)}
        $fclose(f);
    end

endmodule'''

    with open(tb,'w') as f:
        f.write(tbTemplate)


def runiVerilog(cktIn:list,trgtNetlist:str,topLevelMod:str,inList:list,outList:list,trgtTb=str,simOutFn=str,ivCmdFn='iv_cmd_file') -> dict:
    '''
    Call external netlist simulation software iVerilog. Returns netlist output for a single input
    pattern, using the same syntax as the CNF clauses

    cktIn       -
    trgtNetlist - Verilog netlist filepath to include in ivCmdFn
    topLevelMod -
    inList      - List of input names for oracle and encrytped circuit
    outList     - List of output names for oracle and encrytped circuit
    trgtTb      -
    simOutFn    -
    ivCmdFn     -
    '''
    # Make testbench
    buildTestbench(cktIn,trgtTb,inList,outList,topLevelMod=topLevelMod,simOutFile=simOutFn)

    # Make IV file
    with open(ivCmdFn,'w') as f:
        f.write(trgtNetlist+'\n')
        f.write(trgtTb+'\n')

    # Run simulator
    os.system(f'iverilog -c "{ivCmdFn}"')
    os.system('./a.out')

    # Parse generated output
    cktOut = {}
    with open(simOutFn,'r') as f:
        lines = f.readlines()
    for line in lines:
        mtchObj = re.match(r'^(?P<outName>\w+)\s*:\s*(?P<value>[\dA-Fa-f]+)\s*$',line)
        try:
            if mtchObj.group('value') == '0':
                cktOut[mtchObj.group('outName')] = False
            else:
                cktOut[mtchObj.group('outName')] = True
        except:
            logging.error(f'Unable to properly parse iVerilog simulation output file "{simOutFn}"')

    # Delete extraneous files: a.out, iv file, testbench, simOut text file
    os.remove('a.out')
    os.remove(ivCmdFn)
    os.remove(trgtTb)
    os.remove(simOutFn)

    return cktOut


def runPyOracle(oracleIns:dict,oracleFile:io.TextIOWrapper) -> dict:
    '''
    Run Python oracle script.

    There's nothing here yet!
    '''
    raise RuntimeError('Whoops, using a Python oracle is not currently supported. Use a Verilog one instead.')


def queryOracle(oracleIns:dict,oracleFile:io.TextIOWrapper,inList:list,outList:list,topLevelMod='',trgtTb='',simOutFile='',oracleSel=False) -> dict:
    '''
    Function for selecting desired oracle query method. Returns oracle outputs as a dict.

    oracleIns   - Values for inputs to query oracle with.
    inList      - List of oracle input names.
    outList     - List of oracle output names. 
    topLevelMod - Name of top level mod in Verilog file. Necessary only if oracleSel = False.
    oracleSel   - If true, indicates that oracleFile is a Python file instead of a Verilog file.
    '''
    if not oracleSel and (topLevelMod != '' or trgtTb != '' or simOutFile != ''):
        ivCmdFile = os.path.join(here,workDir) + 'iv_cmd_file'
        oracleOut = runiVerilog(oracleIns,oracleFile,topLevelMod,inList,outList,trgtTb,simOutFile,ivCmdFn=ivCmdFile)
    elif not oracleSel:
        raise RuntimeError('Missing arguments for using an iVerilog oracle testbench.')
    else:
        oracleOut = runPyOracle()

    return oracleOut


def appendMiter(copyTrgt:str,DIP:dict,oracleOut:dict,inVars:list,keyVars:list,outVars:list,miterFile:str,suff:str,debug=False,hiZVars={}):
    '''
    Append circuit copies to a preexisting miter circuit to prevent a SAT solver from solving for the same DIP over and over.

    copyTrgt    - Path to Z3 Python file describing circuit to be copied
    DIP         - Contains input literals & their values
    oracleOut   - Contains output literals corresponding to input literals
    inList      - Path to file containing list of variables designated as inputs in CNF, separated by lines or spaces
    keyList     - Path to file containing list of variables designated as key inputs in CNF, separated by lines or spaces
    outList     - Path to file containing list of variables designated as outputs in CNF, separated by lines or spaces
    miterFile   - Path to miter file to append circuit copy to
    suff        - Suffix appended to the end of variables to differentiate them from past entries in the miter file
    debug       - Debug mode: the previous miter circuit will be saved as a new file before modifying it, using
                    provided "suff" variable
    '''
    # Copy old miter circuit to new file if in troubleshoot mode
    if debug:
        oldVars,oldClauses = readZ3pl(miterFile)
        writeZ3pl(oldVars,oldClauses,debugDir+miterName+suff+'.py',prnt=True)

    # Read in template PL
    plVars,plClauses = readZ3pl(copyTrgt)
    
    # Make circuit copy pair
    coupleVars = {}
    coupleCopy = []
    for i in range(1,3):
        copy,copyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=f'{suff}_{i}',modIns=False,modKeys=False,modOuts=False)   # Nets are copy-unique
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=suff,modKeys=False,modNets=False)                            # Inputs & outputs are identical
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=f'_{i}',modIns=False,modNets=False,modOuts=False)      # Consistent keys
        coupleVars = coupleVars | {k:v for k,v in copyVars.items() if k not in coupleCopy}
        coupleCopy.extend(copy)

    # Assign I/O from oracle query
    ioList = DIP | oracleOut
    for var,val in ioList.items():
        if val == True:
            coupleCopy.append(f'{var}{suff} == True')
        elif val == False:
            coupleCopy.append(f'{var}{suff} == False')
        else:
            logging.error('Error encountered when appending constant I/O definition clauses to miter circuit')
            raise RuntimeError('Error encountered when appending constant I/O definition clauses to miter circuit')
        
    # Assign hiZ variables if applicable - they are tied to True, since oracle outputs should always be electrically driven
    # The phrasing of the implication 
    # NOTE: what if the oracle CAN exhibit a high-impedance output? Then this will need to be either changed such that the 
    # hiZ variables are assigned to the oracle's outputs... or hiZ flag should not be used at all and hiZ variables should be 
    # included in the outputs list
    if hiZVars != {}: 
        for var in hiZVars.values():
            coupleCopy.append(f'{var}{suff}_1 == True')
            coupleCopy.append(f'{var}{suff}_2 == True')

    writeZ3pl(coupleVars,coupleCopy,miterFile,append=True,prnt=debug)


def appendDIPCircuit(trgtPL:str,DIP:dict,oracleOut:list,inVars:list,keyVars:list,outVars:list,DIPCircuitFile:str,suff:str,tsVars={},debug=False):
    '''
    Append a circuit copy with specific I/O to a running file to be solved when all DIPs have been found. If the 
    file does not exist, it is created.

    trgtPL          - Filepath to CNF file containing clauses of a circuit to be copied
    DIP             - Contains input literals
    oracleOut       - Contains output literals corresponding to input literals
    DIPCircuitFile  - Filepath to file to append circuit copy to
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)
    
    # Make unique circuit copy with common key inputs
    DIPcopy, DIPcopyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=suff,modKeys=False)

    # Assign I/O
    ioList = DIP | oracleOut
    for var,val in ioList.items():
        if val == True:
            DIPcopy.append(f'{var}{suff} == True')
        elif val == False:
            DIPcopy.append(f'{var}{suff} == False')
    if tsVars != {}:      # NOTE: these lines need to be changed if hiZ is an expected output from the oracle
        for var in tsVars.values():
            DIPcopy.append(f'{var}{suff} == True')

    # Append circuit to file
    if os.path.exists(DIPCircuitFile):
        writeZ3pl(DIPcopyVars,DIPcopy,DIPCircuitFile,append=True)
    else:
        writeZ3pl(DIPcopyVars,DIPcopy,DIPCircuitFile,prnt=debug)


def createDIPCircuit(trgtPL:str,DIPs:list,oracleOuts:list,inVars:list,keyVars:list,outVars:list,DIPCircuitFile:str,tsVars={},debug=False):
    '''
    Append a circuit copy with specific I/O to a running file to be solved when all DIPs have been found. If the 
    file does not exist, it is created.

    trgtPL          - Filepath to CNF file containing clauses of a circuit to be copied
    DIP             - List of DIPs from attack rounds, where DIPs are stored as dicts
    oracleOut       - List of output patterns corresponding to input literals from attack rounds, where patterns are stored as dicts
    DIPCircuitFile  - Filepath to Python file containing all circuit copies.
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)

    copiesClauses = []
    copiesVars = {}
    for rnd,(DIP,outVec) in enumerate(zip(DIPs,oracleOuts)):
        suff=f'_cp{rnd}'
        # Make unique circuit copy with common key inputs
        DIPcopy, DIPcopyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=suff,modKeys=False)

        # Assign I/O
        ioList = DIP | outVec
        for var,val in ioList.items():
            if val == True:
                DIPcopy.append(f'{var}{suff} == True')
            elif val == False:
                DIPcopy.append(f'{var}{suff} == False')
        if tsVars != {}:      # NOTE: these lines need to be changed if hiZ is an expected output from the oracle
            for var in tsVars.values():
                DIPcopy.append(f'{var}{suff} == True')

        copiesClauses.extend(DIPcopy)
        copiesVars = copiesVars | DIPcopyVars

    writeZ3pl(copiesVars,copiesClauses,DIPCircuitFile,prnt=debug)


def satAttack(plLogicFile:str,ioCSV:str,oracleNetlist:str,topModule:str,noEarlyTermination=False,fresh=False,hiZOracle=True,pythonOracle=False,debug=False,quiet=False,recMiterFn=None,highImpedance=False):

    # Run argument parsing, directory creation, variable identification, and logging setup
    startTime = datetime.datetime.now()
    if recMiterFn == None:
        setup(plLogicFile,fresh,pythonOracle,quiet,debug)
    else:   # Recovery mode
        print('Running SAT attack in recovery mode. See log for more details.')
        fresh = False
        setup(plLogicFile,fresh,pythonOracle,quiet,debug)

    inVars = []
    keyVars = []
    outVars = []
    hiZVars = {}
    with open(ioCSV,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ioNm,ioAtts = row[0],row[1:]
            if ioAtts[0] == 'input':
                inVars.append(ioNm)
            elif ioAtts[0] == 'key':
                keyVars.append(ioNm)
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
    
    if recMiterFn == None:  # Create miter circuit
        miterFile = defMiterFile
        buildMiter(plLogicFile,inVars,keyVars,outVars,miterFile,mSuff=miterSuffix,hiZOracle=hiZOracle,hiZVars=hiZVars,debug=debug)
        logging.info(f'Miter logic successfully created and located at: {miterFile}')
    else:   # Recovery mode
        miterFile = recMiterFn
        logging.info(f'SAT attack running in recovery mode, using the user-provided miter file at: {miterFile}')

    # SAT attack loop
    iters = 1
    allDIPs = []
    allOuts = []
    while(True):
        # If 2^N rounds exceeded, the attack has failed to terminate correctly.
        if(iters > ((2**len(inVars))+1)):
            logging.error(f'Attack entering round {iters}, despite only a possible {2**len(inVars)} DIPs. Attack is improperly formulated. Please review and fix input files.')
            raise RuntimeError('All possible DIPs explored without expected attack termination. See log for details.')
        # We've already explored every I/O combination as a DIP, then we can be done early. No need for the final round, since it should return UNSAT (nothing new learned on that round).
        elif(iters > (2**len(inVars))) and noEarlyTermination:
            logging.warning(f'Attack entering round {iters}. All possible input patterns have been explored as DIPs. Since all information has been learned, and this round is expected to return UNSAT, this round will be skipped.')
            print('All possible input patterns have been explored as DIPs. Skipping ahead to key solve step...')
            break

        # Run SAT on miter & extract DIP if SAT
        print(f'\nRunning SAT on Miter clauses, round #{iters}.')
        sat,dip = runZ3(miterName,inVars)
        if not sat:         # Attack loop exit condition
            logging.info(f'Miter circuit UNSATISFIED at round #{iters}.')
            print('UNSAT')
            if iters == 1:  # The base Z3 model is unsatisfiable... you messed up
                logging.error(f'The provided encrytped logic file is unsatisfiable within itself. Please review and fix {plLogicFile}')
                raise RuntimeError('Base circuit unsatisfiable. See log for details.')
            break           # If no more DIPs, we're done
        logging.info(f'Miter circuit SATISFIED at round #{iters}. Extracted DIP: {dip}')
        print('SAT\nExtracted DIP:',*dip.items(),'\n',sep=' ')

        # Consult oracle
        oracleOut = queryOracle(dip,oracleNetlist,inVars,outVars,topLevelMod=topModule,trgtTb=tb,simOutFile=tbOutputFile)

        # Append circuit copies to the miter circuit file
        appendMiter(plLogicFile,dip,oracleOut,inVars,keyVars,outVars,miterFile,suff=f'_cp{iters}',debug=debug,hiZVars=hiZVars)

        # Append circuit copy to running "DIP circuits" CNF file with DIP and oracle output
        appendDIPCircuit(plLogicFile,dip,oracleOut,inVars,keyVars,outVars,dipCircuitsFile,suff=f'_cp{iters}',tsVars=hiZVars,debug=debug)

        # Compare latest DIP to past DIPs to see if there is a repeat. If so, throw & log error
        for pastIterMin1,pastDIP in enumerate(allDIPs):
            if ({} == {k: dip[k] for k in dip if k in pastDIP and dip[k] != pastDIP[k]}):   # If this DIP matches a previous one...
                logging.debug(f'The attack has revisited DIP {dip} in round {iters}. This DIP was first explored in round {pastIterMin1+1}. This is the first revisited DIP. The attack has not been formulated properly, and will now terminate early. Check the miter circuit.')
                raise RuntimeError('The attack has revisited a previously-explored DIP. See log for more details.')

        if debug:       # Checkpoint each round
            miterVars,miterCls = readZ3pl(miterFile)
            writeZ3pl(miterVars,miterCls,os.path.join(debugDir,'miter_final.py'),prnt=True)
        
        allDIPs.append(dip)
        allOuts.append(oracleOut)
        iters += 1

    # Run SAT on 'DIP Circuits' file
    #createDIPCircuit(plLogicFile,allDIPs,allOuts,inVars,keyVars,outVars,dipCircuitsFile,tsVars=hiZVars,debug=debug)
    print('\nRunning SAT on all extracted DIPS...')
    sat,key = runZ3(dipCircuitsName,keyVars)
    if not sat:
        logging.error('DIP Circuit UNSATISFIED - SAT ATTACK FAILED')
        print('DIP Circuit UNSATISFIED - SAT ATTACK FAILED')
        return -1

    # Save extracted key
    logging.info(f'Key extracted successfully to: {extractedKeyCSV}')
    if debug:
        print('Extracted key:')
        for i,j in sorted(key.items()):
                print(f'{i}\t:\t{j}')
    else:
        print(f'Key extracted successfully to: {extractedKeyCSV}')
    with open(extractedKeyCSV,'w') as f:
        writer = csv.writer(f,delimiter=',')
        writer.writerows(sorted(key.items()))

    # Wrap-up
    logging.info(f'{os.path.basename(__file__)} concluded. Total runtime: {datetime.datetime.now()-startTime} seconds')
    print(f'\nScript {os.path.basename(__file__)} concluded.\n')
    if quiet: enablePrint()
    return key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='satAttack',description='A tool for running SAT attacks on an encrypted netlist written in Z3 for Python')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('oracleNetlist',type=str,help='Path to the HDL netlist file for the unencrypted, oracle black box. Input and output names must coincide with what is found in the inputList and outputList files')
    parser.add_argument('topModule',type=str,help='Top-level module name within "oracleNetlist"')
    parser.add_argument('-e','--disableEarlyTermination',default=True,action='store_false',help='By default, skips the final (UNSAT) round of the attack if all possible inputs are explored as DIPs. Enable flag to go through final round regardless')
    parser.add_argument('-d','--debug',default=False,action='store_true',help='Creates intermediate scripts in a "debug" directory, for the purposes of troubleshooting when an attack goes awry')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-o','--oracleType',default=True,action='store_false',help='In cases where a circuit can express tri-state outputs, this indicates if the oracle can express HiZ outputs. Setting the flag indicates that the oracle cannot express HiZ outputs.')
    parser.add_argument('-p','--pythonOracle',default=False,action='store_true',help='If true, oraclenetlist points to a Python oracle file (alternative to using iVerilog). Oracle function must be declared as "main", and all input variable names must coincide with inputList')
    parser.add_argument('-q','--quiet',default=False,action='store_true',help='Prevent printing of SAT attack progress to terminal')
    parser.add_argument('-r','--recover',default=None,action='store',dest='recMiterFn',help='Set this flag and point to a running miter file (likely in a work/ directory)')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs = parser.parse_args()

    satAttack(clArgs.plLogicFile,clArgs.ioCSV,clArgs.oracleNetlist,clArgs.topModule,clArgs.disableEarlyTermination,clArgs.fresh,clArgs.oracleType,clArgs.pythonOracle,clArgs.debug,clArgs.quiet,clArgs.recMiterFn,clArgs.tristate)
