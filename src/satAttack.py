#!/usr/bin/env python3
'''
Script for running a SAT attack on encrypted circuits, described in Z3 
for Python, with an unencrypted oracle described in Verilog HDL.

Author:     Aric Fowler
Python:     3.10.6
Updated:    May 2023
'''
import os
import sys
import apt
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
logFormat = '%(asctime)s %(levelname)s: %(message)s\n'
logDateFormat = '%b-%d-%Y_%I-%M%p'
miterName = 'miter'
miterSuffix = '_m'
dipCircuitsName = 'dipCircuits'
tbName = 'tb.v'
tbOutputFile = 'vOut'

here = os.getcwd()
now = datetime.datetime.now().strftime(logDateFormat)

workDir = 'work' + '/'
logDir = 'log' + '/'

miterFile = os.path.join(here,workDir) + miterName + '.py'
dipCircuitsFile = os.path.join(here,workDir) + dipCircuitsName + '.py'
tb = os.path.join(here,workDir) + tbName
extractedKeyFile = os.path.join(here,workDir) + 'extracted_key.txt'


# -------------------------------------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------------------------------------


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
    if outDirName == '':
        outDirName = outDirName
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


def setup(plLogicFile,fresh,pythonOracle,verbosity):
    '''
    Parses input arguments, creates output and log directories, sets up logging, and elevates select
    variables to global scope.
    '''
    if not verbosity: blockPrint()
    print('Executing {}'.format(os.path.basename(__file__)))

    # Setup logging & output directories
    initDirs(workDir,logDir,freshDirs=fresh)
    logging.basicConfig(
        filename= os.path.join(here,logDir) + now + '.log',
        format=logFormat,
        datefmt=logDateFormat,
        level=logging.DEBUG)
    logging.info('SAT attack script called at: {}'.format(datetime.date.today()))
    logging.info('Target PL file: {}'.format(plLogicFile))
    logging.info('Output directories created.')

    sys.path.append(workDir)

    # Do a one-time check to ensure the I/O listed in the I/O text lists match the names 
    # found in the encrypted logic and the decrypted oracle netlist.
    logging.warning('Code does not currently support cross-checking I/O names found in text lists against netlist files. Please check manually.')

    # Check to see if iVerilog is installed if "-po" argument is not provided
    if pythonOracle is None:
        try:
            cache = apt.Cache()
            if cache['iverilog'].is_installed:
                pass
        except:
            print('It appears iVerilog is not installed. Running installation now...')
            returnCode = os.system('sudo apt install iverilog')
            if returnCode != 0:
                raise OSError('iVerilog was not successfully installed. Exiting SAT attack.')
            else:
                print('iVerilog was installed correctly. Proceeding with SAT attack...\n')


def readZ3pl(trgtZ3:str) -> Tuple[dict,list]:
    '''
    Read a Python Z3 script and parse the variable and function declarations, leaving out any 
    comment lines or Z3 Solver information. Returns dict of variables and a string of functions.
    '''
    varDict = {}
    funList = []
    with open(trgtZ3,'r') as f:
        f.seek(0)
        lines = f.readlines()

    # Search for variables
    for line in lines:
        mtchObj = re.match(r'^\s*(?P<varID>\w+)\s*=\s*(?P<varType>[a-zA-Z]+)\([\',"](?P<varName>\w+)[\',"]\).*$',line)
        if mtchObj:
            if (mtchObj.group('varID') != mtchObj.group('varName')):
                logging.error('Variable {name} is given a different identifier ("{id}") in the source Z3 Python script "{f}". Change this so they are identical.'.format(name=mtchObj.group('varName'),id=mtchObj.group('varID'),f=trgtZ3))
                raise RuntimeError('Variable mismatch name in "{}". See log file for details.'.format(trgtZ3))
            else:
                varDict[mtchObj.group('varID')] = mtchObj.group('varType')


    # Search for functions (logic clauses)
    for line in lines:
        mtchObj = re.match(r'^\s*(?P<funID>\w+)\s*=\s*(?P<fun>[^\'\"]*)\n$',line)     # Future work: there's gotta be a better RE to exclude "Solver"
        if mtchObj:
            if mtchObj.group('fun') != 'Solver()':
                funList.append(mtchObj.group('fun'))


    return varDict,funList


def writeZ3pl(z3Lines:list,z3Vars:dict,z3Fn:str,append=False) -> int:
    '''
    Writes or appends a Python Z3 script from a provided list of lines. If append is true, then
    writeZ3pl will read z3fileName and rewrite it, adding in additional clauses from z3Lines. 
    Assumes that the Python variable names and the PL variable names are identical. Returns 0 
    on success.
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
        f.write('from z3 import *\n\n\ndef main():\n')
        for var,varType in varList.items():
            f.write("\t{n} = {t}('{n}')\n".format(n=var,t=varType))
        f.write('\n')
        for i,line in enumerate(clauseList):
            clauseIndList.append('c{}'.format(i))
            f.write('\t{0} = {1}\n'.format(clauseIndList[i],line))
        f.write("\n\ts = Solver()\n\ts.add({})\n\ttry:\n\t\treturn s.check(), s.model()\n\texcept:\n\t\treturn s.check(), None\n\n\nif __name__ == '__main__':\n\tmain()".format(','.join(clauseIndList)))

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

    clauses = plClauses
    clauseVars = {k:v for k,v in allVars.items() if k not in changeList}
    for var in changeList.keys():
        newVar = var+suffix
        clauses = [re.sub(r'\b{}\b'.format(var),newVar,i) for i in clauses]
        clauseVars = clauseVars | {newVar: allVars[var]}

    return clauses,clauseVars


def buildMiter(trgtPL:str,inVars:list,keyVars:list,outVars:list,miterFile:str,mSuff='_m'):
    '''
    Create miter circuit for a given input CNF file. Returns a list of input variable names and a list key variable names for convenience.

    targetPL    - Path to Z3 Python file containing PL clauses to create a miter circuit out of
    inVars      - List of variables designated as inputs in targetPL, separated by lines or spaces
    keyVars     - List of variables designated as key inputs in targetPL, separated by lines or spaces
    outVars     - List of variables designated as outputs in targetPL, separated by lines or spaces
    miterFile   - Desired path, filename, and extension for output Z3 file
    mSuff       - Desired suffix to be added to net names for each miter circuit (do not include copy number)
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)

    # Create two copies of one circuit with identical inputs
    miterVars = {}
    miterClauses = []
    for i in range(1,3):
        copy,copyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=mSuff+str(i),modIns=False,modKeys=False)
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=('_'+str(i)),modIns=False,modOuts=False,modNets=False)
        miterVars = miterVars | {k:v for k,v in copyVars.items() if k not in miterClauses}
        miterClauses.extend(copy)

    # Build miter circuit - essentially a bitwise XOR operation followed by a reduction OR ("OR of XORs")
    outSubclauses = []
    for var in outVars:
        outSubclauses.append('Xor({0},{1})'.format(var+mSuff+'1',var+mSuff+'2'))
    miterClauses.append('Or({})'.format(','.join(outSubclauses)))

    writeZ3pl(miterClauses,miterVars,miterFile)


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
            voiVals = {k: modelVals[k] for k in set(voi).intersection(modelVals.keys())}
        else:
            voiVals = modelVals
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

    tbTemplate = '''// Testbench for iVerilog oracle. Automatically generated by Aric Fowler's SAT attack script.

`timescale 10ms/1ms

module tb();
    reg {inList};
    wire {outList};
    integer f;

    {cktName} dut({portDec});

    initial begin
        f = $fopen("{outputValueFile}","w");
        #1
        // Input assignment - DIP
{assignInValues}
        #1
{writeOutputs}
        $fclose(f);
    end

endmodule'''

    # Create explicit port declaration
    expPortDec = []
    for var in (inList + outList):
        expPortDec.append('.{port}({port})'.format(port=var))
    expPortDec = ','.join(expPortDec)

    ins = ','.join(inList)
    outs = ','.join(outList)


    # Format input assignment (for input assignment in testbench body)
    inputAssigns = []
    for var,val in inputStim.items():
        if val:
            inputAssigns.append("\t\t{vVar} <= 1'b{bVal};\n".format(vVar=var,bVal='1'))
        else:
            inputAssigns.append("\t\t{vVar} <= 1'b{bVal};\n".format(vVar=var,bVal='0'))


    # Format output value write
    outputWrites = []
    for var in outs.replace(' ','').split(','):
        outputWrites.append('\t\t$fwrite(f,"{var} : %b\\n",{var});\n'.format(var=var))
        
    # Write the testbench file
    with open(tb,'w') as f:
        f.write(tbTemplate.format(
            inList = ins,
            outList = outs,
            cktName = topLevelMod,
            portDec = expPortDec,
            outputValueFile = simOutFile,
            assignInValues = ''.join(inputAssigns),
            writeOutputs = ''.join(outputWrites)
            ))


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
    os.system('iverilog -c {}'.format(ivCmdFn))
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
            logging.error('Unable to properly parse iVerilog simulation output file "{}"'.format(simOutFn))

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


def appendMiter(copyTrgt:str,DIP:dict,oracleOut:dict,inVars:list,keyVars:list,outVars:list,miterFile:str,suff:str,ts=False):
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
    ts          - Troubleshoot mode: the previous miter circuit will be saved as a new file before modifying it, using
                    provided "suff" variable
    '''
    if ts:
        shutil.copy(miterFile,workDir+'miter'+suff+'.py')

    # Read in PL
    plVars,plClauses = readZ3pl(copyTrgt)
    
    # Make circuit copy pair
    coupleVars = {}
    coupleCopy = []
    for i in range(1,3):
        copy,copyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=suff+'_{}'.format(i),modIns=False,modKeys=False,modOuts=False)   # Nets are copy-unique
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=suff,modKeys=False,modNets=False)                                   # Inputs & outputs are identical
        copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix='_'+str(i),modIns=False,modNets=False,modOuts=False)                # Consistent keys
        coupleVars = coupleVars | {k:v for k,v in copyVars.items() if k not in coupleCopy}
        coupleCopy.extend(copy)

    # Assign I/O
    ioList = DIP | oracleOut         
    for var,val in ioList.items():
        if val == True:
            coupleCopy.append('{0}{1} == True'.format(str(var),suff))
        elif val == False:
            coupleCopy.append('{0}{1} == False'.format(str(var),suff))
        else:
            logging.error('Error encountered when appending constant I/O definition clauses to miter circuit')
            raise RuntimeError('Error encountered when appending constant I/O definition clauses to miter circuit')
        
    writeZ3pl(coupleCopy,coupleVars,miterFile,append=True)


def appendDIPCircuit(trgtPL:str,DIP:dict,oracleOut:list,inVars:list,keyVars:list,outVars:list,DIPCircuitFile:str,suff:str):
    '''
    Append a circuit copy with specific I/O to a running file to be solved when all DIPs have been found. If the 
    file does not exist, it is created.

    targetPL        - Filepath to CNF file containing clauses of a circuit to be copied
    DIP             - Contains input literals
    oracleOut       - Contains output literals corresponding to input literals
    DIPCircuitFile  - String. Filepath to file to append circuit copy to
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)
    
    # Make unique circuit copy with common key inputs
    DIPcopy, DIPcopyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=suff,modKeys=False)

    # Assign I/O
    ioList = DIP | oracleOut
    for var,val in ioList.items():
        if val == True:
            DIPcopy.append('{0}{1} == True'.format(str(var),suff))
        elif val == False:
            DIPcopy.append('{0}{1} == False'.format(str(var),suff))

    # Append circuit to file
    if os.path.exists(DIPCircuitFile):
        writeZ3pl(DIPcopy,DIPcopyVars,DIPCircuitFile,append=True)
    else:
        writeZ3pl(DIPcopy,DIPcopyVars,DIPCircuitFile)


def satAttack(plLogicFile:str,inputList:str,keyList:str,outputList:str,oracleNetlist:str,topModule:str,fresh=False,pythonOracle=False,troubleshoot=False,verbosity=True):

    # Run argument parsing, directory creation, and logging setup
    startTime = datetime.datetime.now()
    setup(plLogicFile,fresh,pythonOracle,verbosity)

    # Read in input lists & output list (.split() will get rid of spaces, tabs, and newlines)
    with open(inputList,'r') as f:
        inVars = f.read().split()
    with open(keyList,'r') as f:
        keyVars = f.read().split()
    with open(outputList,'r') as f:
        outVars = f.read().split()

    # Create miter circuit
    buildMiter(plLogicFile,inVars,keyVars,outVars,miterFile,mSuff=miterSuffix)
    logging.info('Miter logic successfully created. Miter CNF located at: {}'.format(miterFile))

    # SAT attack loop
    iters = 1
    while(True):
        
        # Run SAT on miter & extract DIP if SAT
        print('\nRunning SAT on Miter clauses, iteration #{}'.format(iters))
        sat,dip = runSAT(miterName,inVars)
        if not sat:
            logging.info('Miter circuit UNSATISFIED at iteration #{}'.format(iters))
            print('UNSAT')
            if iters == 1:
                logging.error('The provided encrytped logic file is unsatisfiable within itself. Please review and fix {}'.format(plLogicFile))
                raise RuntimeError('Base circuit unsatisfiable. See log for details.')
            break   # If no more DIPs; we're done 
        logging.info('Miter circuit SATISFIED at iteration #{0}. Extracted DIP:{1}'.format(iters,dip))
        print('SAT\nExtracted DIP:',*dip.items(),'\n',sep=' ')
        
        # Consult oracle
        oracleOut = queryOracle(dip,oracleNetlist,inVars,outVars,topLevelMod=topModule,trgtTb=tb,simOutFile=tbOutputFile)
        
        # Append circuit copies to the miter circuit file
        appendMiter(plLogicFile,dip,oracleOut,inVars,keyVars,outVars,miterFile,suff='_cp{}'.format(iters),ts=troubleshoot)
        
        # Append circuit copy to running "DIP circuits" CNF file with DIP and oracle output
        appendDIPCircuit(plLogicFile,dip,oracleOut,inVars,keyVars,outVars,dipCircuitsFile,suff='_cp{}'.format(iters))

        iters += 1

    # Run SAT on 'DIP Circuits' file
    print('\nRunning SAT on all extracted DIPS...')
    sat,key = runSAT(dipCircuitsName,keyVars)
    if not sat:
        logging.error('DIP Circuit UNSATISFIED - SAT ATTACK FAILED')
        print('DIP Circuit UNSATISFIED - SAT ATTACK FAILED')
        return -1

    logging.info('Key extracted successfully: {}'.format(key))
    print('Extracted key:')
    with open(extractedKeyFile,'w') as f:
        for i,j in sorted(key.items()):
            kiPair = '{0}   :   {1}'.format(i,j)
            f.write(kiPair+'\n')
            print(kiPair)

    # Wrap-up
    logging.info('Script concluded. Total runtime: {} seconds'.format(datetime.datetime.now()-startTime))
    if not verbosity: enablePrint()
    return key


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tool for running SAT attacks on an encrypted netlist written in Z3 for Python.')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('inputList',type=str,help='Path to the text file containing a list of inputs to the plLogicFile. Inputs must be separated by a space or newline character')
    parser.add_argument('keyList',type=str,help='Path to the text file containing a list of key inputs to the plLogicFile. Keys must be separated by a space or newline character')
    parser.add_argument('outputList',type=str,help='Path to the text file containing a list of outputs to the plLogicFile. Outputs must be separated by a space or newline character')
    parser.add_argument('oracleNetlist',type=str,help='Name + extension of the HDL netlist file for the unencrypted, oracle black box. Input and output names must coincide with what is found in the inputList and outputList files')
    parser.add_argument('topModule',type=str,help='Top-level module name within "oracleNetlist"')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-po','--pythonOracle',default=False,action='store_true',help='If true, oraclenetlist points to a Python oracle file (alternative to using iVerilog). Oracle function must be declared as "main", and all input variable names must coincide with inputList')
    parser.add_argument('-t','--troubleshoot',default=False,action='store_true',help='Creates intermediate scripts for the purposes of troubleshooting when an attack goes awry.')
    parser.add_argument('-v','--verbosity',default=False,action='store_true',help='Print progress of SAT attack to terminal')
    clArgs=parser.parse_args()

    satAttack(clArgs.plLogicFile,clArgs.inputList,clArgs.keyList,clArgs.outputList,clArgs.oracleNetlist,clArgs.topModule,clArgs.fresh,clArgs.pythonOracle,clArgs.troubleshoot,clArgs.verbosity)
