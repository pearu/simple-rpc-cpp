
#ifdef SimpleRPC
#include "SimpleRPC.hpp"
#endif

#include <iostream>
#include <typeinfo> 
#include <sys/time.h>

#include "stdlib.hpp"

main()
{
#ifdef SimpleRPC
  simple_rpc::SimpleRPC rpc("127.0.0.1", 2340, 0);
  if (!rpc)
    {
      std::cout << "Failure in creating connection to RPC server. Quiting," << std::endl;
      return 1;
    }
#endif

#ifdef SimpleRPC
  /*
  std::cout << "Calling exit.." << std::endl; 
  simple_rpc::stdlib::exit(1); // this will force RPC server to exit with given return status
  */

  char * command = (char*)simple_rpc::stdlib::malloc(3);
  simple_rpc::stdlib::memset(command, 'l', 1);
  simple_rpc::stdlib::memset(command+1, 's', 1);
  simple_rpc::stdlib::memset(command+2, 0, 1);
  simple_rpc::stdlib::system(command);
  simple_rpc::stdlib::free(command);
#endif
  std::cout << "EOF main" << std::endl; 
}
