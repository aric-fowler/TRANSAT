'''
Command-line interface for satAttack.py

Author:     Aric Fowler
'''
import argparse
from .abcAttack import abcAttack

def main():
    parser = argparse.ArgumentParser('A SAT attack script built around MiniSAT, iVerilog, and the verification capabilities of ABC')
    parser.add_argument('encVerilog',type=str,help='Path to Verilog file describing encrypted circuit')
    parser.add_argument('orcVerilog',type=str,help='Path to Verilog file describing unencrypted circuit (oracle)')
    parser.add_argument('-f','--fresh',default=False,action='store_true',help='Creates fresh working and log directories upon calling this script')
    parser.add_argument('-g','--fraig',default=True,action='store_false',help='Disable fraiging capabilities of ABC solver (on by default)')
    clArgs= parser.parse_args()

    abcAttack(clArgs.encVerilog,clArgs.orcVerilog,clArgs.fresh,clArgs.fraig)


if __name__ == '__main__':
    exit(main())
