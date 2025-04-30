'''
Command-line interface for satVerify.py

Author:     Aric Fowler
'''
import argparse
from .satVerify import satVerify

def main():
    parser = argparse.ArgumentParser(prog='satVerify',description='A tool for running SAT verification on a programmable netlist written in Z3 for Python')
    parser.add_argument('plEncryptedFile',type=str,help='Path to a Python file containing propositional logic clauses that require key inputs. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('plFunctionFile',type=str,help='Path to a Python file containing the counterpart non-encrypted functionality to plEncryptedFile. Clauses must be written in the Z3 Python format. For help writing Z3 Python, see: https://www.cs.toronto.edu/~victorn/tutorials/sat20/index.html#installation')
    parser.add_argument('ioCSV',type=str,help='Path to the comma-delimited CSV file containing a list of input/output/key names, their corresponding type (input/output/key), and a corresponding HiZ variable, if applicable.')
    parser.add_argument('keyValueCSV',type=str,help='Path to the CSV file containing a list of key input names and values to the plEncryptedFile')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Create fresh directories for SAT attack. WARNING: deletes preexisting logs and outputs')
    parser.add_argument('-q','--quiet',default=False,action='store_true',help='Prevent printing of SAT attack progress to terminal')
    parser.add_argument('-z','--tristate',default=False,action='store_true',help='Enables "tri-state" mode for circuit outputs. High-impedance mode considers situations where an output may exhibit tri-state behavior and its associated logic value may be invalid. The correlating tri-state variable name must be listed after the "output" type in the ioCSV file')
    clArgs = parser.parse_args()

    satVerify(clArgs.plEncryptedFile,clArgs.plFunctionFile,clArgs.ioCSV,clArgs.keyValueCSV,clArgs.fresh,clArgs.quiet,clArgs.tristate)


if __name__ == '__main__':
    exit(main())
