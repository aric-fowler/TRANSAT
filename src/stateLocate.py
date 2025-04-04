#!/usr/bin/env python3
import sys
import csv
import re
import z3
import shutil
import glob
import importlib
import argparse
import logging
import copy
from typing import Tuple
from collections import deque

# -------------------------------------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------------------------------------
from .globals import *      # TRANSAT common global variables
logName = 'stateFinder'
miterName = 'stateFinderMiter'
miterSuffix = '_m'

miterFile = os.path.join(here,workDir) + miterName + '.py'


# -------------------------------------------------------------------------------------------------
# Classes & Functions
# -------------------------------------------------------------------------------------------------
class NetlistGraph:
    '''
    Directed graph object for a Z3 netlist

    rGraph - Reverse graph, outputs point to inputs
    fGraph - Forward graph, inputs point to outputs. Transpose of rGraph
    '''
    def __init__(self,z3Nets:list,z3Clauses:list):
        '''
        Constructor for NetlistGraph. Creates a directed graph from input Z3 clause list
        '''
        self.vertices = []
        self.rGraph = {k : [] for k in z3Nets}
        self.fGraph = {k : [] for k in z3Nets}

        for lineNum,line in enumerate(z3Clauses):
            impMtch = re.match(r'Implies\((?P<condExpr>.+)\s*,\s*\(?(?P<impExpr>.+)\)+',line,re.DOTALL)         # Match implication statement (e.g. transistor switches, tri-state buffers)
            eqMtch = re.match(r'\(?\s*(?P<lftExpr>(?!Implies).+)\s*==\s*(?P<rhtExpr>.+)\s*\)?',line,re.DOTALL)  # Match equivalence (e.g. logic gates, direct wire taps)

            if impMtch:
                # condVars = re.findall(r'\b(?!And\b|Not\b|Or\b|Xor\b)\w+\b',impMtch.group('condExpr'))
                implied = re.match(r'\(?\s*(?P<lftExpr>.+)\s*==\s*(?P<rhtExpr>.+)\s*\)?',impMtch.group('impExpr'),re.DOTALL)    # Implied expression
                lftVars = re.findall(r'\b(?!And\b|Not\b|Or\b|Xor\b)\w+\b',implied.group('lftExpr'))
                rhtVars = re.findall(r'\b(?!And\b|Not\b|Or\b|Xor\b)\w+\b',implied.group('rhtExpr'))

                # Left side has output
                if re.match(r'\b(And|Not|Or|Xor)\b',implied.group('rhtExpr')) and re.match(r'(?!And|Not|Or|Xor).*',implied.group('lftExpr')):
                    self.__addEdge(lftVars[0],rhtVars)
                # Right side has output
                elif re.match(r'\b(And|Not|Or|Xor)\b',implied.group('lftExpr')) and re.match(r'(?!And|Not|Or|Xor).*',implied.group('rhtExpr')):
                    self.__addEdge(rhtVars[0],lftVars)
                # Bidirection - either side can be an input
                elif re.match(r'(?!And|Not|Or|Xor).*',implied.group('lftExpr')) and re.match(r'(?!And|Not|Or|Xor).*',implied.group('rhtExpr')):
                    # How do we determine direction for transistors? You can't go both ways or DFS will detect a 
                    # loop and return a state-holding net at one of the two ends
                    logging.warning(f'Bidirectional implication detected on line {lineNum}, no action taken')
                else:
                    logging.warning(f'Unable to parse implication line: {lineNum}')

                # Count conditional inputs (condVars) as inputs

            elif eqMtch:
                lftVars = re.findall(r'\b(?!And\b|Not\b|Or\b|Xor\b)\w+\b',eqMtch.group('lftExpr'))
                rhtVars = re.findall(r'\b(?!And\b|Not\b|Or\b|Xor\b)\w+\b',eqMtch.group('rhtExpr'))
                if re.match(r'\b(And|Not|Or|Xor)\b',eqMtch.group('rhtExpr')) and re.match(r'(?!And|Not|Or|Xor).*',eqMtch.group('lftExpr')):   # Left side has ouptut
                    self.__addEdge(lftVars[0],rhtVars)
                elif re.match(r'\b(And|Not|Or|Xor)\b',eqMtch.group('lftExpr')) and re.match(r'(?!And|Not|Or|Xor).*',eqMtch.group('rhtExpr')): # Right side has output
                    self.__addEdge(rhtVars[0],lftVars)
                else:
                    logging.warning(f'Unable to parse equivalence line: {lineNum}')

            else:
                logging.warning(f'Unable to interpret or parse line: {lineNum}')

        self.tarjanSCC()


    def __addVertex(self,v) -> None:
        if type(v) != list:
            self.vertices.append(v)
        else:
            self.vertices.extend([x for x in list(v) if x not in self.vertices])


    def __addEdge(self,v,w:list) -> None:
        '''
        Add edges to the directed graph and its transpose if the edge does
        not already exist.
        v   -   Graph node new edges are pointing from
        w   -   List of graph nodes new edges are pointing to
        '''
        self.__addVertex(v)
        self.__addVertex(w)
        self.rGraph[v].extend([x for x in w if x not in self.rGraph[v]])

        for y in w:
            self.fGraph[y].append(v)


    def prntGraph(self):
        '''
        Print the current stored graph to the command terminal
        '''
        for v in self.rGraph:
            print(f'{v} -> {self.rGraph[v]}')


    def reportSCCs(self,mxLps=False,excl=True) -> list:
        '''
        Return list of strongly-connected components

        excl    -   Exclude SCCs that consist of only a single node
        '''
        if excl:
            return [x for x in self._sccs if (len(x) > 1)]
        else:
            return self._sccs


    def __strongConnect(self,v):
        vInitInd = self._lowLink[v] = self._index
        self._index += 1
        self._stack.append(v)
        self._visited.add(v)

        # Consider neighbors of v through recursive DFS
        for w in self.fGraph[v]:
            if w not in self._lowLink:  # Neighbor has not yet been visited 
                self.__strongConnect(w)
                self._lowLink[v] = min(self._lowLink[v],self._lowLink[w])
            elif w in self._stack:      # Neighbor is in stack and hence in current SCC
                self._lowLink[v] = min(self._lowLink[v],self._lowLink[w])
            # If not in stack, neighbor belongs to a different SCC - ignore it

        # If v is a root node, pop stack and generate SCC
        if self._lowLink[v] == vInitInd:
            scc = []
            while(True):
                u = self._stack.pop()
                scc.append(u)
                if u == v:
                    break
            self._sccs.append(scc)


    def tarjanSCC(self):
        '''
        Tarjan's Algorithm - produce groups of strongly-connected components (SCCs)
        '''
        self._sccs = []
        self._index = 0
        self._lowLink = {}
        self._stack = []
        self._visited = set()
        for v in self.fGraph.keys():
            if v not in self._lowLink:
                self.__strongConnect(v)


    def _bfsMinimumCycles(self,subGraph:list) -> dict:
        '''
        Perform breadth-first search on an ordered graph (assumed to be an SCC) to find 
        all cycles that do not contain a smaller cycle within them

        Returns a dict of revisited nodes and a list of all nodes included in the cycle
        '''
        prohibitedRevisits = []
        queue = deque([subGraph[0]])                # Start arbitrarily with first listed vertex
        visited = {subGraph[0]: [subGraph[0]]}
        fdbkCycles = {}
        while queue:                                # While length of queue is not 0...
            x = queue.popleft()                     # Remove from left of FIFO
            for y in self.fGraph[x]:
                trail = copy.deepcopy(visited[x])
                if (y not in visited.keys()) and (y in subGraph):                                   # If net 'y' has not been visited...
                    visited[y] = trail+[y]
                    queue.append(y)                 # Insert on right of FIFO
                elif (y in visited.keys()) and (y in subGraph) and (y not in prohibitedRevisits):   # Revisited net 'y' indicates a cycle
                    prohibitedRevisits.extend([x for x in trail if x not in prohibitedRevisits])
                    cycle = [y]                     # Initialize cycle
                    stack = trail                   # Initialize stack
                    while stack[-1] != y:
                        cycle.append(stack.pop())
                    fdbkCycles[x] = cycle

        return fdbkCycles


    def minimalCycles(self) -> dict:
        '''
        Find the cycles within an SCC in the graph that do not contain a smaller internal graph.
        '''
        minCycles = {}
        for scc in self.reportSCCs(mxLps=True):     # For each SCC that has more than one vertex in it...
            minCycles = minCycles | self._bfsMinimumCycles(scc)
        
        return minCycles   


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


def setup(plLogicFile,fresh=False,debug=False):
    '''
    Parses input arguments, creates output and log directories, sets up logging, and elevates select
    variables to global scope.
    '''
    print(f'Executing {os.path.basename(__file__)}...')

    # Setup logging & output directories
    initDirs(workDir,logDir,freshDirs=fresh,debug=debug)
    logging.basicConfig(
        filename= os.path.join(here,logDir)+logName+'_'+now+'.log',
        format=logFormat,
        datefmt=logDateFormat,
        level=logging.DEBUG)
    logging.info(f'Unrolling script called at: {datetime.datetime.now()}')
    logging.info(f'Target PL file: {plLogicFile}')
    logging.info('Output directories created.')

    sys.path.append(workDir)

    # Do a one-time check to ensure the I/O listed in the I/O CSV matches the I/O listed in the Z3Py
    logging.warning('Code does not currently support cross-checking I/O names found in text lists against netlist files. Please check manually.')


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
        mtchObj = re.match(r'^\s*(?P<funID>\w+)\s*=\s*(?P<fun>[^\'\"]+\)).*',line)     # Future work: there's gotta be a better RE to exclude "Solver"
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


def parseIO(ioCSV,plLogicFile,hiZ=False) -> Tuple[list,list,list,dict]:
    '''
    Extract I/O from CSV file

    ioCSV       -   CSV containing I/O list
    plLogicFile -   Z3Py netlist file, for cross-checking against the I/O CSV
    hiZ         -   True if plLogicFile contains outputs with correlating high-impedance variables
    '''
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
            elif (ioAtts[0] == 'output') and hiZ:
                outVars.append(ioNm)
                try:
                    hiZVars[ioNm] = ioAtts[1]
                except:
                    raise RuntimeError(f'I/O file {ioCSV} not formatted correctly to indicate a matching HiZ variable to output variable {ioNm}')
            elif (ioAtts[0] == 'output') and not hiZ:
                outVars.append(ioNm)
            else:
                raise RuntimeError(f'I/O {ioNm} has unrecognized data type "{ioAtts[0]}". Please revise I/O file {ioCSV}')
    
    return inVars,keyVars,outVars,hiZVars


def buildStateFinder(trgtPL:str,inVars:list,keyVars:list,outVars:list,miterFile:str,mSuff='_m',hiZVars={},debug=False) -> list:
    '''
    Create miter circuit for a given input Z3Py file. Returns a list of input variable names and a list key variable names for convenience.

    trgtPL      - Path to Z3 Python file containing PL clauses to create a miter circuit out of
    inVars      - List of variables designated as inputs in targetPL
    keyVars     - List of variables designated as key inputs in targetPL
    outVars     - List of variables designated as outputs in targetPL
    miterFile   - Desired path, filename, and extension for output Z3 file
    mSuff       - Desired suffix to be added to net names for each miter circuit (do not include copy number)
    hiZVars     - Dict of high-impedance variables designated in targetPL
    '''
    # Read in PL
    plVars,plClauses = readZ3pl(trgtPL)

    # Create two copies of one circuit with identical inputs
    miterVars = {}
    miterClauses = []
    for i in range(1,3):
        copy,copyVars = copyCircuit(plClauses,plVars,inVars,keyVars,outVars,suffix=f'{mSuff}{i}',modIns=False,modKeys=False)
        #copy,copyVars = copyCircuit(copy,copyVars,inVars,keyVars,outVars,suffix=f'_{i}',modIns=False,modOuts=False,modNets=False)  # This "recopy" step creates unique keys
        miterVars = miterVars | {k:v for k,v in copyVars.items() if k not in miterClauses}
        miterClauses.extend(copy)

    # Make the miter comparator
    # compVars = outVars                                                        # Only outputs considered by comparator
    compVars = [x for x in plVars.keys() if x not in (inVars+keyVars)]          # All internal nets and outputs considered by comparator
    outSubclauses = []
    if hiZVars == {}:
        # Traditional comparator
        for var in compVars:
                outSubclauses.append(f'Xor({var+mSuff+"1"},{var+mSuff+"2"})')
    else:
        # "BLUE" miter circuit - for all output pairs, at least one logical pair must differ with at least one
        # of the two corresponding hiZ variables being true.
        for compVar, hiZVar in hiZVars.items():
            outSubclauses.append(f'And(Xor({compVar+mSuff+"1"},{compVar+mSuff+"2"}),Or({hiZVar+mSuff+"1"},{hiZVar+mSuff+"2"}))')
    miterClauses.append(f'Or({",".join(outSubclauses)})     # Miter comparator')

    writeZ3pl(miterVars,miterClauses,miterFile,prnt=debug)

    return plClauses


def runZ3(trgtZ3:str,voi=[]) -> Tuple[bool,list]:
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


def stateLocate(plLogicFile:str,ioCSV:str,fresh=False,debug=False,highImpedance=False) -> list:
    '''
    Find the state-holding nets within a Z3 netlist
    '''
    setup(plLogicFile,fresh=fresh,debug=debug)

    # PREPROCESSING
    # Parse I/O and nets from input Z3
    inVars,keyVars,outVars,hiZVars = parseIO(ioCSV,plLogicFile,hiZ=highImpedance)
    netsDict,clauseList = readZ3pl(plLogicFile)

    # Create miter circuit from input netlist, extract netlist description, create graph
    buildStateFinder(plLogicFile,inVars,keyVars,outVars,miterFile,mSuff=miterSuffix,hiZVars=hiZVars,debug=debug)
    graph = NetlistGraph(list(netsDict),clauseList)


    # PROCESSING
    # Run miter file, extract variable results
    sat,varAssigns = runZ3(miterName)
    stateNets = []

    while(sat):

        # Find conflicting variables and put them in list
        diffList = []
        netsDictPruned = {key: netsDict[key] for key in netsDict if key not in (inVars+keyVars)}      # Ignore primary and key inputs
        for net in netsDictPruned:
            if varAssigns[f'{net}{miterSuffix}1'] != varAssigns[f'{net}{miterSuffix}2']:
                diffList.append(net)

        # Trace variables from diff List - tee-up and then DFS along nets that received conflicting assignments
        roundStateNets = []
        for cycle in graph.minimalCycles().values():
            if set(cycle).issubset(diffList):
                roundStateNets.extend(cycle)

        # Tie those outputs together - they must have the same value to prevent a discrepancy
        for net in roundStateNets:
            writeZ3pl({},[f'({net}{miterSuffix}1 == {net}{miterSuffix}2)\t\t# Frozen state-holding net'],miterFile,append=True)

        stateNets.extend(roundStateNets)
        sat,varAssigns = runZ3(miterName)

    if len(stateNets) == 0:
        print('No state-carrying nets detected')
    else:
        print(stateNets)

    return stateNets


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A tool for running SAT attacks on an encrypted netlist written in Z3 for Python')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('-d','--debug',default=False,action='store_true',help='Creates intermediate scripts in a "debug" directory, for the purposes of troubleshooting when an attack goes awry')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs = parser.parse_args()

    stateLocate(clArgs.plLogicFile,clArgs.ioCSV,clArgs.fresh,clArgs.debug,clArgs.tristate)
