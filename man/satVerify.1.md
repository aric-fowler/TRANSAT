---
title: SATVERIFY
section: 1
header: User Manual
footer: satVerify 0.1.1
date: November 3, 2023
---

# NAME
satVerify - A SAT-based verification program, developed for verifying programming bitstreams for UTD's TRAnsistor-level Programmable (TRAP) fabric.

# SYNOPSIS
**satVerify** [*OPTION*] plEncryptedFile plFunctionFile ioCSV keyValueCSV

# DESCRIPTION
**satVerify** runs bitstream verification on an unprogrammed Z3Py netlist, using a provided oracle netlist that contains the programmed functionality.

# OPTIONS
**-h**, **--help**
: Display help message.

**-f**, **--fresh**
: Creates fresh directories for all script outputs. WARNING: deletes prexisting directories. Do not use if running satVerify directly after satAttack. 

**-q**, **--quiet**
: Stops printing of results to terminal. Recommended when optimizing runtime or for attacks with many keys.

**-z**,
: Enables the verification tool to consider outputs that may have high-impedance functionality. May be needed for proper attack on circuits that have tri-state outputs or transistor-level behavior (like T-gates). Expects HiZ variables correlating to output variables to be placed in the ioCSV file after the "output" value.

# EXAMPLES
**satVerify -z programmablePL.py functionalPL.py ioList.csv keyVals.csv**
: Runs programming functionality on the unprogrammed circuit described in plFile.py, against the oracle "topName" described in oracle.v. HiZ mode is active.

**ioList.csv formatting for N-input, M-key, P-output circuit with hiZ varaibles correlating to outputs**
: ```text
a,input
b,input
...
inN,input
k1,key
k2,key 
...
kM,key
O,output,vO
z,output,zHiZVar
...
outP,output,vOutP
```

**keyVals.csv formatting for M-key circuit**
: ```
k1,True
k2,True
k3,False
...
kM,True
```

# AUTHORS
Written by Aric Fowler

# BUGS
Submit bug reports online at: <https://github.com/aric-fowler/STRAPT/issues>

# SEE ALSO
Full documentation and sources at: <https://github.com/aric-fowler/STRAPT>
