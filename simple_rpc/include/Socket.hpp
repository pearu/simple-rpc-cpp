
#ifndef SOCKET_HPP_DEFINED
#define SOCKET_HPP_DEFINED

#include <string>
#include <iostream>
#include <typeinfo> 
#include <boost/asio.hpp>


class Socket: public  boost::asio::ip::tcp::socket
{
private:
  int m_debug_level;
  std::string m_appname;

private:
  template <typename T> uint64_t size_bytes(const std::vector<T>& value) { return sizeof(T) * value.size(); } 
  uint64_t size_bytes(const std::string& value) { return sizeof(char)*value.size(); } 

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
  



  template <typename T> bool write_container(const T &value, const std::string & name = "")
  {
    uint32_t sz = value.size();
    if (!write_scalar(sz, name + ".size"))
      return false;
    boost::system::error_code error;
    size_t len = boost::asio::write(*this, boost::asio::buffer( value ), error);
    if (error)
      {
	std::cerr<<m_appname<<":write_container<"<<typeid(T).name()<<">("<<name<<") error on write: "<<error.message ()<<std::endl;
	return false;
      }
    if (len != size_bytes(value))
      {
	std::cerr<<m_appname<<":write_container<"<<typeid(T).name()<<">("<<name<<") expected to write "<<value.size()<<" bytes but wrote "<<len<<std::endl;
	return false;
      }
    if (m_debug_level>1)
      std::cout<<m_appname<<":write_container<"<<typeid(T).name()<<">("<<name<<") successfully wrote=["<<value.size()<<"]"<<std::endl;
    return true;
  }

  template <typename T> bool read_container(T &value, const std::string & name = "")
  {
    boost::system::error_code error;
    uint32_t sz = 0;
    if (!read_scalar(sz, name + ".size"))
      {
	return false;
      }
    value.resize(sz);
    size_t len = boost::asio::read( *this, boost::asio::buffer( value ), error);
    if (error)
      {
	std::cerr<<m_appname<<":read_scalar<"<<typeid(T).name()<<">("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != size_bytes(value))
    {
      std::cerr<<m_appname<<":read_scalar<"<<typeid(T).name()<<">("<<name<<") expected to read "<<size_bytes(value)<<" bytes but got "<<len<<std::endl;
      return false;
    }
    if (m_debug_level>1)
      std::cout<<m_appname<<":read_scalar<"<<typeid(T).name()<<"g>("<<name<<") successfully read "<<len<<" bytes"<<std::endl;

    return true;
  }

  bool read_string(std::string &value, const std::string & name = "")
  {
    boost::system::error_code error;
    uint32_t sz = 0;
    if (!read_scalar(sz, name + ".size"))
      {
	return false;
      }
    std::vector<char> data;
    data.resize(sz);
    size_t len = boost::asio::read( *this, boost::asio::buffer( data ), error);
    if (error)
      {
	std::cerr<<m_appname<<":read_scalar<string>("<<name<<") error="<<error.message ()<<std::endl;
	return false;
    }
    if (len != sz)
    {
      std::cerr<<m_appname<<":read_scalar<string>("<<name<<") expected to read "<<value.size()<<" bytes but got "<<len<<std::endl;
      return false;
    }
    copy( data.begin(), data.end(), back_inserter( value ) );
    if (m_debug_level>1)
      std::cout<<m_appname<<":read_scalar<string>("<<name<<") successfully read "<<len<<" bytes='"<<value<<"'"<<std::endl;

    return true;
  }

};

#endif
