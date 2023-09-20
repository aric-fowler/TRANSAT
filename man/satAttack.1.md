---
title: SATATTACK
section: 1
header: User Manual
footer: satAttack 0.0.4
date: September 13, 2023
---

# NAME
satAttack - A SAT attack program, developed for launching SAT attacks on UTD's TRAnsistor-level Programmable (TRAP) fabric.

# SYNOPSIS
**satAttack** [*OPTION*]...

# DESCRIPTION
**satAttack** runs a SAT attack on a 

# OPTIONS
**-h** 
: Display help message

**-f**
: Creates fresh directories for all script outputs. WARNING: deletes prexisting directories.

**-q** 
: Stops printing of SAT attack results to terminal. Recommended when optimizing runtime or for attacks with many keys.

**-z**
: Enables the SAT attack to consider outputs that may have high-impedance functionality. May be needed for proper attack on circuits that have tri-state outputs or 
: transistor-level behavior (like T-gates). Expects a text file containing names of "hiZ output" variables, separated by whitespaces.

# EXAMPLES
**satAttack plFile.py ins.txt keys.txt outs.txt oracle.v topName -fv**
: Runs a SAT attack on the encrypted circuit described in plFile.py, against the oracle "topName" described in oracle.v.

# AUTHORS
Written by Aric Fowler

# BUGS
Submit bug reports online at: <https://github.com/aric-fowler/STRAPT/issues>

# SEE ALSO
Full documentation and sources at: <https://github.com/aric-fowler/STRAPT>