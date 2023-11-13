#!/bin/bash

trapFabricBuilder 1 1 ioMap.csv -m 5 -o trapNAND2

satAttack trapNAND2.py trapNAND2_io.csv twoInputGates.v nand2 -fz

satVerify -z trapNAND2.py nand2PL.py trapNAND2_io.csv work/extracted_key.csv
