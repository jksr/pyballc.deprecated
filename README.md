# pyballc

[![PyPI version](https://badge.fury.io/py/pyballc.svg)](https://badge.fury.io/py/pyballc)


Pyballc is a python module to read/manipulate BAllC files. It is based on the [BAllCools](https://github.com/jksr/ballcools).

_Currently only reading and querying operations are supported, but more is comming:wink:_


## Dependency
```g++``` (with -std=c++11 supported)

```libhts``` (```conda``` installation recommended)

```libdeflated``` (this is libhts' dependency. so it should be available if libhts is correctly installed)

```libz``` (usually no installation needed. should be available for most systems)

```libbz2``` (usually no installation needed. should be available for most systems)


## Installation
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

## Usage
### 1. Command Line
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
#### Extract all C positon from given fasta file
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

#### allc to ballc
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
# 11M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz (11152529 bytes)
# plain text (77M, 80675455)

zcat FC_E17a_3C_8-6-I15-M23.allc.tsv.gz |wc -l
# 3025059

zcat FC_E17a_3C_8-6-I15-M23.allc.tsv.gz |head
```
```text
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

# test.ballc
# 5M, 5107194 bytes
```

```text
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

#### View ballc header
```shell
pyballc header -b test.ballc -c mm10_with_chrL_cmeta.txt.gz
```

```text
version_minor: 1
sc: 1
assembly_text: test
l_assembly: 4
header_text: test header
l_text: 11
refs: Swig Object of **
n_refs: 67
```

#### Query ballc
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
#### ballc to allc
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

```text
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
```text
 11M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz  1.0M FC_E17a_3C_8-6-I15-M23.allc.tsv.gz.tbi   
 11M test.allc.gz  1.0M test.allc.gz.tbi  512K test.ballc.bci  4.5M test.ballc.gz
```

### 2. Python API
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

### 3. Conversion time
```shell
mkdir -p test_ballc
gsutil ls gs://mouse_pfc/allc/devel_1 > test_allc_path.txt
```

#### Randomly select 100 allc files
```python
import random
with open("test_allc_path.txt",'r') as f:
    lines=f.readlines()
allc_files=[line.strip() for line in lines if '.tbi' not in line]
selected_allc_files=random.sample(allc_files,100)
with open("100allc.txt",'w') as f:
    for file in selected_allc_files:
        f.write(file+'\n')
```
#### Download 100 allc files
```shell
mkdir allc_files
cat 100allc.txt | while read path; do
    echo ${path}
    gsutil -m cp -n ${path}* allc_files
  done;
```

#### Test allc to ballc speed
Machine information:
```text
Machine type: n2-standard-4
vCPU: 4
Memory: 16GB
```
#### Conversion
```shell
mkdir -p ballc
# Convert one by one
```

### 4. Storage reduction
```python
import os,sys
import pandas as pd
df=pd.DataFrame([f.replace('.ballc','') for f in os.listdir("./") if f .endswith('.ballc')],
                columns=['SampleID'])
df['allc_size']=df.SampleID.apply(lambda x:os.path.getsize(f"allc/{x}.allc.tsv"))
df['allc_gz_size']=df.SampleID.apply(lambda x:os.path.getsize(f"{x}.allc.tsv.gz"))
df['ballc_size']=df.SampleID.apply(lambda x:os.path.getsize(f"{x}.ballc"))
df['gz_reduce']=(df.allc_gz_size - df.ballc_size) / df.allc_gz_size
df['plain_text_reduce']=(df.allc_size - df.ballc_size) / df.allc_size
print("Average reduce size for *allc.tsv.gz: %s"%(df.gz_reduce.mean() * 100))
print("Average reduce size for *allc.tsv: %s"%(df.plain_text_reduce.mean() * 100))
def wc(file):
    f=open(file,'r')
    i=0
    line=f.readline()
    while line:
        i+=1
        line=f.readline()
    f.close()
    return i

df['No.Records']=df.SampleID.apply(lambda x:wc(f"allc/{x}.allc.tsv"))
print("Average No. of records: %s"%(df['No.Records'].mean()))
df
```
```text
Average reduce size for *allc.tsv.gz: 55.338291329041
Average reduce size for *allc.tsv: 93.49512318067059
Average No. of records: 32294578.555555556
                         SampleID   allc_size  allc_gz_size  ballc_size  gz_reduce  plain_text_reduce  No.Records
0    AG_JF1NQ_AR_Plate10-1-I15-J1   691536116     100832383    44997569   0.553739           0.934931    25906516
1   AG_JF1NQ_AR_Plate10-1-I15-C14  1003919255     146296085    65225519   0.554154           0.935029    37604603
2   AG_JF1NQ_AR_Plate10-1-I15-M13   956987899     139472976    62259197   0.553611           0.934943    35844682
3   AG_JF1NQ_AR_Plate10-1-I15-D13  1078080507     156790589    70040827   0.553284           0.935032    40379983
4   AG_JF1NQ_AR_Plate10-1-I15-P13   956937535     139306655    62271268   0.552991           0.934927    35841634
..                            ...         ...           ...         ...        ...                ...         ...
58   AG_JF1NQ_AR_Plate10-1-I15-L1  1038034137     151099535    67577030   0.552765           0.934899    38881334
59  AG_JF1NQ_AR_Plate10-1-I15-A14  1006003011     146344525    65182630   0.554595           0.935206    37682515
60  AG_JF1NQ_AR_Plate10-1-I15-H13   894854438     130280878    57995033   0.554846           0.935191    33517883
61  AG_JF1NQ_AR_Plate10-1-I15-N14  1007703326     146931230    65661719   0.553113           0.934840    37744544
62   AG_JF1NQ_AR_Plate10-1-I15-O1   853060638     124311383    55627544   0.552514           0.934791    31955764

[63 rows x 7 columns]
```


### 5. merge
```shell
time ballcools merge -f test/ballc_path.txt test/merged.ballc
#Merging finished. 63 ballc files.

#real    51m58.078s
#user    50m41.804s
#sys     0m32.174s
```

### 6. Usage for non-single cell datasets
#### Create meta index file
```shell
mkdir Mammal40
wget https://github.com/zhou-lab/InfiniumAnnotationV1/raw/main/Anno/Mammal40/Mammal40.hg38.manifest.tsv.gz
# create cmeta index file
awk 'BEGIN{FS=OFS="\t"};{if(NR >1 && $1!="NA"){print $9,1,".","CG"}}' Mammal40.hg38.manifest.tsv |sort -k 1,1 -k 2,2n |bgzip > mammal40_meta.bed.gz
tabix -f -b 2 -e 2 -s 1 mammal40_meta.bed.gz
zcat mammal40_meta.bed.gz |head
```

```text
cg00000165      1       .       CG
cg00001209      1       .       CG
cg00001364      1       .       CG
cg00001582      1       .       CG
cg00002920      1       .       CG
cg00003994      1       .       CG
cg00004555      1       .       CG
cg00005112      1       .       CG
cg00005271      1       .       CG
cg00006213      1       .       CG
```

You can chose custom field to be included in the meta index file as your wish.

#### Prepare example methylation array dataset.
Download the example dataset from GEO with accession ID: GSE173330
Similarly, one can chose custom field to be included in sample allc file, here, we choose beta value and p-value to be included in allc file for each sample.
```shell
head test.bed
```
```text
cg00000165      0.417660370297546       0.244289340101523
cg00001209      0.891975949908926       0.0056237218813906
cg00001364      0.419087384097591       0.0071574642126789
cg00001582      0.0574073237198707      0.0044416243654822
cg00002920      0.509226493083919       0.335378323108384
cg00003994      0.0494848794490276      0.0152284263959391
cg00004555      0.183195004139376       0.0431472081218274
cg00005112      0.871984516124028       0.0028118609406953
cg00005271      0.969467259727841       0.0035787321063395
cg00006213      0.962269523745587       0.0012781186094069
```
Let's add several columns to make it looks like allc file
```shell
awk 'BEGIN{FS=OFS="\t"};{print $1,1,".","CG",$2,$3}' test.bed |bgzip > test.tsv.gz
zcat test.tsv.gz |head
```
In this example test.tsv.gz, columsn are: probe ID, start position, strand, beta, pvalue
```text
cg00000165      1       .       CG      0.417660370297546       0.244289340101523
cg00001209      1       .       CG      0.891975949908926       0.0056237218813906
cg00001364      1       .       CG      0.419087384097591       0.0071574642126789
cg00001582      1       .       CG      0.0574073237198707      0.0044416243654822
cg00002920      1       .       CG      0.509226493083919       0.335378323108384
cg00003994      1       .       CG      0.0494848794490276      0.0152284263959391
cg00004555      1       .       CG      0.183195004139376       0.0431472081218274
cg00005112      1       .       CG      0.871984516124028       0.0028118609406953
cg00005271      1       .       CG      0.969467259727841       0.0035787321063395
cg00006213      1       .       CG      0.962269523745587       0.0012781186094069
```
```shell
beta=pd.read_csv("20211117_GSE173330_Mammal40_betas.txt",sep='\t',index_col=0,usecols=['GSM5265435'])
pval=pd.read_csv("20211117_GSE173330_Mammal40_pvals.txt",sep='\t',index_col=0,usecols=['GSM5265435'])
beta.rename(columns={'GSM5265435':'beta'},inplace=True)
beta['pval']=beta.index.to_series().map(pval.GSM5265435.to_dict())
idx=pd.read_csv('mammal40_meta.bed.gz',sep='\t',header=None)
use_rows=list(set(beta.index.tolist()) & set(idx[0].tolist()))
beta=beta.loc[use_rows]
beta.to_csv("test.bed",sep='\t',header=False)
```


#### Convert allc to ballc
```shell
ballcools a2b -a mammal40_meta.bed.gz test.tsv.gz test.ballc chrom_size.bed
ballcools index test.ballc
```

#### Query probe
```shell
ballcools query test.ballc cg17254774
```

#### ballc to allc
```shell
ballcools b2a test.ballc mammal40_meta.bed.gz test_allc
zcat test_allc.allc.tsv.gz |head
```

```text
cg05604535      1       .       CG      0       0       1
cg19972243      1       .       CG      0       0       1
cg20983335      1       .       CG      0       0       1
cg13951226      1       .       CG      0       0       1
cg13853159      1       .       CG      0       0       1
cg18686900      1       .       CG      0       0       1
cg15855498      1       .       CG      0       0       1
cg17254774      1       .       CG      0       0       1
cg00058449      1       .       CG      0       0       1
cg08019519      1       .       CG      0       0       1
```


file sizes
```text
-rw-rw-r-- 1 wding wding  128486 Sep 12 16:56 mammal40_meta.bed.gz
-rw-rw-r-- 1 wding wding  439202 Sep 12 16:56 mammal40_meta.bed.gz.tbi
-rw-rw-r-- 1 wding wding  169401 Sep 12 17:06 test_allc.allc.tsv.gz
-rw-rw-r-- 1 wding wding  472876 Sep 12 17:06 test_allc.allc.tsv.gz.tbi
-rw-rw-r-- 1 wding wding  200232 Sep 12 17:01 test.ballc
-rw-rw-r-- 1 wding wding  193909 Sep 12 17:01 test.ballc.bci
-rw-rw-r-- 1 wding wding 1778349 Sep 12 17:00 test.bed
-rw-rw-r-- 1 wding wding  609890 Sep 12 17:01 test.tsv.gz
```