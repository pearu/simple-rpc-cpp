
#include <iostream>
#include <typeinfo> 

#define SIMPLE_RPC_MAIN
#include "SimpleRPC_std_scalars.hpp"

//#include "std_scalars.hpp"

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

main()
{
  SIMPLE_RPC_StdScalars(rpc, "127.0.0.1", 2340);
  check_getarg((bool)3);
  check_getarg((char)3);
  check_getarg((short)3);
  check_getarg((long)3);
  check_getarg((char)3);
  check_getarg((float)3.14);
  check_getarg((double)3.14);
  std::cout<<"check_getarg "<<check_getarg_success_count<<" tests PASSED OK"<<std::endl;
  if (check_getarg_failure_count)
    std::cout<<"check_getarg "<<check_getarg_failure_count<<" tests FAILED"<<std::endl;
  return check_getarg_failure_count;
}
