#include <iostream>
using namespace std;

#include "example_dot-rpc.hpp"
#ifdef SimpleRPC
using namespace simple_rpc::example_dot;
#endif

main()
{
  SIMPLE_RPC_CONNECT("127.0.0.1", 2340, 0);
  vector<double> a(3); a[0] = 1.2; a[1] = 3.4; a[2] = 5.6;
  cout << "dot_product(a,a) -> " << dot_product(a,a) << endl;
}
