CC = g++
CFLAGS = -fPIC -shared -w -std=c++11 -O3 #-finline-functions -fPIC -Wno-unused-result
CLIB = -L${CONDA_PREFIX}/lib -lhts -ldeflate -lbz2 -lpthread -lz -lstdc++
PYINCLUDE = $(shell python3-config --includes)
CINCLUDE =  -I${CONDA_PREFIX}/include
SRCDIR = ballcools/src
TRTDIR = pyballc

LIB = ${SRCDIR}/allc.cc ${SRCDIR}/ballc.cc ${SRCDIR}/ballc_index.cc ${SRCDIR}/ballc_index_core.cc ${SRCDIR}/ballc_iterator.cc ${SRCDIR}/context_matcher.cc ${SRCDIR}/meta_indexing.cc ${SRCDIR}/timer.cc ${SRCDIR}/utils.cc


${TRTDIR}/_pyballcools.so: ${TRTDIR}/pyballcools_wrap.cxx ${LIB}
	${CC} -I${SRCDIR} ${PYINCLUDE} ${CINCLUDE} ${CLIB}  $< ${LIB} ${CFLAGS} -o $@


#${TRTDIR}/pyballcools_wrap.cxx: ${SRCDIR}/*.cc ${SRCDIR}/*.h ${TRTDIR}/pyballcools.i
#	swig  -o $@ -I${SRCDIR} -c++ -python ${TRTDIR}/pyballcools.i 
