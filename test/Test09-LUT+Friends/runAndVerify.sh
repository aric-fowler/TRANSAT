#!/bin/bash

satAttack lutWithLogic.py io.csv oracle.v oracle -f

satVerify lutWithLogic.py oracle.py io.csv work/extracted_key.csv