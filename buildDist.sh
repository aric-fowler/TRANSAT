#!/bin/bash
#
# Following this tutorial on building packages:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Author:   Aric Fowler
# Updated:  Apr 2023

pip3 uninstall strapt

rm -rf dist/

# Write the MANs
pandoc man/satAttack.1.md -s -t man -o man/satAttack.1

# Builds the wheel & zip
python3 -m build

cd dist/

pip3 install *.tar.gz

cd ../
