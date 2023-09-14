# STRAPT

STRAPT, or "Satisfiability TRAP Tools", is a Python library for launching SAT-related functions on the Univesity 
of Texas - Dallas TRAP TRAnsistor-level Programmable fabric (TRAP) technology. These functions include SAT attacks, 
SAT-based routing, and SAT-based synthesis. While TRAP is a transistor-level approach to 
implementing logic functions, these tools should be able to be extended to other types of logic
circuits, including logic-locked circuits (results may vary).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install STRAPT, or contact [Aric](aric.fowler@utdallas.edu) for the package.

```bash
pip3 install strapt
```

## Usage

### Command line:
```bash
# Help:
satAttack -h

# User manual:
man satAttack

# SAT attack:
satAttack plLogicFile inputList keyList outputList oracleNetlist oracleName
```

### Within Python:
```python
# SAT attack:
from strapt import satAttack

satAttack(plLogicFile,inputList,keyList,outputList,oracleNetlist,oracleName)
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
