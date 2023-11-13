#!/bin/bash

satAttack -fd encryptC17pl.py encryptC17io.csv c17.v c17

satVerify encryptC17pl.py c17.py encryptC17io.csv work/extracted_key.csv