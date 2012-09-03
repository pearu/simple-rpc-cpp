
#include <cstdlib>

namespace simple_rpc {
  namespace stdlib {
    void exit ( int status );
    int system ( const char * command );
    void * malloc ( size_t size );
    void * memset ( void * ptr, int value, size_t num );
    void free ( void * ptr );
  } 
}




