#!/usr/bin/env python3
'''
Command-line interface for stateLocate.py

Author:     Aric Fowler
'''
import argparse
from .stateLocate import stateLocate

def main():
    parser = argparse.ArgumentParser(prog='stateLocate',description='A tool for finding state-holding elements within a netlist written in Z3 for Python')
    parser.add_argument('plLogicFile',type=str,help='Path to the Python file containing propositional logic clauses to be solved. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('-d','--debug',default=False,action='store_true',help='Creates intermediate scripts in a "debug" directory, for the purposes of troubleshooting when an attack goes awry')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs = parser.parse_args()

    stateLocate(clArgs.plLogicFile,clArgs.ioCSV,clArgs.fresh,clArgs.debug,clArgs.tristate)


if __name__ == '__main__':
    exit(main())
