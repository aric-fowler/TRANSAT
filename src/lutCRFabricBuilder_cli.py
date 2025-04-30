'''
Command-line interface for crTRAPFabricBuilder.py

Author:     Aric Fowler
'''
import argparse
from .lutCRFabricBuilder import lutCRFabricBuilder

def main():
    parser = argparse.ArgumentParser(prog='lutCRFabricBuilder',description='A tool for generating islands of LUTs hardwired together, written in Z3 for Python')
    parser.add_argument('numLUTs',type=int,help='The number of LUTs for the output fabric. Minimum value is 1')
    parser.add_argument('pinMap',type=str,help='Path to the comma-delimited CSV file containing a list of I/O pin names, the corresponding input wires they are placed on, and whether the pin is an input, output, or route')
    parser.add_argument('-d',action='store_true',dest='debug',default=False,help='Puts verbosity in Z3 output scripts for SMT readout')
    parser.add_argument('-m',action='store',dest='maxCount',default=None,type=int,help='The maximum allotted value for count variables. A lower number may speed up SAT solver times, but could overconstrain the output model. The count will be constrained only if this variable is set')
    parser.add_argument('-o',action='store',dest='outputFileName',default='lutCRFabricPL',type=str,help='Base name of output files (no extension) to be created in the current directory')
    clArgs = parser.parse_args()

    lutCRFabricBuilder(clArgs.numLUTs,clArgs.pinMap,clArgs.debug,clArgs.outputFileName,clArgs.maxCount)

if __name__ == '__main__':
    exit(main)
