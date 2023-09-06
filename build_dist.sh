#!/bin/bash
#
# Following this tutorial on building packages:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Author:   Aric Fowler
# Updated:  Apr 2023

pip3 uninstall strapt

rm -rf dist/

# This line actually builds the code
python3 -m build

cd dist/

pip3 install *.tar.gz

cd ../
