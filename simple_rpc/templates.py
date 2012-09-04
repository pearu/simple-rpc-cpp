client_header = '''
/*
  This file is generated using simple_rpc script.

  For more information, see
    http://code.google.com/p/simple-rpc-cpp/
*/

#ifndef %(FILENAME)s_RPC_HPP_DEFINED
#define %(FILENAME)s_RPC_HPP_DEFINED
#ifdef DISABLE_SIMPLE_RPC
#define SIMPLE_RPC_CONNECT(HOST, PORT, DEBUG_LEVEL)
#include "%(original_filename)s"
#else
#define SimpleRPC SimpleRPC_%(namespace)s
#include "SimpleRPC.hpp"
namespace simple_rpc 
{ 
  %(special_prototypes)s
  namespace %(namespace)s 
  {
#include "%(original_filename)s"
  }
}
#endif
#endif
'''

client_source = '''
/*
  This file is generated using simple_rpc script.

  For more information, see
    http://code.google.com/p/simple-rpc-cpp/
*/

#include "%(namespace)s-rpc.hpp"

namespace simple_rpc
{

int SimpleRPC::debug_level = 0;
unsigned short SimpleRPC::port = 0;
std::string SimpleRPC::host = "";
bool SimpleRPC::success = false;

}

%(function_implementations)s

'''

function_implementation = '''
  %(function_prototype)s
  {
    static const uint32_t %(srpc)sfunction_magic = %(function_magic)s;
    static const uint32_t %(srpc)sexpected_server_magic = %(server_magic)s;
    boost::asio::io_service %(srpc)sio_service;
    simple_rpc::Socket %(srpc)ssocket(%(srpc)sio_service, "%(function_name)s", simple_rpc::SimpleRPC::get_debug_level());
    if (simple_rpc::SimpleRPC::establish_connection(%(srpc)sio_service, %(srpc)ssocket))
    {
      uint32_t %(srpc)sserver_magic = 0;
      uint64_t %(srpc)sconnection_magic = 0;
      uint64_t %(srpc)send_connection_magic = 0;
      uint64_t %(srpc)scounter = 0;
      if (%(srpc)ssocket.read_scalar (%(srpc)sserver_magic, "server_magic", -1)
          && (%(srpc)sserver_magic == %(srpc)sexpected_server_magic) // server is ready
          && %(srpc)ssocket.write_scalar(%(srpc)sfunction_magic, "function_magic", -1)
          && %(srpc)ssocket.read_scalar(%(srpc)sconnection_magic, "connection_magic", -1)
          && (%(srpc)scounter = %(srpc)sconnection_magic >> 32)
          && ((%(srpc)sconnection_magic & 0xffffffff)==%(srpc)sfunction_magic)) // server is knowledgeable
      {

        if (%(send_arguments)s)
        {
          %(return_declaration)s
          if (%(recieve_results)s
              && %(srpc)ssocket.read_scalar(%(srpc)send_connection_magic, "end_connection_magic", -1)
              && (%(srpc)sconnection_magic==%(srpc)send_connection_magic) // check for surprises
             )
          {
            %(return_statement)s
          }
          else
            std::cerr << "%(function_name)s-rpc["<<%(srpc)scounter<<"] ERROR: failed to recieve results" <<std::endl;
        }
        else
          std::cerr << "%(function_name)s-rpc["<<%(srpc)scounter<<"] ERROR: failed to send arguments" <<std::endl;
      }
      else
        {
          std::cerr << "%(function_name)s-rpc["<<%(srpc)scounter<<"] ERROR: handshake failed" <<std::endl;
          std::cerr << "  function_magic="<<%(srpc)sfunction_magic<<"(%(function_magic)sul)"<<std::endl;
          std::cerr << "  server_magic="<< %(srpc)sserver_magic<<" (expected:"<< %(srpc)sexpected_server_magic<<")"<<std::endl;
          std::cerr << "  connection_magic="<< %(srpc)sconnection_magic<<std::endl;
        }
    }
    else
      std::cerr << "%(function_name)s-rpc ERROR: failed to connect" <<std::endl;
  }
'''

server_source = '''
/*
  This file is generated using simple_rpc script.

  For more information, see
    http://code.google.com/p/simple-rpc-cpp/
*/

#include "%(original_filename)s"

#include "Socket.hpp"

main()
{
  int %(srpc)sdebug_level = 0;
  unsigned short %(srpc)sport = 2340;
  uint64_t %(srpc)scounter = 0;
  uint32_t %(srpc)sserver_magic = %(server_magic)sul;
  boost::asio::io_service %(srpc)sio_service;
  boost::asio::ip::tcp::resolver %(srpc)sresolver(%(srpc)sio_service);
  try
  {
    boost::asio::ip::tcp::acceptor %(srpc)sacceptor(%(srpc)sio_service,
                                            boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), %(srpc)sport));
    for (;;)
    {
      uint32_t %(srpc)sfunction_magic = 0;
      uint64_t %(srpc)sconnection_magic = 0;
      simple_rpc::Socket %(srpc)ssocket(%(srpc)sio_service, "rpc-server", %(srpc)sdebug_level);
      if (%(srpc)sdebug_level>0)
        std::cout << "rpc-server["<<(%(srpc)scounter+1)<<"] waits connection via port "<<%(srpc)sport<<"..."; std::cout.flush ();
      %(srpc)sacceptor.accept(%(srpc)ssocket);
      %(srpc)scounter ++;
      if (%(srpc)sdebug_level>0)
      std::cout << "connected!" << std::endl;

      if (%(srpc)ssocket.write_scalar(%(srpc)sserver_magic, "server_magic", -1)
          && %(srpc)ssocket.read_scalar(%(srpc)sfunction_magic, "function_magic", -1)
          && ((%(srpc)sconnection_magic = (%(srpc)scounter << 32) | %(srpc)sfunction_magic))
          && %(srpc)ssocket.write_scalar(%(srpc)sconnection_magic, "connection_magic", -1)
         )
      {
        switch (%(srpc)sfunction_magic)
        {
           %(server_switch_cases)s
           default :
             std::cerr << "rpc-server["<<%(srpc)scounter<<"] ERROR: unknown function_magic=="<<%(srpc)sfunction_magic<<std::endl;
        }
      }
      else
      {
        std::cerr << "rpc-server["<<%(srpc)scounter<<"] ERROR: handshake failed" <<std::endl;
      }
    }
  }
  catch (std::exception& e)
  {
    std::cerr << "rpc-server["<<%(srpc)scounter<<"] EXCEPTION: " << e.what() << std::endl;
  }
}
'''

server_switch_case = '''
case %(function_magic)s :
  {
     %(variable_declarations)s
     %(return_declaration)s
     if (%(recieve_arguments)s)
     {
       %(function_call)s
       if (%(send_results)s
           && %(srpc)ssocket.write_scalar(%(srpc)sconnection_magic, "connection_magic", -1)
          ) {}
       else
         std::cerr << "rpc-server["<<%(srpc)scounter<<"] ERROR: failed to send %(function_name)s results" <<std::endl;
     }
     else
       std::cerr << "rpc-server["<<%(srpc)scounter<<"] ERROR: failed to recieve %(function_name)s arguments" <<std::endl;
  }
  continue;
'''

