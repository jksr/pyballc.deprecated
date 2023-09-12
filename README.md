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
pyballc --help
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

     header
       Print ballc file header.

     query
       Query ballc file with or without cmeta index.
```
##### Extract all C positon from given fasta file
```shell
pyballc cmeta --help
INFO: Showing help with the command 'pyballc cmeta -- --help'.

NAME
    pyballc cmeta - Extract all C position from fasta file.

SYNOPSIS
    pyballc cmeta FASTA_PATH CMETA_PATH

DESCRIPTION
    Extract all C position from fasta file.

POSITIONAL ARGUMENTS
    FASTA_PATH
        path for fasta file
    CMETA_PATH
        path for the output cmeta file.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
        
pyballc cmeta ~/Ref/mm10/mm10_ucsc_with_chrL.fa mm10_with_chrL_cmeta.txt
# or
pyballc cmeta -f ~/Ref/mm10/mm10_ucsc_with_chrL.fa -c mm10_with_chrL_cmeta.txt
```

##### allc to ballc
```shell
pyballc a2b --help
INFO: Showing help with the command 'pyballc a2b -- --help'.

NAME
    pyballc a2b - Convert allc file into ballc file.

SYNOPSIS
    pyballc a2b ALLC_PATH BALLC_PATH <flags>

DESCRIPTION
    Convert allc file into ballc file.

POSITIONAL ARGUMENTS
    ALLC_PATH
        input allc file path.
    BALLC_PATH
        output ballc path, will be indexed automatically.

FLAGS
    -c, --chrom_size_path=CHROM_SIZE_PATH
        Type: Optional[]
        Default: None
    -a, --assembly_text=ASSEMBLY_TEXT
        Default: ''
        text to be added
    -h, --header_text=HEADER_TEXT
        Default: ''
        text to be added
    -s, --sc=SC
        Default: True
        whether single cell file?

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

```shell
ls FC_E17a_3C_8-6-I15-M23.allc.tsv.gz -sh
# 11M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz

zcat FC_E17a_3C_8-6-I15-M23.allc.tsv.gz |wc -l
# 3025059

zcat FC_E17a_3C_8-6-I15-M23.allc.tsv.gz |head
```
```shell
chr1	3004019	+	CAC	0	1	1
chr1	3004025	+	CTG	0	1	1
chr1	3004030	+	CTC	0	1	1
chr1	3004032	+	CAG	0	1	1
chr1	3004040	+	CCT	0	1	1
chr1	3004041	+	CTA	0	1	1
chr1	3004049	+	CAA	0	1	1
chr1	3004055	+	CAA	0	1	1
chr1	3004065	+	CTT	0	1	1
chr1	3004083	+	CAA	0	1	1
```

```shell        
time pyballc a2b FC_E17a_3C_8-6-I15-M23.allc.tsv.gz test.ballc -c ~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes --assembly_text test -h test_header -s
# or
time pyballc a2b --allc_path FC_E17a_3C_8-6-I15-M23.allc.tsv.gz -b test.ballc -c ~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes --assembly_text test -h test_header -s
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

##### View ballc header
```shell
pyballc header -b test.ballc -c mm10_with_chrL_cmeta.txt.gz
```

```
version_minor: 1
sc: 1
assembly_text: test
l_assembly: 4
header_text: test header
l_text: 11
refs: Swig Object of **
n_refs: 67
```

##### Query ballc
```shell
pyballc query --help
INFO: Showing help with the command 'pyballc query -- --help'.

NAME
    pyballc query - Query ballc file with or without cmeta index.

SYNOPSIS
    pyballc query BALLC_PATH <flags>

DESCRIPTION
    Query ballc file with or without cmeta index.

POSITIONAL ARGUMENTS
    BALLC_PATH
        path for ballc file.

FLAGS
    --cmeta_path=CMETA_PATH
        Type: Optional[]
        Default: None
        path for cmeta file
    --chrom=CHROM
        Default: '*'
        chromosome, "*" to query all records.
    -s, --start=START
        Type: Optional[]
        Default: None
        start position, if chrom=="*", start can be ignored.
    -e, --end=END
        Type: Optional[]
        Default: None
        start position, if chrom=="*", start can be ignored.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```
```shell
pyballc query test.ballc --cmeta_path ~/Ref/mm10/annotations/mm10_with_chrL_cmeta.txt.gz --chrom chr1 -s 3004025 -e 3004055
```
##### ballc to allc
```shell
pyballc b2a --help
INFO: Showing help with the command 'pyballc b2a -- --help'.

NAME
    pyballc b2a - Convert ballc file into allc path.

SYNOPSIS
    pyballc b2a BALLC_PATH CMETA_PATH ALLC_PATH <flags>

DESCRIPTION
    Convert ballc file into allc path.

POSITIONAL ARGUMENTS
    BALLC_PATH
        input ballc path, should be indexed
    CMETA_PATH
    ALLC_PATH
        output allc file

FLAGS
    -w, --warn_mismatch=WARN_MISMATCH
        Default: True
    -e, --err_mismatch=ERR_MISMATCH
        Default: True
    -s, --skip_mismatch=SKIP_MISMATCH
        Default: True
    -c, --c_context=C_CONTEXT
        Default: '*'

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

```shell
time pyballc b2a -b test.ballc --cmeta_path ~/Ref/mm10/annotations/mm10_with_chrL_cmeta.txt.gz -a test.allc
```

```shell
Converting BAllC to AllC
Compressing AllC
Indexing AllC
Converting BAllC to AllC finished
test.allc

real    14m56.884s
user    14m46.040s
sys     0m7.990s
```

test.ballc could be further gzipped to reduce the file size.
```shell
gzip test.ballc
```

file sizes
```shell
 11M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz  1.0M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz.tbi   
 11M test.allc.gz  1.0M test.allc.gz.tbi  512K test.ballc.bci  4.5M test.ballc.gz
```

#### 2. Python API
Read ballc
```python
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