
#include "stdlib-rpc.hpp"

#include <iostream>
#include <typeinfo> 
#include <sys/time.h>


main()
{
  SIMPLE_RPC_CONNECT("127.0.0.1", 2340, 0);

#ifdef SimpleRPC
  using namespace simple_rpc;
  /*
  std::cout << "Calling exit.." << std::endl; 
  stdlib::exit(1); // this will force RPC server to exit with given return status
  */

  char * command = (char*)stdlib::malloc(3);
  stdlib::memset(command, 'l', 1);
  stdlib::memset(command+1, 's', 1);
  stdlib::memset(command+2, 0, 1);
  stdlib::system(command);

  stdlib::free(command);

  stdlib::system(std::string("pwd"));
#endif
  std::cout << "EOF main" << std::endl; 
}
