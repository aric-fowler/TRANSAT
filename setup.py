'''
File used for packaging. Official documentation now recommends 'setup.cfg' instead of this file for
packaging. Documentation is located here:
https://packaging.python.org/en/latest/tutorials/packaging-projects/

Author:     Aric Fowler
Python:     3.6.9
Updated:    Sept 2022
'''
import os
import sys
import setuptools

with open('README.md','r',encoding='utf-8') as fhand:
    long_description = fhand.read()

setuptools.setup(
    name='strapt',
    version='0.0.6',
    author='Aric Fowler',
    author_email='aric.fowler@utdallas.edu',
    description='STRAPT is a set of SAT tools for solving the University of Texas - Dallas TRAP circuit technology, built around the Microsoft Z3 SMT solver.',
    long_description=long_description,
    long_description_context_type='text/markdown',
    url="https://github.com/aric-fowler/STRAPT",
    data_files= [('share/man/man1/', ['man/satAttack.1'])],
    project_urls={
        "Bug Tracker":"https://github.com/aric-fowler/STRAPT/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
    'z3-solver',
    'python-apt'],
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'satAttack = src.satAttack_cli:main',
        ]
    }
)
