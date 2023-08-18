# pyballc

[![PyPI version](https://badge.fury.io/py/pyballc.svg)](https://badge.fury.io/py/pyballc)


Pyballc is a python module to read/manipulate BAllC files. It is based on the [BAllCools](https://github.com/jksr/ballcools).

_Currently only reading and querying operations are supported, but more is comming:wink:_


### Dependency
```g++``` (with -std=c++11 supported)

```libhts``` (```conda``` installation recommended)

```libdeflated``` (this is libhts' dependency. so it should be available if libhts is correctly installed)

```libz``` (usually no installation needed. should be available for most systems)

```libbz2``` (usually no installation needed. should be available for most systems)


### Installation
pyballc is a stand alone package. You don't need to install BAllCools separately.

**Installing from pypi**
```bash
pip install pyballc
```

**Installing from github**
```bash
git clone https://jksr@github.com/jksr/pyballc
cd pyballc
git submodule init 
git submodule update 
pip install .
```

or 
```shell
pip install git+https://jksr@github.com/jksr/pyballc

pip install git+https://github.com/DingWB/pyballc.git
```

### Usage
#### 1. Command Line
```shell
pyballc -h
INFO: Showing help with the command 'pyballc -- --help'.

NAME
    pyballc

SYNOPSIS
    pyballc COMMAND

COMMANDS
    COMMAND is one of the following:

     cmeta
       Extract all C position from fasta file.

     b2a
       Convert ballc file into allc path.

     a2b
       Convert allc file into ballc file.
```
##### Extract all C positon from given fasta file
```shell
pyballc cmeta --help
INFO: Showing help with the command 'pyballc cmeta -- --help'.

NAME
    pyballc cmeta - Extract all C position from fasta file.

SYNOPSIS
    pyballc cmeta <flags>

DESCRIPTION
    Extract all C position from fasta file.

FLAGS
    -f, --fasta_path=FASTA_PATH
        Type: Optional[]
        Default: None
        path for fasta file
    -c, --cmeta_path=CMETA_PATH
        Type: Optional[]
        Default: None
        path for the output cmeta file.
        
pyballc cmeta -f ~/Ref/mm10/mm10_ucsc_with_chrL.fa -c mm10_with_chrL_cmeta.txt
```

##### allc to ballc
```shell
pyballc a2b --help
INFO: Showing help with the command 'pyballc a2b -- --help'.

NAME
    pyballc a2b - Convert allc file into ballc file.

SYNOPSIS
    pyballc a2b <flags>

DESCRIPTION
    Convert allc file into ballc file.

FLAGS
    --allc_path=ALLC_PATH
        Type: Optional[]
        Default: None
        input allc file path.
    -b, --ballc_path=BALLC_PATH
        Type: Optional[]
        Default: None
        output ballc path, will be indexed automatically.
    -c, --chrom_size_path=CHROM_SIZE_PATH
        Type: Optional[]
        Default: None
    --assembly_text=ASSEMBLY_TEXT
        Default: ''
        text to be added
    -h, --header_text=HEADER_TEXT
        Default: ''
        text to be added
    -s, --sc=SC
        Default: True
        whether single cell file?
```

```shell        
time pyballc a2b --allc_path FC_E17a_3C_8-6-I15-M23.allc.tsv.gz -b test.ballc -c ~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes --assembly_text "test" -h "test header" -s
```

```
Writing BAllC header to test.ballc
Converting AllC to BAllC
Converting AllC to BAllC finished
Building index for test.ballc
Warning: The index file is older than the BAllC file. It may be out-of-date.
Writing the index file test.ballc.bci
Indexing test.ballc finished
test.ballc

real    0m3.772s
user    0m3.707s
sys     0m0.027s
```

#### 2. API
Read ballc
```shell
import pyballc
ballc_file = 'test.ballc'
cmeta_file = 'h1930001.cmeta.gz'

region = 'chr1', 0, 80000
ballc = pyballc.BAllCFile(ballc_file, cmeta_file)

# fetch tuple
for x in ballc.fetch('chr1', 0, 80000):
    print(x)
    
# fetch all records line by line
for line in ballc.fetch_line("*",None,None):
  print(line)
```

ballc to allc
```python
pyballc.Ballc2Allc(ballc_path,cmeta_path,allc_path)
```

allc to ballc
```python
allc_path = "/anvil/scratch/x-wding2/Projects/pyballc/Pool179_Plate1-1-I3-A14.allc.tsv.gz"
ballc_path = "test.ballc"
chrom_size_path = os.path.expanduser("~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes")
assembly_text = "test"
header_text = "header_test"
sc = True
pyballc.AllcToBallC(allc_path, ballc_path, chrom_size_path,
            assembly_text, header_text, sc)
```