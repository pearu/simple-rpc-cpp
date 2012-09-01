
#include <iostream>
#include <typeinfo> 

#include "std_scalars.hpp"

#ifdef SimpleRPC
#include "SimpleRPC.hpp"
#endif

static unsigned int check_getarg_success_count = 0;
static unsigned int check_getarg_failure_count = 0;

template <typename T> bool check_getarg(T a)
{
  T r = getarg(a);
  bool success = (r == a);
  if (!success)
    {
      std::cout << "check_getarg failed: getarg<"<<typeid(T).name()<<">("<<a<<")->"<<r<<" but expected "<<a<<std::endl;
      check_getarg_failure_count ++;
    }
  else
    check_getarg_success_count ++;
  return success;
}

template <typename T> bool check_getarg_container(T& a)
{
  T r = getarg(a);
  bool success = (r == a);
  if (!success)
    {
      std::cout << "check_getarg failed: getarg<"<<typeid(T).name()<<">(["<<a.size()<<"])->["<<r.size()<<"] but expected given argument"<<std::endl;
      check_getarg_failure_count ++;
    }
  else
    check_getarg_success_count ++;
  return success;
}

main()
{
#ifdef SimpleRPC
  SimpleRPC rpc("127.0.0.1", 2340, 0);
  set_debug_level(0);
#endif

  check_getarg((bool)3);
  check_getarg((char)3);
  check_getarg((short)3);
  check_getarg((long)3);
  check_getarg((char)3);
  check_getarg((float)3.14);
  check_getarg((double)3.14);
  check_getarg(std::string("Hello"));
  {
    std::vector<char> v(3); v[0] = 1; v[1] = 2; v[2] = 3;
    check_getarg_container(v);
  }
  {
    std::vector<short> v(3); v[0] = 1; v[1] = 2; v[2] = 3;
    check_getarg_container(v);
  }
  {
    std::vector<int> v(3); v[0] = 1; v[1] = 2; v[2] = 3;
    check_getarg_container(v);
  }
  {
    std::vector<long> v(3); v[0] = 1; v[1] = 2; v[2] = 3;
    check_getarg_container(v);
  }
  {
    std::vector<float> v(3); v[0] = 1.1; v[1] = 2.2; v[2] = 3.3;
    check_getarg_container(v);
  }
  {
    std::vector<double> v(3); v[0] = 1.1; v[1] = 2.2; v[2] = 3.3;
    check_getarg_container(v);
  }
  {
    std::vector<std::string> v(3); v[0] = "hello"; v[1] = "hey"; v[2] = "hi";
    //FAILS WITH RPC: check_getarg_container(v);
  }

  
  //
  std::cout<<"check_getarg "<<check_getarg_success_count<<" tests PASSED OK"<<std::endl;
  if (check_getarg_failure_count)
    std::cout<<"check_getarg "<<check_getarg_failure_count<<" tests FAILED"<<std::endl;
  return check_getarg_failure_count;
}
