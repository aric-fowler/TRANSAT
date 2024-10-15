'''
File used for packaging. Official documentation now recommends 'setup.cfg' instead of this file for
packaging. Documentation is located here:
https://packaging.python.org/en/latest/tutorials/packaging-projects/

Author:     Aric Fowler
Python:     3.10.12
Updated:    Oct 2024
'''
import setuptools

with open('README.md','r',encoding='utf-8') as fhand:
    long_description = fhand.read()

setuptools.setup(
    name='transat',
    version='0.1.4',
    author='Aric Fowler',
    author_email='aric.fowler@utdallas.edu',
    description='TRANSAT is a set of SAT tools for solving the transistor-level circuit technologies, built around the Microsoft Z3 SMT solver.',
    long_description=long_description,
    long_description_context_type='text/markdown',
    url="https://github.com/aric-fowler/STRAPT",
    data_files= [('share/man/man1/', ['man/satAttack.1','man/satVerify.1'])],
    project_urls={
        "Bug Tracker":"https://github.com/aric-fowler/STRAPT/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
    'z3-solver'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'satAttack = src.satAttack_cli:main',
            'satVerify = src.satVerify_cli:main',
            'trapFabricBuilder = src.trapFabricBuilder_cli:main',
            'crTRAPFabricBuilder = src.crTRAPFabricBuilder_cli:main',
            'lutCRFabricBuilder = src.lutCRFabricBuilder_cli:main',
            'abcAttack = src.abcAttack_cli:main'
        ]
    }
)
