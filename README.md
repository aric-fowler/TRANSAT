# TRANSAT

TRANSAT, or "Transistor-Level SAT Tools", is a Python library for launching SAT-related functions on digital circuits implemented on the transistor level. 
These functions include SAT attacks andSAT-based verification. These tools can be extended to other types of logic circuits, including logic-locked circuits.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install a locally-downloaded TRANSAT distribution (available from dist/), or contact 
[Aric](aric.fowler@utdallas.edu) for the package. Icarus Verilog (iVerilog) may be installd easily using [apt](https://en.wikipedia.org/wiki/APT_(software)).

```bash
sudo apt install iverilog

pip3 install transat            # .whl or .tar.gz file must be in current directory
```

To use the ABC SAT attack, [download](https://github.com/berkeley-abc/abc) and install it using the included Makefile. 

## Usage

### Command Terminal (Recommended):
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

# Alternative SAT attack based on ABC tool:
abcAttack encryptedVerilog.v oracleVerilog.v
```
For examples on how to run a SAT attack, see the shell scripts in test/

### Within Python:
```python
# SAT attack:
from transat import satAttack

satAttack(plLogicFile,inputList,keyList,outputList,oracleNetlist,oracleName)
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
