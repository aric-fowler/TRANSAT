'''
Command-line interface for satAttack.py

Author:     Aric Fowler

'''
import argparse
from .satAttack import satAttack

def main():
    # Parse necessary input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('inputList',type=str,help='Path to the text file containing a list of inputs to the plLogicFile. Inputs must be separated by a space or newline character')
    parser.add_argument('keyList',type=str,help='Path to the text file containing a list of key inputs to the plLogicFile. Keys must be separated by a space or newline character')
    parser.add_argument('outputList',type=str,help='Path to the text file containing a list of outputs to the plLogicFile. Outputs must be separated by a space or newline character')
    parser.add_argument('oracleNetlist',type=str,help='Name + extension of the HDL netlist file for the unencrypted, oracle black box. Input and output names must coincide with what is found in the inputList and outputList files')
    parser.add_argument('topModule',type=str,help='Top-level module name within "oracleNetlist"')
    parser.add_argument('-f','--fresh',action='store_true',default=False,help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-po','--pythonOracle',default=False,action='store_true',help='If true, oraclenetlist points to a Python oracle file (alternative to using iVerilog). Oracle function must be declared as "main", and all input variable names must coincide with inputList')
    parser.add_argument('-v','--verbosity',default=False,action='store_true',help='Print progress of SAT attack to terminal')
    clArgs=parser.parse_args()

    satAttack(clArgs.plLogicFile,clArgs.inputList,clArgs.keyList,clArgs.outputList,clArgs.oracleNetlist,clArgs.topModule,clArgs.fresh,clArgs.pythonOracle,clArgs.verbosity)



if __name__ == '__main__':
    main()