---
title: SATATTACK
section: 1
header: User Manual
footer: satAttack 0.1.1
date: February 8, 2024
---

# NAME
satAttack - A SAT attack program, developed for launching SAT attacks on transistor-level circuits.

# SYNOPSIS
**satAttack** [*OPTION*] plLogicFile ioCSV oracleNetlist topLevelModule

# DESCRIPTION
**satAttack** runs a SAT attack on an encrypted Z3Py netlist, using a provided oracle netlist that contains the programmed functionality.

# OPTIONS
**-h**, **--help**
: Display help message.

**-f**, **--fresh**
: Creates fresh directories for all script outputs. WARNING: deletes prexisting directories.

**-q**, **--quiet**
: Stops printing of SAT attack results to terminal. Recommended when optimizing runtime or for attacks with many keys.

**-z**,
: Enables the verification tool to consider outputs that may have high-impedance functionality. May be needed for proper attack on circuits that have tri-state outputs or transistor-level behavior (like T-gates). Expects HiZ variables correlating to output variables to be placed in the ioCSV file after the "output" value.

# EXAMPLES
**satAttack plFile.py ioList.csv oracle.v topName -f**
: Runs a SAT attack on the encrypted circuit described in plFile.py, against the oracle "topName" described in oracle.v.

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

# AUTHORS
Written by Aric Fowler

# BUGS
Submit bug reports online at: <https://github.com/aric-fowler/STRAPT/issues>

# SEE ALSO
Full documentation and sources at: <https://github.com/aric-fowler/STRAPT>
