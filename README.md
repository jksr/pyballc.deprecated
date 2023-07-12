# pyballc
Pyballc is a python module to reading/manipulating BAllC files. It is based on the [BAllCools](https://github.com/jksr/ballcools).

_Currently only reading and querying operations are supported, but more is comming:wink:_


### Dependency
```g++``` (with -std=c++11 supported)

```libhts``` (```conda``` installation recommended)

```libdeflated``` (this is libhts' dependency. so it should be available if libhts is correctly installed)

```libz``` (usually no installation needed. should be available for most systems)

```libbz2``` (usually no installation needed. should be available for most systems)


### Installation
pyballc is a stand alone package. You don't need to install BAllCools separately.

To install, run
```bash
git clone https://jksr@github.com/jksr/pyballc
cd pyballc
git submodule init 
git submodule update 
pip install .
```

### Usage
see ```test``` for examples
