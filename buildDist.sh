#!/bin/bash
#
# Following this tutorial on building packages:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Updated:  Oct 2023

rm -rf dist/

# Write the MANs
pandoc man/satAttack.1.md -s -t man -o man/satAttack.1
pandoc man/satVerify.1.md -s -t man -o man/satVerify.1

# Builds the wheel & zip
python3 -m build

cd dist/

pip3 install *.tar.gz

cd ../
