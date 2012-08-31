
client_header = '''
#ifndef %(FILENAME)s_DEFINED
#define %(FILENAME)s_DEFINED

#ifdef USE_SIMPLE_RPC

#include <iostream>
#include <boost/asio.hpp>
#include <boost/lexical_cast.hpp>
#include "Socket.hpp"

%(redefine_original_functions)s

#include "%(original_filename)s"

%(undefine_original_functions)s

#define SIMPLE_RPC_%(CodeName)s(INSTANCE, HOST, PORT) \\
  SimpleRPC_%(CodeName)s INSTANCE(HOST, PORT)

class SimpleRPC_%(CodeName)s
{

private:
  static std::string host;
  static unsigned short port;
  static bool success;
  bool m_success;

  static
  bool establish_connection(boost::asio::io_service& io_service, Socket & socket)
  {
    boost::asio::ip::tcp::resolver resolver(io_service);
    boost::asio::ip::tcp::resolver::query query(host,
                               boost::lexical_cast<std::string>(port));
    success = true;
    try
    {
      boost::asio::ip::tcp::resolver::iterator endpoint_iterator = resolver.resolve(query);
      boost::asio::connect(socket, endpoint_iterator);
    }
    catch (std::exception& e)
    {
      success = false;
      std::cerr << "establish_connection["<<host<<":"<<port<<"] ERROR: " << e.what() << std::endl;
    }
    return success;
  }

public:
  SimpleRPC_%(CodeName)s(const std::string & remote_host,
		         unsigned short remote_port)
  {
    if (host != "")
    {
      std::cerr << "SimpleRPC_%(CodeName)s("<<remote_host<<", "<<remote_port<<") ERROR: ";
      std::cerr << "already connecting to "<<host<<":"<<port<<std::endl;
      m_success = false;
    }
    else
    {
      host = remote_host; 
      port = remote_port; 
      m_success = true;
      success = true;
    }
  }
  ~SimpleRPC_%(CodeName)s () 
  {
    host = ""; 
    port = 0; 
    success = false;
  }
  operator bool () const { return m_success && success; }


%(function_methods)s

};

%(define_wrapper_functions)s

#ifdef SIMPLE_RPC_MAIN
unsigned short SimpleRPC_%(CodeName)s::port = 0;
std::string SimpleRPC_%(CodeName)s::host = "";
bool SimpleRPC_%(CodeName)s::success = false;
#undef SIMPLE_RPC_MAIN
#endif

#else

#include "%(original_filename)s"
#define SIMPLE_RPC_%(CodeName)s(INSTANCE, HOST, PORT) bool INSTANCE = true;

#endif

#endif
'''

function_method = '''
  static
  %(function_prototype)s
  {
    static const uint32_t %(srpc)sfunction_magic = %(function_magic)s;
    static const uint32_t %(srpc)sexpected_server_magic = %(server_magic)s;
    boost::asio::io_service %(srpc)sio_service;
    Socket %(srpc)ssocket( %(srpc)sio_service);
    if (establish_connection(%(srpc)sio_service, %(srpc)ssocket))
    {
      uint32_t %(srpc)sserver_magic = 0;
      uint64_t %(srpc)sconnection_magic = 0;
      uint64_t %(srpc)send_connection_magic = 0;
      uint64_t %(srpc)scounter = 0;
      if (%(srpc)ssocket.read_scalar (%(srpc)sserver_magic, "server_magic")
          && (%(srpc)sserver_magic == %(srpc)sexpected_server_magic) // server is ready
          && %(srpc)ssocket.write_scalar(%(srpc)sfunction_magic, "function_magic")
          && %(srpc)ssocket.read_scalar(%(srpc)sconnection_magic, "connection_magic")
          && (%(srpc)scounter = %(srpc)sconnection_magic >> 32)
          && ((%(srpc)sconnection_magic & 0xffffffff)==%(srpc)sfunction_magic)) // server is knowledgeable
      {

        if (%(send_arguments)s)
        {
          %(return_declaration)s
          if (%(recieve_results)s
              && %(srpc)ssocket.read_scalar(%(srpc)send_connection_magic, "end_connection_magic")
              && (%(srpc)sconnection_magic==%(srpc)send_connection_magic) // check for surprises
             )
          {
            %(return_statement)s
          }
          else
            std::cerr << "SimpleRPC_%(CodeName)s::%(function_name)s["<<%(srpc)scounter<<"] ERROR: failed to recieve results" <<std::endl;
        }
        else
          std::cerr << "SimpleRPC_%(CodeName)s::%(function_name)s["<<%(srpc)scounter<<"] ERROR: failed to send arguments" <<std::endl;
      }
      else
        {
          std::cerr << "SimpleRPC_%(CodeName)s::%(function_name)s["<<%(srpc)scounter<<"] ERROR: handshake failed" <<std::endl;
          std::cerr << "  function_magic="<<%(srpc)sfunction_magic<<"(%(function_magic)sul)"<<std::endl;
          std::cerr << "  server_magic="<< %(srpc)sserver_magic<<" (expected:"<< %(srpc)sexpected_server_magic<<")"<<std::endl;
          std::cerr << "  connection_magic="<< %(srpc)sconnection_magic<<std::endl;
        }
    }
    else
      std::cerr << "SimpleRPC_%(CodeName)s::%(function_name)s ERROR: failed to connect" <<std::endl;
  }
'''

server_source = '''
#include "%(original_filename)s"
#include "Socket.hpp"

main()
{
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
      Socket %(srpc)ssocket(%(srpc)sio_service);
      std::cout << "SimpleRPC_%(CodeName)s_server["<<(%(srpc)scounter+1)<<"] waits connection via port "<<%(srpc)sport<<"..."; std::cout.flush ();
      %(srpc)sacceptor.accept(%(srpc)ssocket);
      %(srpc)scounter ++;
      std::cout << "connected!" << std::endl;

      if (%(srpc)ssocket.write_scalar(%(srpc)sserver_magic, "server_magic")
          && %(srpc)ssocket.read_scalar(%(srpc)sfunction_magic, "function_magic")
          && ((%(srpc)sconnection_magic = (%(srpc)scounter << 32) | %(srpc)sfunction_magic))
          && %(srpc)ssocket.write_scalar(%(srpc)sconnection_magic, "connection_magic")
         )
      {
        //std::cerr << "  server_magic="<<%(srpc)sserver_magic<<std::endl;
        //std::cerr << "  connection_magic="<<%(srpc)sconnection_magic<<std::endl;
        //std::cerr << "  function_magic="<<%(srpc)sfunction_magic<<std::endl;
        switch (%(srpc)sfunction_magic)
        {
           %(server_switch_cases)s
           default :
             std::cerr << "SimpleRPC_%(CodeName)s_server["<<%(srpc)scounter<<"] ERROR: unknown function_magic=="<<%(srpc)sfunction_magic<<std::endl;
             //std::cerr << "  computed function magic="<<(%(srpc)sconnection_magic & 0xffffffff)<<std::endl;
             //std::cerr << "  recieved function magic="<<%(srpc)sfunction_magic<<std::endl;
        }
      }
      else
         std::cerr << "SimpleRPC_%(CodeName)s_server["<<%(srpc)scounter<<"] ERROR: handshake failed" <<std::endl;
    }
  }
  catch (std::exception& e)
  {
    std::cerr << "SimpleRPC_%(CodeName)s_server["<<%(srpc)scounter<<"] EXCEPTION: " << e.what() << std::endl;
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
           && %(srpc)ssocket.write_scalar(%(srpc)sconnection_magic, "connection_magic")
          ) {}
       else
         std::cerr << "SimpleRPC_%(CodeName)s_server["<<%(srpc)scounter<<"] ERROR: failed to send %(function_name)s results" <<std::endl;
     }
     else
       std::cerr << "SimpleRPC_%(CodeName)s_server["<<%(srpc)scounter<<"] ERROR: failed to recieve %(function_name)s arguments" <<std::endl;
  }
  continue;
'''
