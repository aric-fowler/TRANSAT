#!/bin/bash

# Runs a SAT attack on a logic-locked C17 and verifies the key

satAttack -fd encryptC17pl.py encryptC17io.csv c17.v c17

satVerify encryptC17pl.py c17.py encryptC17io.csv work/extracted_key.csv