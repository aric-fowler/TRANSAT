# TRANSAT

TRANSAT, or "Transistor-Level SAT Tools", is a Python library for launching SAT-related functions 
on digital circuits implemented on the transistor level. These functions include SAT attacks and
SAT-based verification. These tools can be extended to other types of logic circuits, including 
logic-locked circuits.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TRANSAT, or contact Aric Fowler for the package.

```bash
pip3 install transat
```

## Usage

### Command line:
```bash
# Help:
satAttack -h
satVerify -h

# User manual:
man satAttack
man satVerify

# SAT attack:
satAttack plLogicFile ioCSV oracleNetlist oracleName

# SAT verification:
satVerify plEncryptedFile plFunctionFile ioCSV keyValueCSV
```

### Within Python:
```python
# SAT attack:
from transat import satAttack

satAttack(plLogicFile,inputList,keyList,outputList,oracleNetlist,oracleName)
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
