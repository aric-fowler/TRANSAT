#!/bin/bash
#
# Following this tutorial on building packages:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# Author:   Aric Fowler
# Updated:  Apr 2023


rm -rf dist/

python3 -m build
