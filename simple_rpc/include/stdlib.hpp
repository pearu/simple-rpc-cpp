/*
  stdlib.hpp

  Author: Pearu Peterson
  Created: September 2012
 */


#ifndef SIMPLE_RPC_STDLIB_HPP_DEFINED
#define SIMPLE_RPC_STDLIB_HPP_DEFINED

#include <string>
#include <cstdlib>

int system ( const std::string & command );

#ifdef SimpleRPC 
/* This is special hack to wrap standard C/C++ library functions, in
   general.  Since the corresponding header files are convolved
   (prototypes are hard to find and may depend on CPP macro
   definitions), here we define few stdlib function prototypes
   that simple_rpc will use to construct the corresponding RPC
   wrapper functions. These prototypes should not be visibile
   to RPC server code in order to avoid declaration conflicts
   but must be exposed to RPC client code as they are prototypes
   of wrapper functions (living in simple_rpc::stdlib namespace).
   Hence the usage of `#ifdef SimpleRPC`.
 */

void exit ( int status );
int system ( const char * command );

void * malloc ( size_t size );
void * memset ( void * ptr, int value, size_t num );
void free ( void * ptr );
#endif

#endif
