'''
Command-line interface for satAttack.py

Author:     Aric Fowler
'''
import argparse
from .satAttack import satAttack

def main():
    parser = argparse.ArgumentParser('A tool for running SAT attacks on an encrypted netlist written in Z3 for Python')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('oracleNetlist',type=str,help='Path to the HDL netlist file for the unencrypted, oracle black box. Input and output names must coincide with what is found in the inputList and outputList files')
    parser.add_argument('topModule',type=str,help='Top-level module name within "oracleNetlist"')
    parser.add_argument('-e','--disableEarlyTermination',default=True,action='store_false',help='By default, skips the final (UNSAT) round of the attack if all possible inputs are explored as DIPs. Enable flag to go through final round regardless')
    parser.add_argument('-d','--debug',default=False,action='store_true',help='Creates intermediate scripts in a "debug" directory, for the purposes of troubleshooting when an attack goes awry')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-p','--pythonOracle',default=False,action='store_true',help='If true, oraclenetlist points to a Python oracle file (alternative to using iVerilog). Oracle function must be declared as "main", and all input variable names must coincide with inputList')
    parser.add_argument('-q','--quiet',default=False,action='store_true',help='Prevent printing of SAT attack progress to terminal')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs=parser.parse_args()

    satAttack(clArgs.plLogicFile,clArgs.ioCSV,clArgs.oracleNetlist,clArgs.topModule,clArgs.disableEarlyTermination,clArgs.fresh,clArgs.pythonOracle,clArgs.debug,clArgs.quiet,clArgs.tristate)


if __name__ == '__main__':
    exit(main())
