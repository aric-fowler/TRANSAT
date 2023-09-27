---
title: SATATTACK
section: 1
header: User Manual
footer: satAttack 0.0.6
date: September 27, 2023
---

# NAME
satAttack - A SAT attack program, developed for launching SAT attacks on UTD's TRAnsistor-level Programmable (TRAP) fabric.

# SYNOPSIS
**satAttack** [*OPTION*] encryptedZ3PyFile inputList keyList outputList oracleNetlist topLevelModule

# DESCRIPTION
**satAttack** runs a SAT attack on an encrypted Z3Py netlist, using a provided oracle netlist.

# OPTIONS
**-h**, **--help**
: Display help message.

**-f**, **--fresh**
: Creates fresh directories for all script outputs. WARNING: deletes prexisting directories.

**-q**, **--quiet**
: Stops printing of SAT attack results to terminal. Recommended when optimizing runtime or for attacks with many keys.

**-z**,
: Enables the SAT attack to consider outputs that may have high-impedance functionality. May be needed for proper attack on circuits that have tri-state outputs or 
: transistor-level behavior (like T-gates). Expects a text file containing names of "hiZ output" variables, separated by whitespaces.

# EXAMPLES
**satAttack plFile.py ins.txt keys.txt outs.txt oracle.v topName -f**
: Runs a SAT attack on the encrypted circuit described in plFile.py, against the oracle "topName" described in oracle.v.

**inputList.txt for N-input circuit**
: a b c ... inN

**keylist.txt for M-key circuit**
: k1 k2 k3 ... kM

**outputList.txt for P-output circuit**
: O z circOut sum ... outP

**matching hiZoutputList.txt for example outputList.txt**
: O         : vO \
: z         : vz \
: circOut   : vcircOut \
: sum       : vsum \

# AUTHORS
Written by Aric Fowler

# BUGS
Submit bug reports online at: <https://github.com/aric-fowler/STRAPT/issues>

# SEE ALSO
Full documentation and sources at: <https://github.com/aric-fowler/STRAPT>