# TRANSAT

TRANSAT, or "Transistor-Level SAT Tools", is a Python library for launching SAT-related functions on digital circuits implemented on the transistor level. 
These functions include SAT attacks and SAT-based verification. These tools can be extended to other types of logic circuits, including logic-locked circuits.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install a locally-downloaded TRANSAT distribution (available from dist/), or contact 
[Aric](aric.fowler@utdallas.edu) for the package. Icarus Verilog (iVerilog) may be installed easily using [apt](https://en.wikipedia.org/wiki/APT_(software)).

```bash
sudo apt install iverilog python3-pip

git clone https://github.com/aric-fowler/TRANSAT

cd TRANSAT/dist/

pip3 install *.tar.gz            # Alternatively: $ pip3 install *.whl
```

To use the ABC SAT attack, [download ABC](https://github.com/berkeley-abc/abc) and install it using the included Makefile, along with the TRANSAT package.

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
For examples on how to run a SAT attack, see the shell scripts in the test/ directory. The output of a SAT attack is  "extracted_key.csv", located in the work/ 
directory created by the attack script. Verification tool results are printed directly to the terminal. 

### Within Python:
```python
# SAT attack:
from transat import satAttack

satAttack(plLogicFile,inputList,keyList,outputList,oracleNetlist,oracleName)
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
