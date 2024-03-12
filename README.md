> # Warming: This package is deprecated
> This package relies on the 3rd party software SWIG to port C/C++ functions to python. On rare cases, the SWIG proting could give incorrect results when querying a ballc file. Unfortunatedly, it too complicated to solve this bug in a short time frame since SWIG is implicated. Therefore, we decide to make this implementation deprecated and we are working on a new version of pyballc which does not rely on SWIG. Please stay tuned and the new one will come soon.





----------------------------
----------------------------
----------------------------
















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
Comprssed allc.tsv.gz
vim run_a2b.sh
```shell
mkdir -p ballc
#find ../allc -name "*.allc.tsv.gz" > allc_path.txt 

cat 1000_allc_path.txt | while read allc; do
  sname=$(basename ${allc})
  prefix=${sname/.allc.tsv.gz/}
  echo "SampleID" :${prefix}
  /usr/bin/time -f "%e\t%M\t%P" ballcools a2b -a mm10_with_chrL_cmeta.txt.gz ${allc} ballc/${prefix}.ballc ~/Ref/mm10/mm10_ucsc_with_chrL.chrom.sizes
  zcat ${allc} | wc -l
  ls -l ${allc}
  echo "----"
done;
```
```shell
nohup bash run_a2b.sh > a2b.log &
````

```python
import os, sys
import pandas as pd

infile = "a2b.log"
with open(infile, 'r') as f:
	data = f.read()
records = data.split('----\n')
R = []
for record in records:
	if "SampleID :" not in record:
		continue
	lines = record.strip().split('\n')
	if len(lines) < 5:
		continue
	sname = lines[0].lstrip('SampleID :').strip()
	if len(lines) == 5:
		time, memory, _ = lines[-1].split('\t')
		R.append([sname, time, memory])
	else:
		time, memory, _ = lines[-3].split('\t')
		line_num = lines[-2].split(' ')[0].strip()
		file_size = lines[-1].split(' ')[4]
		R.append([sname, time, memory, line_num, file_size])

if len(R[0]) == 3:
	df = pd.DataFrame(R, columns=['SampleID', 'Time', 'Memory'])
	df['allc_gz_size'] = df.SampleID.apply(lambda x: os.path.getsize(f"allc_files/{x}.allc.tsv.gz"))
	df.rename(columns={'Time': 'gz_time', 'Memory': 'gz_memory'}, inplace=True)
	df.to_csv("time_memory_usage_gz_version.txt", sep='\t', index=False)
else:
	df = pd.DataFrame(R, columns=['SampleID', 'time', 'memory', 'line_num', 'allc_size'])
    df['ballc_size']=df.SampleID.apply(lambda x:os.path.getsize(f"ballc/{x}.ballc"))
	df.to_csv("time_memory_usage.txt", sep='\t', index=False)
```

```python
import os
import pandas as pd

df = pd.read_csv("time_memory_usage.txt", sep='\t', index_col=0)

print("1000 allc files:")
print("Median number of lines for *allc.tsv: %s in %s allc files" % (int(df.line_num.median()),df.shape[0]))
print("Median file size for *allc.tsv.gz: %s MB" % ((df.allc_size / 1024 /1024).median()))
print("Median reduce size for *allc.tsv.gz: %s" % (((df.allc_size - df.ballc_size) / df.allc_size).median() * 100))
print("Median time usage to convert allc.tsv.gz to ballc: %s seconds" % (df.time.median()))
print("Median peak memory usage to convert allc.tsv.gz to ballc: %s MB" % (df.memory.median() / 1024))

df=df.sample(500)

```

```text
1000 allc files:
Median number of lines for *allc.tsv: 33503256 in 1000 allc files
Median file size for *allc.tsv.gz: 120.70244932174683 MB
Median reduce size for *allc.tsv.gz: 51.671223148772924
Median time usage to convert allc.tsv.gz to ballc: 51.905 seconds
Median peak memory usage to convert allc.tsv.gz to ballc: 24.21875 MB


```

### 4. Merge (1 core, 20G memory)
ballcools merge
```shell
for file in `ls ballc`; do ballcools index ballc/${file}; done;

find ballc -name *.ballc > ballc_path.txt
/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f ballc_path.txt merged.ballc

/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 500_ballc_path.txt 500_merged.ballc
/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 100_ballc_path.txt 100_merged.ballc
/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 50_ballc_path.txt 50_merged.ballc
/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 10_ballc_path.txt 10_merged.ballc


/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 750_ballc_path.txt 750_merged.ballc
/usr/bin/time -f "%e\t%M\t%P" ballcools merge -f 250_ballc_path.txt 250_merged.ballc
````

```text
Merging finished (1000 files)
13952.71        16285288        59%
3.88 h; 15.5GB memory


Merging finished (750 files)
11036.53        13327184        59%

Merging finished (500 files)
7878.89 8250068 63%

Merging finished (250 files)
4605.19 4265344 75%

Merging finished (100 files)
2282.19 1854276 98%

Merging finished (50 files)
1710.55 1022428 99%

Merging finished (10 files)
400.98  249280  99%
```

allcools merge
```python
import pandas as pd
import os,sys
df1=pd.read_csv("allc_path.txt",sep='\t',header=None,names=['path'])
df1['SampleID']=df1.path.apply(lambda x:os.path.basename(x).rstrip('.allc.tsv.gz'))
D=df1.set_index('SampleID').path.to_dict()
outdir="allc_path"

for file in os.listdir("ballc_path"):
	df = pd.read_csv(os.path.join("ballc_path", file), sep='\t', header=None, names=['ballc_path'])
	df['SampleID'] = df.ballc_path.apply(lambda x: os.path.basename(x).rstrip('.ballc'))
	df['allc_path']=df.SampleID.map(D)
	df.allc_path.to_csv(os.path.join(outdir,file.replace('ballc','allc')),sep='\t',index=False,header=False)
```
```shell
# allcools merge 
for no in "1000" "500" "100" "50" "10"; do
  echo ${no}
  /usr/bin/time -f "%e\t%M\t%P" allcools merge --cpu 20 --allc_paths allc_path/${no}_allc_path.txt --output_path ${no}_merged_allc.tsv.gz --chrom_size_path ~/Ref/mm10/mm10_ucsc.nochrM.sizes > ${no}.log 2>&1
done;
```

```text
merge finished (1000 files)
24187.61        4629032 767%

merge finished (500)
12125.63        4344556 820%

merge finished (100)
2404.86 3844580 851%

merge finished (50)
1880.39 2742552 824%

merge finished (10)
521.13  1053168 792%
```

| Number of Files | Tools     | No.CPU | Merge Time (Second) | Merge Time (Hour) | Memory Peak (KB) | Memory Peak (GB) |
| --------------- | --------- | ------ | ------------------- | ----------------- | ---------------- | ---------------- |
| 1000            | ballcools | 1      | 13952.71            | 3.875752778       | 16285288         | 15.5308609       |
| 750             | ballcools | 1      | 11036.53            | 3.065702778       | 13327184         | 12.70979309      |
| 500             | ballcools | 1      | 7878.89             | 2.188580556       | 8250068          | 7.86787796       |
| 250             | ballcools | 1      | 4605.19             | 1.279219444       | 4265344          | 4.067749023      |
| 100             | ballcools | 1      | 2282.19             | 0.633941667       | 1854276          | 1.768375397      |
| 50              | ballcools | 1      | 1710.55             | 0.475152778       | 1022428          | 0.975063324      |
| 10              | ballcools | 1      | 400.98              | 0.111383333       | 249280           | 0.237731934      |
| 1000            | allcools  | 20     | 24187.61            | 6.718780556       | 4629032          | 4.414588928      |
| 500             | allcools  | 20     | 12125.63            | 3.368230556       | 4344556          | 4.143291473      |
| 100             | allcools  | 20     | 2404.86             | 0.668016667       | 3844580          | 3.666477203      |
| 50              | allcools  | 20     | 1880.39             | 0.522330556       | 2742552          | 2.615501404      |
| 10              | allcools  | 20     | 521.13              | 0.144758333       | 1053168          | 1.004379272      |

### 5. Usage for non-single cell datasets
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
