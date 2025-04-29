#!/usr/bin/env python3
'''
Author:     Aric Fowler
Python:     3.10.12
Updated:    Sept 2024
'''
import os
import sys
import logging
import re
import argparse
import shutil
import glob
import subprocess
import datetime
from typing import Tuple

# ----------------
# GLOBALS
# ----------------
# from .globals import *       # TRANSAT common global variables
logName = 'abcAttack'
logFormat = '%(asctime)s %(levelname)s: %(message)s\n'
logDateFormat = '%b-%d-%Y_%I-%M%p'
logDir = 'log/'
workDir = 'work/'

here = os.getcwd()
now = datetime.datetime.now().strftime(logDateFormat)

miterModName = 'miter'
tbName = 'tb.v'
tbOutputFile = 'vOut'
tb = os.path.join(here,workDir) + tbName


# ----------------
# FUNCTIONS
# ----------------
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


def readVerilog(trgtV:str) -> Tuple[dict,list,str]:
    '''
    Reads structural Verilog and parses the variable and function declarations, leaving out any 
    comment lines. Returns dict of variables, lines with gate descriptions or comments, and the 
    top-level module
    '''
    modName = None
    varsDict = {}
    funList = []
    with open(trgtV,'r') as f:
        f.seek(0)
        lines = f.readlines()

    for line in lines:
        moduleMtch = re.match(r'^module\s+(?P<modName>\w+)\s*\(.*\);',line,re.IGNORECASE)
        keyInMtch = re.match(r'^\s*input\s+(?P<vars>.+)\s*;\s*//\s*key.*',line,re.IGNORECASE)
        inMtch = re.match(r'^\s*input\s+(?P<vars>.+)\s*;.*',line)
        outMtch = re.match(r'^\s*output\s+(?P<vars>.+)\s*;.*',line)
        netMtch = re.match(r'^\s*wire\s+(?P<vars>.+)\s*;.*',line)
        gateMtch = re.match(r'^\s*(?P<gate>(and|or|nand|nor|xor|xnor|not)\([a-zA-Z0-9_,\s]*\))',line)
        # commentMtch = re.match(r'^\s*//.*$',line)
        if keyInMtch:       # Extract key inputs
            for var in re.findall(r'\b(?!input)\w+\b(?=.*;)',line):
                varsDict[var] = 'key'
        elif inMtch:        # Extract primary inputs
            for var in re.findall(r'\b(?!input)\w+\b(?=.*;)',line):
                varsDict[var] = 'input'
        elif outMtch:       # Extract outputs
            for var in re.findall(r'\b(?!output)\w+\b(?=.*;)',line):
                varsDict[var] = 'output'
        elif netMtch:
            for var in re.findall(r'\b(?!wire)\w+\b(?=.*;)',line):
                varsDict[var] = 'wire'
        elif gateMtch:
            funList.append(gateMtch.group('gate'))
        # elif commentMtch:
        #     funList.append(line)
        elif moduleMtch:
            modName = moduleMtch.group('modName')

    return varsDict,funList,modName


def copyVerilog(vars:dict,gates:list,suffix:str,dupKeys=(False,'_',range(1),0),modIns=False,modOuts=False,modNets=False) -> Tuple[dict,list]:
    '''
    Creates a copy of a gate-level Verilog description.
    '''
    newVars = {}
    varMap = dict.fromkeys(vars.keys())

    # Modify variables
    for var,varType in vars.items():
        if modIns and varType == 'input':
            newVar = f'{var}{suffix}'
            varMap[var] = newVar
            newVars[newVar] = 'input'
        elif modOuts and varType == 'output':
            newVar = f'{var}{suffix}'
            varMap[var] = newVar
            newVars[newVar] = 'output'
        elif modNets and varType == 'wire':
            newVar = f'{var}{suffix}'
            varMap[var] = newVar
            newVars[newVar] = 'wire'
        elif dupKeys[0] == True and varType == 'key':
            varMap[var] = f'{var}{dupKeys[1]}{dupKeys[3]}'
            for i in dupKeys[2]:
                newVars[f'{var}{dupKeys[1]}{i}'] = 'key'
        else:
            varMap[var] = var
            newVars[var] = vars[var]

    # Modify gates
    newGates = '\n'.join(gates)

    for var in vars.keys():
        newGates = re.sub(r'\b{}\b'.format(re.escape(var)),varMap[var],newGates)

    newGates = newGates.split('\n')

    return newVars,newGates


def writeVerilog(vars:dict,gates:list,modName:str,outputPath='./verilog.v'):
    '''
    Write a gate-level Verilog description.
    '''
    ioList = ','.join([x for x in vars.keys() if vars[x] == 'input'] + [x for x in vars.keys() if vars[x] == 'key'] + [x for x in vars.keys() if vars[x] == 'output'])
    inVars = ','.join([x for x in vars.keys() if vars[x] == 'input'])
    keyVars = ','.join([x for x in vars.keys() if vars[x] == 'key'])
    outVars = ','.join([x for x in vars.keys() if vars[x] == 'output'])
    netVars = ','.join([x for x in vars.keys() if vars[x] == 'wire'])

    with open(outputPath,'w') as f:
        f.write(f'// Module {modName}\nmodule {modName} ({ioList});\n')
        f.write(f'\tinput {inVars};\n')
        f.write(f'\tinput {keyVars};\t// Key variables\n')
        f.write(f'\toutput {outVars};\n\n')
        f.write(f'\twire {netVars};\n\n')
        for line in gates:
            f.write(f'\t{line};\n')
        f.write('\n\nendmodule')

    return 
        

def initMiterHalves(vars:dict,gateDefs:list,modName:str,location:str) -> Tuple[str,str,dict]:
    '''
    Creates two separate Verilog file copies, each with separate keys but 
    identical primary I/O. Returns full paths for two Verilog files.

    vars        - Dictionary of all nets, including I/O, with designation
    gateDefs    - List of all gates within structural Verilog
    modName     - Base name for top-level module and file name
    location    - Path where output Verilog miter files will be created
    '''
    suffixBase = '_'
    miterPath = [None]*2
    for m in range(2):
        miterPath[m] = f'{location}miterHalf{m}.v'
        cpyVars, cpyGates = copyVerilog(vars,gateDefs,suffix=f'{suffixBase}{m}',dupKeys=(True,suffixBase,range(2),m),modIns=False,modOuts=False,modNets=False)

        writeVerilog(cpyVars,cpyGates,modName,miterPath[m])

    return miterPath[0],miterPath[1],cpyVars


def runBerkSAT(miterHalf1:str,miterHalf2:str,runDir:str,vars:dict,fraig=True,resultFn='miterResult.txt') -> Tuple[bool,dict]:
    '''
    Run a miter problem through SAT using ABC, return SAT results
    '''
    abcScipt = f'{runDir}abcMiterScript'
    outFile = f'{runDir}{resultFn}'
    with open(abcScipt,'w') as f:
        f.write(f'miter {miterHalf1} {miterHalf2}\n')
        if fraig:
            f.write(f'iprove -L {outFile}')
        else:
            f.write(f'iprove -f -L {outFile}')

    try:
        subprocess.run(['abc','-f',abcScipt,'-o',outFile])

        with open(outFile,'r') as f:
            lines = f.readlines()
        if re.match(r'snl_SAT',lines[0]):
            varVals = {k:None for k in sorted(vars.keys()) if (vars[k] == 'input' or vars[k] == 'key')}
            decision = True
            vals = list(lines[2])               # This is alphabetized
            for i,var in enumerate(varVals.keys()):
                varVals[var] = vals[i]
        else:
            decision = False
            varVals = None

        return decision, varVals
    except:
        raise RuntimeError('Attack failed when calling ABC. ABC may not be installed. Install from: https://github.com/berkeley-abc/abc')


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


def buildTestbench(inputStim:dict,tb:str,inList:list,outList:list,topLevelMod='top',simOutFile=tbOutputFile):
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
        if var not in inList:
            pass
        elif val == '1':
            inputAssigns.append(f"\t\t{var} <= 1'b1;\n")
        elif val == '0':
            inputAssigns.append(f"\t\t{var} <= 1'b0;\n")
        else:
            raise RuntimeError('An input variable has ')


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


def runiVerilog(cktIn:dict,trgtNetlist:str,topLevelMod:str,inList:list,outList:list,trgtTb=str,simOutFn=str,ivCmdFn='iv_cmd_file') -> dict:
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
            raise RuntimeError(f'Unable to properly parse iVerilog simulation output file "{simOutFn}"')

    # Delete extraneous files: a.out, iv file, testbench, simOut text file
    os.remove('a.out')
    os.remove(ivCmdFn)
    os.remove(trgtTb)
    os.remove(simOutFn)

    return cktOut


def runPyOracle(oracleIns:dict,oracleFile:str) -> dict:
    '''
    Run Python oracle script.

    There's nothing here yet!
    '''
    raise RuntimeError('Whoops, using a Python oracle is not currently supported. Use a Verilog one instead.')


def queryOracle(oracleFile:str,topLevelMod:str,vars:dict,queryVals:dict,trgtTb='',simOutFile='',oracleSel=False) -> dict:
    '''
    Function for selecting desired oracle query method. Returns oracle outputs as a dict.

    oracleIns   - Values for inputs to query oracle with.
    topLevelMod - Name of top level mod in Verilog file. Necessary only if oracleSel = False.
    oracleSel   - If true, indicates that oracleFile is a Python file instead of a Verilog file.
    '''
    vars,gates,name = readVerilog(oracleFile)
    inVars = [x for x in vars if vars[x] == 'input']
    outVars = [x for x in vars if vars[x] == 'output']
    if not oracleSel and trgtTb != '' and simOutFile != '':
        ivCmdFile = os.path.join(here,workDir) + 'iv_cmd_file'
        oracleOut = runiVerilog(queryVals,oracleFile,name,inVars,outVars,trgtTb,simOutFile,ivCmdFn=ivCmdFile)
    elif not oracleSel:
        raise RuntimeError('Missing arguments for using an iVerilog oracle testbench.')
    else:
        oracleOut = runPyOracle()

    return oracleOut


def appendMiter(origVars:dict,origGates:list,dip:dict,outVals:dict,miterFiles:tuple,round:int,modName:str,location:str) -> Tuple[str,str]:
    '''
    Create new miter halves using the new information gained from the previously-discovered DIP
    '''
    if len(miterFiles) != 2:
        raise RuntimeError(f'Two miter files expected, {len(miterFiles)} received.')
    suffixBase = '_c'
    cpyASuff = f'{suffixBase}{round}A'
    cpyBSuff = f'{suffixBase}{round}B'
    intSuff = '_int'                # Intermediate output suffix needed for injecting outputs

    for m in miterFiles:
        prevVars, prevGates, prevName = readVerilog(m)
        newVars = {}
        newGates = []

        # 1. For each output, create intermediate output and modify output gates, if not done already
        for out in outVals.keys():
            if not f'{out}{intSuff}' in prevVars.keys():
                newVars[f'{out}{intSuff}'] = 'wire'
                for ind,gate in enumerate(prevGates):
                    prevGates[ind] = re.sub(r'\b{}\b'.format(re.escape(out)),f'{out}{intSuff}',gate)

        # 2. For each input (read from DIPs), add clauses and variables to force a new wire high/low
        for var in dip.keys():
            newVars[f'{var}{suffixBase}{round}'] = 'wire'
            newVars[f'{var}N{suffixBase}{round}'] = 'wire'
            newGates.append(f'not({var}N{suffixBase}{round},{var})')
            if dip[var] == '0':
                newGates.append(f'and({var}{suffixBase}{round},{var},{var}N{suffixBase}{round})')
            else:
                newGates.append(f'or({var}{suffixBase}{round},{var},{var}N{suffixBase}{round})')

        # 3. Create 2 circuit copies that takes in forced same inputs, each gets an original key, has new unique output
        cpyVars, cpyGates = copyVerilog(origVars,origGates,f'{suffixBase}{round}',dupKeys=(False,None,None,None),modIns=True,modOuts=False,modNets=False)
        for var in cpyVars.keys():                          # Copy outputs are actually wires
            if cpyVars[var] == 'output':
                cpyVars[var] = 'wire'
        cpyAVars, cpyAGates = copyVerilog(cpyVars,cpyGates,cpyASuff,dupKeys=(True,'_',range(2),0),modIns=False,modOuts=True,modNets=True)
        cpyBVars, cpyBGates = copyVerilog(cpyVars,cpyGates,cpyBSuff,dupKeys=(True,'_',range(2),1),modIns=False,modOuts=True,modNets=True)

        for out,outVal in outVals.items():                  # Invert output if it is expected to be a '0'
            if outVal == False:
                newInvVar = f'{out}{cpyASuff}Inv'
                for ind,line in enumerate(cpyAGates):
                    cpyAGates[ind] = re.sub(r'\b{}\b'.format(f'{out}{cpyASuff}'),newInvVar,line)
                cpyAVars[newInvVar] = 'wire'
                cpyAGates.append(f'not({out}{cpyASuff},{newInvVar})')
                newInvVar = f'{out}{cpyBSuff}Inv'
                for ind,line in enumerate(cpyBGates):
                    cpyBGates[ind] = re.sub(r'\b{}\b'.format(f'{out}{cpyBSuff}'),newInvVar,line)
                cpyBVars[newInvVar] = 'wire'
                cpyBGates.append(f'not({out}{cpyBSuff},{newInvVar})')

        # 4. AND together copy outputs with original output
        for out in outVals.keys():
            for ind,gate in enumerate(prevGates):   # Remove the old AND of all copy outputs
                if re.match(r'(and|or|nand|nor|xor|xnor|not)\(\b{}\b'.format(re.escape(out)),gate):
                    prevGates.pop(ind)
                
            allInstOuts = [f'{out}{intSuff}']       # Create new AND of all copy outputs
            for i in range(round):
                allInstOuts.extend([f'{out}{suffixBase}{i+1}A',f'{out}{suffixBase}{i+1}B'])
            allInstOuts = ','.join(allInstOuts)
            newGates.append(f'and({out},{allInstOuts})')

        

        allVars = prevVars | cpyAVars | cpyBVars | newVars
        allGates = prevGates + [f'// Circuit copy {round}A'] + cpyAGates + [f'// Circuit copy {round}B'] + cpyBGates + [f'// DIP prep and output AND'] + newGates

        writeVerilog(allVars,allGates,modName,m)

    return miterFiles


def initKeySolveHalves(vars:dict,gateDefs:list,dipsList:list,oracleOutList:list,location:str) -> Tuple[str,str]:
    '''
    Formulate key solve step in the context of a miter problem for ABC.
    '''
    # Create circuit 1 - all circuit copies
    f1 = f'{location}keySolveHalf1.v'
    suffixBase = '_c'
    allVars = {}
    allGates = []
    allCpyOuts = {}
    for i,dip in enumerate(dipsList):
        cpyVars, cpyGates = copyVerilog(vars,gateDefs,suffix=f'{suffixBase}{i}',dupKeys=(False,None,None,None),modIns=True,modOuts=True,modNets=True)
        allVars = allVars | cpyVars
        allGates.extend(cpyGates+[f'// End of copy {i}'])
        for var,varVal in dip.items():
            newInvVar = f'{var}Inv{suffixBase}{i}'
            allVars[newInvVar] = 'wire'
            allVars[f'{var}{suffixBase}{i}'] = 'wire'
            allGates.append(f'not({newInvVar},{var})')
            if varVal == '1':   # Expected input needs to be a '1'
                allGates.append(f'or({var}{suffixBase}{i},{newInvVar},{var})')
            else:               # Expected input needs to be a '0'
                allGates.append(f'and({var}{suffixBase}{i},{newInvVar},{var})')
        for var,varVal in oracleOutList[i].items():
            if varVal:      # Expect output to be '1'
                allCpyOuts[f'{var}{suffixBase}{i}'] = var
            else:           # Expect output to be '0'
                newInvVar = f'{var}{suffixBase}{i}inv'
                allVars[newInvVar] = 'wire'
                allGates.append(f'not({newInvVar},{var}{suffixBase}{i})')
                allCpyOuts[newInvVar] = var
        for var,varType in allVars.items():
            if varType == 'output':
                allVars[var] = 'wire'
    allVars = allVars | {k:v for k,v in vars.items() if vars[k] == 'input'}
    for var in oracleOutList[0].keys(): # Finally create big AND with an output for each unique output across all circuit copies
        allVars[var] = 'output'
        allGates.append(f'and({var},{",".join([x for x in allCpyOuts.keys() if allCpyOuts[x] == var])})')

    writeVerilog(allVars,allGates,'keySolveHalf1',f1)

    # Create circuit 2 - hard 0 (the miter problem will be forced to satisfy output values in circuit 1 that are AND'd together)
    f2 = f'{location}keySolveHalf2.v'
    allVars = {k:v for k,v in vars.items() if v != 'wire'}
    allGates = []
    dummyIn = [k for k,v in vars.items() if v == 'input'][0]
    newInvVar = f'{dummyIn}Inv'
    allVars[newInvVar] = 'wire'
    allGates.append(f'not({newInvVar},{dummyIn})')
    for var in [k for k,v in vars.items() if v == 'output']:
        allGates.append(f'and({var},{newInvVar},{dummyIn})')
    
    writeVerilog(allVars,allGates,'keySolveHalf2',f2)

    return f1,f2

# ----------------
# MAIN
# ----------------
def abcAttack(encV,orcV,fresh,fraig):
    '''
    Runs a SAT attack on some gate-level Verilog for a locked circuit, against 
    an oracle unlocked Verilog circuit.
    '''
    startTime = datetime.datetime.now()
    print('Running ABC-based SAT attack...')
    initDirs(workDir,logDir,fresh)
    logging.basicConfig(
        filename= os.path.join(here,logDir)+logName+'_'+now+'.log',
        format=logFormat,
        datefmt=logDateFormat,
        level=logging.DEBUG)
    logging.info(f'SAT attack script called at: {datetime.datetime.now()}')
    logging.info(f'Target encrypted Verilog file: {encV}')
    logging.warning('This attack is meant for the purposes of comparison to the "standard" Z3-based attack included in this package. Please use the Z3 attack for fastest times.')

    sys.path.append(workDir)

    # Read I/O
    vars,gates,modName = readVerilog(encV)
    orcVars,orcGates,orcName = readVerilog(orcV)
    ins = [x for x in vars if vars[x] == 'input']
    keys = [x for x in vars if vars[x] == 'key']

    # Create two copies of locked circuit, freezing inputs, outputs, internal nets. Must create double keys and provide to both (dumb I know)
    miterFile1,miterFile2,miterVars = initMiterHalves(vars,gates,miterModName,workDir)
    
    iters = 1
    dipsList = []
    oracleOutList = []
    print(f'\nRunning SAT on Miter clauses, round #{iters}.')
    sat,valAssigns = runBerkSAT(miterFile1,miterFile2,workDir,miterVars)

    while(sat):
        dip = dict([(k,v) for k,v in valAssigns.items() if k in ins])
        logging.info(f'Miter circuit SATISFIED at round #{iters}. Extracted DIP: {dip}')
        print(f'Miter circuit SATISFIED at round #{iters}. Extracted DIP: {dip}')
        if dip in dipsList:
            logging.debug(f'The attack has revisited DIP {dip} in round {iters}. This is the first revisited DIP. The attack has not been formulated properly, and will now terminate early. Check the miter circuit.')
            raise RuntimeError('DIP revisited - please check input files')
        dipsList.append(dip)

        # Feed ABC results to iVerilog
        oracleOut = queryOracle(orcV,orcName,orcVars,valAssigns,trgtTb=tb,simOutFile=tbOutputFile)
        print(f'\nOracle queried for round #{iters} DIP. Oracle response: {oracleOut}')
        oracleOutList.append(oracleOut)

        # Append circuit copies to two copies of circuit files
        miterFile1,miterFile2 = appendMiter(vars,gates,dip,oracleOut,(miterFile1,miterFile2),iters,miterModName,workDir)

        iters += 1
        print(f'\nRunning SAT on Miter clauses, round #{iters}.')
        sat,valAssigns = runBerkSAT(miterFile1,miterFile2,workDir,miterVars,fraig=fraig)

    logging.info(f'Miter circuit UNSATISFIED at round #{iters}.')
    print(f'Miter circuit UNSATISFIED at round #{iters}.')
    print('\nProceeding to key solve step...')

    # SAT solve step - create a bunch of circuit copies in Verilog, send the to ABC to be turned into CNF, then call MiniSAT on the CNF
    f1,f2 = initKeySolveHalves(vars,gates,dipsList,oracleOutList,workDir)
    sat, valAssigns = runBerkSAT(f1,f2,workDir,vars)
    key = {k:v for k,v in valAssigns.items() if k in keys}

    if sat:
        logging.info(f'SAT attack completed. Extracted key: {key}')
        print(f'SAT attack completed. Total runtime: {datetime.datetime.now() - startTime}')
    else:
        logging.error(f'SAT solve step failed. Please review {f1}, {f2}')
        raise RuntimeError(f'SAT solve step failed. Please review {f1}, {f2}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A SAT attack script built around MiniSAT, iVerilog, and the verification capabilities of ABC')
    parser.add_argument('encVerilog',type=str,help='Path to Verilog file describing encrypted circuit')
    parser.add_argument('orcVerilog',type=str,help='Path to Verilog file describing unencrypted circuit (oracle)')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Creates fresh working and log directories upon calling this script')
    parser.add_argument('-g','--fraig',default=True,action='store_false',help='Disable fraiging capabilities of ABC solver (on by default)')
    clArgs= parser.parse_args()

    abcAttack(clArgs.encVerilog,clArgs.orcVerilog,clArgs.fresh,clArgs.fraig)
