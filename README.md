# TRANSAT
Anonymous repo for TRANSAT

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TRANSAT, or contact for the package.

```bash
pip3 install strapt
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
from strapt import satAttack

satAttack(plLogicFile,inputList,keyList,outputList,oracleNetlist,oracleName)
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
