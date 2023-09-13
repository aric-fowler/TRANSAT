'''
File used for packaging. Official documentation now recommends 'setup.cfg' instead of this file for
packaging. Documentation is located here:
https://packaging.python.org/en/latest/tutorials/packaging-projects/

Author:     Aric Fowler
Python:     3.6.9
Updated:    Sept 2022
'''
import setuptools

with open('README.md','r',encoding='utf-8') as fhand:
    long_description = fhand.read()

setuptools.setup(
    name='strapt',
    version='0.0.4',
    author='Aric Fowler',
    author_email='aric.fowler@utdallas.edu',
    description='STRAPT is a set of SAT tools for solving the University of Texas - Dallas TRAP circuit technology, built around the Microsoft Z3 SMT solver.',
    long_description=long_description,
    long_description_context_type='text/markdown',
    url="https://cometmail.sharepoint.com/sites/ECETRAP-SecurityAnalysis/Shared%20Documents/Forms/AllItems.aspx?FolderCTID=0x0120005DC35724679FFA43B3870ABD93481C76&id=%2Fsites%2FECETRAP%2DSecurityAnalysis%2FShared%20Documents%2FSecurity%20Analysis%2FIn%2DHouse%20SAT%20Tools%2FSAT%5FAttack%5Fv2&viewid=bed26541%2D81f2%2D4c77%2D9fae%2D5d41a0958767",
    project_urls={
        "Bug Tracker":"",
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
