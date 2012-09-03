/*
  Provides Socker class that extends boost::asio::ip::tcp::socket with
  various read and write methods.

  Author: Pearu Peterson
  Created: September 2012
 */

#ifndef SOCKET_HPP_DEFINED
#define SOCKET_HPP_DEFINED

#include <string>
#include <iostream>
#include <typeinfo> 
#include <boost/asio.hpp>
#include <boost/serialization/map.hpp>
#include <boost/serialization/set.hpp>
#include <boost/serialization/list.hpp>
#include <boost/serialization/deque.hpp>
#include <boost/serialization/vector.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>

#include <sys/time.h>

namespace simple_rpc
{

class Socket: public  boost::asio::ip::tcp::socket
{
private:
  int m_debug_level;
  std::string m_appname;

private:
  template <typename T> size_t size_bytes(const std::vector<T>& value) { return sizeof(T) * value.size(); } 
  size_t size_bytes(const std::string& value) { return sizeof(char)*value.size(); } 

public:
  Socket(boost::asio::io_service& io_service, std::string appname = "", int debug_level = 0) : 
    boost::asio::ip::tcp::socket(io_service),
    m_appname(appname),
    m_debug_level(debug_level)
  {}
  
  template <typename T> bool write_scalar(const T &value, const std::string & name = "", int delta_debug = 0)
  {
    boost::system::error_code error;
    size_t len = boost::asio::write(*this, boost::asio::buffer( &value, sizeof(T) ), error);
    if (error)
      {
	std::cerr<<m_appname<<":write_scalar<"<<typeid(T).name()<<">("<<name<<") error="<<error.message ()<<std::endl;
	return false;
      }
    if (len != sizeof(value))
      {
	std::cerr<<m_appname<<":write_scalar<"<<typeid(T).name()<<">("<<name<<") expected to write "<<sizeof(T)<<" bytes but wrote "<<len<<std::endl;
	return false;
      }
    if (m_debug_level+delta_debug>1)
      std::cout<<m_appname<<":write_scalar<"<<typeid(T).name()<<">("<<name<<") successfully wrote="<<value<<" sizeof="<<sizeof(T)<<"|"<<sizeof(value)<<std::endl;
    return true;
  }
  
  template <typename T> bool read_scalar(T &value, const std::string & name = "", int delta_debug = 0)
  {
    boost::system::error_code error;
    size_t len = boost::asio::read( *this, boost::asio::buffer( &value, sizeof(T) ), error);
    if (error)
      {
	std::cerr<<m_appname<<":read_scalar<"<<typeid(T).name()<<">("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != sizeof(value))
    {
      std::cerr<<m_appname<<":read_scalar<"<<typeid(T).name()<<">("<<name<<") expected to read "<<sizeof (T)<<" bytes but got "<<len<<std::endl;
      return false;
    }
    if (m_debug_level + delta_debug>1)
      std::cout<<m_appname<<":read_scalar<"<<typeid(T).name()<<">("<<name<<") successfully read="<<value<< " sizeof="<<sizeof(T)<<"|"<<sizeof(value)<<std::endl;
    return true;
  }
  
  template <typename T> bool write_serial(const T &value, const std::string & name = "")
  {
    std::ostringstream archive_stream;
    boost::archive::text_oarchive archive(archive_stream);
    archive << value;
    return write_string(archive_stream.str(), name + "_serialized");

  }

  template <typename T> bool read_serial(T &value, const std::string & name = "")
  {
    std::string inbound_data;
    if (!read_string(inbound_data, name + "_serialized"))
      return false;
    std::istringstream archive_stream(inbound_data);
    boost::archive::text_iarchive archive(archive_stream);
    archive >> value;
    return true;
  }
  
  template <typename T> bool write_vector(const std::vector<T> &value, const std::string & name = "")
  {
    std::list< boost::asio::const_buffer > buffers;
    uint32_t sz = value.size();
    buffers.push_back( boost::asio::buffer( &sz, sizeof(sz) ) );
    buffers.push_back( boost::asio::buffer( value ) );

    boost::system::error_code error;
    size_t len = boost::asio::write(*this, buffers, error);
    if (error)
      {
	std::cerr<<m_appname<<":write_vector<"<<typeid(T).name()<<">("<<name<<") error on write: "<<error.message ()<<std::endl;
	return false;
      }
    if (len != size_bytes(value)+sizeof(sz))
      {
	std::cerr<<m_appname<<":write_vector<"<<typeid(T).name()<<">("<<name<<") expected to write "<<value.size()+sizeof(sz)<<" bytes but wrote "<<len<<std::endl;
	return false;
      }
    if (m_debug_level>1)
      std::cout<<m_appname<<":write_vector<"<<typeid(T).name()<<">("<<name<<") successfully wrote=["<<value.size()<<"]"<<std::endl;
    return true;
  }

  template <typename T> bool read_vector(std::vector<T> &value, const std::string & name = "")
  {
    boost::system::error_code error;
    uint32_t sz = 0;
    if (!read_scalar(sz, name + ".size"))
      return false;
    value.resize(sz);
    size_t len = boost::asio::read( *this, boost::asio::buffer( value ), error);
    if (error)
      {
	std::cerr<<m_appname<<":read_vector<"<<typeid(T).name()<<">("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != size_bytes(value))
    {
      std::cerr<<m_appname<<":read_vector<"<<typeid(T).name()<<">("<<name<<") expected to read "<<size_bytes(value)<<" bytes but got "<<len<<std::endl;
      return false;
    }
    if (m_debug_level>1)
      std::cout<<m_appname<<":read_vector<"<<typeid(T).name()<<">("<<name<<") successfully read "<<len<<" bytes"<<std::endl;

    return true;
  }

  bool write_string(const std::string &value, const std::string & name = "")
  {
    std::list< boost::asio::const_buffer > buffers;
    uint32_t sz = value.size();
    buffers.push_back( boost::asio::buffer( &sz, sizeof(sz) ) );
    buffers.push_back( boost::asio::buffer( value ) );
    boost::system::error_code error;
    size_t len = boost::asio::write(*this, buffers, error);
    if (error)
      {
	std::cerr<<m_appname<<":write_string("<<name<<") error on write: "<<error.message ()<<std::endl;
	return false;
      }
    if (len != size_bytes(value)+sizeof(sz))
      {
	std::cerr<<m_appname<<":write_string("<<name<<") expected to write "<<value.size()+sizeof(sz)<<" bytes but wrote "<<len<<std::endl;
	return false;
      }
    if (m_debug_level>1)
      std::cout<<m_appname<<":write_string("<<name<<") successfully wrote=["<<value.size()<<"]"<<std::endl;
    return true;
  }

  bool read_string(std::string &value, const std::string & name = "")
  {
    boost::system::error_code error;
    uint32_t sz = 0;
    if (!read_scalar(sz, name + ".size"))
      return false;
    std::vector<char> data(sz);
    size_t len = boost::asio::read( *this, boost::asio::buffer( data, sz ), error);
    if (error)
      {
	std::cerr<<m_appname<<":read_string("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != sz)
    {
      std::cerr<<m_appname<<":read_string("<<name<<") expected to read "<<value.size()<<" bytes but got "<<len<<std::endl;
      return false;
    }
    value.assign(data.begin(), data.end());
    if (m_debug_level>1)
      std::cout<<m_appname<<":read_string("<<name<<") successfully read "<<len<<" bytes='"<<value<<"'"<<std::endl;

    return true;
  }

};

}
#endif
