/*
  Provides SimpleRPC class to hold host:port information and to
  provide establish_connection method.

  Author: Pearu Peterson
  Created: September 2012
 */

#ifndef SIMPLE_RPC_HPP_DEFINED
#define SIMPLE_RPC_HPP_DEFINED

#include <iostream>
#include <boost/asio.hpp>
#include <boost/lexical_cast.hpp>
#include "Socket.hpp"

#ifndef SimpleRPC
#error "Must define -DSimpleRPC=SimpleRPC_<server name>"
#endif

namespace simple_rpc
{

  void set_debug_level(const int & debug_level); // implementation is given in generated `*-rpc.cpp` file.

  class SimpleRPC
  {
    
  private:
    static std::string host;
    static unsigned short port;
    static bool success;
    static int debug_level;
    bool m_success;
    
  public:
    static int get_debug_level(void) { return debug_level; }
    
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
    SimpleRPC(const std::string & remote_host,
	      unsigned short remote_port,
	      int debug_level = 0)
    {
      SimpleRPC::debug_level = debug_level;
      if (host != "")
	{
	  std::cerr << "SimpleRPC("<<remote_host<<", "<<remote_port<<") ERROR: ";
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
      set_debug_level(debug_level);
    }
    ~SimpleRPC() 
    {
      host = ""; 
      port = 0; 
      success = false;
    }
    operator bool () const { return m_success && success; }
    
  };
}

#endif
