'''
Command-line interface for crTRAPFabricBuilder.py

Author:     Aric Fowler
'''
import argparse
from .crTRAPFabricBuilder import trapFabricBuilder

def main():
    parser = argparse.ArgumentParser(prog='crTRAPFabricBuilder',description='A tool for generating a model of a given size TRAP fabric with fully custom routes (no interconnect), written in Z3 for Python')
    parser.add_argument('numRows',type=int,help='The number of rows of TRAP units for the output fabric. Minimum value is 1')
    parser.add_argument('numCols',type=int,help='The number of columns of TRAP units for the output fabric. Minimum value is 1')
    parser.add_argument('pinMap',type=str,help='Path to the comma-delimited CSV file containing a list of I/O pin names, the corresponding L3 or L4 wire they are placed on, and whether the pin is an input or an output')
    parser.add_argument('-d',action='store_true',dest='debug',default=False,help='Puts verbosity in Z3 output scripts for SMT readout')
    parser.add_argument('-m',action='store',dest='maxCount',default=None,type=int,help='The maximum allotted value for count variables. A lower number may speed up SAT solver times, but could overconstrain the output model. The count will be constrained only if this variable is set')
    parser.add_argument('-o',action='store',dest='outputFileName',default='trapCRFabricPL',type=str,help='Base name of output files (no extension) to be created in the current directory')
    clArgs = parser.parse_args()

    trapFabricBuilder(clArgs.numRows,clArgs.numCols,clArgs.pinMap,clArgs.debug,clArgs.outputFileName,clArgs.maxCount)

if __name__ == '__main__':
    exit(main)