'''
Command-line interface for satAttack.py

Author:     Aric Fowler
'''
import argparse
from .satAttack import satAttack

def main():
    # Parse necessary input arguments
    parser = argparse.ArgumentParser('A tool for running SAT attacks on an encrypted netlist written in Z3 for Python')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('inputList',type=str,help='Path to the text file containing a list of inputs to the plLogicFile. Inputs must be separated by a space or newline character')
    parser.add_argument('keyList',type=str,help='Path to the text file containing a list of key inputs to the plLogicFile. Keys must be separated by a space or newline character')
    parser.add_argument('outputList',type=str,help='Path to the text file containing a list of outputs to the plLogicFile. Outputs must be separated by a space or newline character')
    parser.add_argument('oracleNetlist',type=str,help='Name + extension of the HDL netlist file for the unencrypted, oracle black box. Input and output names must coincide with what is found in the inputList and outputList files')
    parser.add_argument('topModule',type=str,help='Top-level module name within "oracleNetlist"')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-p','--pythonOracle',default=False,action='store_true',help='If true, oraclenetlist points to a Python oracle file (alternative to using iVerilog). Oracle function must be declared as "main", and all input variable names must coincide with inputList')
    parser.add_argument('-d','--debug',default=False,action='store_true',help='Creates intermediate scripts in a "debug" directory, for the purposes of troubleshooting when an attack goes awry.')
    parser.add_argument('-v','--verbose',default=False,action='store_true',help='Print progress of SAT attack to terminal')
    parser.add_argument('-z','--tristateOuts',default=None,nargs='?',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. Requires an additional input text file containing the names of the tri-state variables, separated by a space or a newline character')
    clArgs=parser.parse_args()

    satAttack(clArgs.plLogicFile,clArgs.inputList,clArgs.keyList,clArgs.outputList,clArgs.oracleNetlist,clArgs.topModule,clArgs.fresh,clArgs.pythonOracle,clArgs.debug,clArgs.verbose,clArgs.tristateOuts)



if __name__ == '__main__':
    main()
