
#ifndef SOCKET_HPP_DEFINED
#define SOCKET_HPP_DEFINED

#include <string>
#include <iostream>
#include <boost/asio.hpp>


class Socket: public  boost::asio::ip::tcp::socket
{

public:
  Socket(boost::asio::io_service& io_service) : 
    boost::asio::ip::tcp::socket(io_service)
  {}
  
  template <typename T> bool write_scalar(const T &value, const std::string & name = "")
  {
    boost::system::error_code error;
    size_t len = boost::asio::write(*this, boost::asio::buffer( &value, sizeof(T) ), error);
    if (error)
      {
	std::cerr<<"write_scalar("<<name<<") error="<<error.message ()<<std::endl;
	return false;
      }
    if (len != sizeof(value))
      {
	std::cerr<<"write_scalar("<<name<<") expected to write "<<sizeof (value)<<" bytes but wrote "<<len<<std::endl;
	return false;
      }
    //std::cout<<"write_scalar("<<name<<") successfully wrote="<<value<<" sizeof="<<sizeof(T)<<std::endl;
    return true;
  }
  
  template <typename T> bool read_scalar(T &value, const std::string & name = "")
  {
    boost::system::error_code error;
    //cerr<<"read_scalar: socket bytes available="<<this->available()<<endl;
    size_t len = boost::asio::read( *this, boost::asio::buffer( &value, sizeof(T) ), error);
    if (error)
      {
	std::cerr<<"read_scalar("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != sizeof(value))
    {
      std::cerr<<"read_scalar("<<name<<") expected to read "<<sizeof (T)<<" bytes but got "<<len<<std::endl;
      return false;
    }
    //std::cout<<"read_scalar("<<name<<") successfully read="<<value<< " sizeof="<<sizeof(T)<<std::endl;
    return true;
  }
};

#endif
