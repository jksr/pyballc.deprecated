%module pyballcools

%{
#include "allc.h"
#include "ballc_files.h"
#include "ballc.h"
#include "ballc_index_core.h"
#include "ballc_index.h"
#include "ballc_iterator.h"
#include "context_matcher.h"
#include "meta_indexing.h"
#include "routines.h"
#include "timer.h"
#include "utils.h"
#include "version.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cstring>
#include <string>
#include <stdexcept>
#include <zlib.h>
#include <algorithm>
#include <sys/stat.h>
%}



%include "std_string.i"
%include "std_vector.i"
%include "std_map.i"
%include "std_unordered_map.i"
%include "std_pair.i"
%include "stdint.i"




%exception {
    try {
        $action
    } catch(const std::exception& e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch(...) {
        SWIG_exception(SWIG_RuntimeError, "An unknown exception occurred");
    }
}


%include "allc.h"
%include "ballc_files.h"
%include "ballc.h"
%include "ballc_index.h"
%include "ballc_iterator.h"
%include "meta_indexing.h"
%include "routines.h"
%include "version.h"
//%include "ballc_index_core.h"
//%include "context_matcher.h"
//%include "timer.h"
//%include "utils.h"


%apply uint32_t { uint32_t };
%apply uint16_t { uint16_t };
%apply uint64_t { uint64_t };
%apply uint8_t { uint8_t };

//%template(PairStringUInt) std::pair<std::string, unsigned int>;
//%template(PairStringString) std::pair<std::string, std::string>;
//%template(UnorderedMapPairStringUIntPairStringString) std::unordered_map<PairStringUInt, PairStringString>;

