
#include <string>
#include <cstdlib>


int system ( const std::string & command );

namespace simple_rpc {
  namespace stdlib {
    void exit ( int status );
    int system ( const char * command );
    int system ( const std::string & command );
    void * malloc ( size_t size );
    void * memset ( void * ptr, int value, size_t num );
    void free ( void * ptr );
  } 
}




