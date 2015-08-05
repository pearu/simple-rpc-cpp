This project initiated from the following practical problem. To control experimental equipment via computers, manufactures provide software drivers with SDK written in C/C++. Unfortunately, Windows platform is often the only supported platform or support for other platforms stays years behind. In order to control such equipment from a Linux platform, for instance, Remote Procedure Calling (RPC) techniques can be used.

_Simple RPC C++_ project provides a Python script that generates wrappers to C/C++ functions and RPC server applications so that the wrapped C/C++ functions could be called from an application (local host) but the C/C++ functions are executed on a server application (remote host).

The usage of word "simple" in the name of this project is due to the following:

  * _RPC technology can be simple to use_ --- editing existing code should be minimal in order to remotely call C/C++ functions. Just changing the name of a header file should be sufficient to adapt an application to use RPC for certain C/C++ functions. Note that existing RPC libraries require RPC specific client applications; the current project aims at requiring minimal modification to client applications so that switching from calling C/C++ functions directly or via RPC, would be straightforward.

  * _Simplification can be sufficient for practical applications_ --- C/C++ functions that can be wrapped for RPC, are assumed to have "simple" prototypes, that is, the arguments should have types that Boost serialization library can handle. This includes all standard C/C++ scalar types and standard STL collections. These types can be defined in arguments as is, or as references, or as pointers. Notice that pointer arguments are treated in application program (in local host) as scalars that can be passed to RPC server program where they point to actual memory location of the remote host.

  * _Simplicity goes with restrictions_ --- For instance, wrapping C++ template functions is not supported. In addition, when running an application and RPC server on hosts with different architecture or operating system, special care must be taken to ensure that the data exchange between local and remote host is correct. For instance, the size of standard C/C++ `int` type may be different on local and remote hosts leading to possible corruption of data. To avoid this, always use scalar types with fixed byte width, for instance, `int32_t`, `uint64_t`, etc. Finally, no care is taken when the endian of local and remote hosts differ..

# Installation #

The project assumes availability of Python 2.x. Python 3.x support might require minor modifications in the project source code, patches are welcome.

Checkout the project source code, see [Source/Checkout](https://code.google.com/p/simple-rpc-cpp/source/checkout) for instructions. In the source code directory, run
```
sudo python setup.py install
```
Windows users should run `python setup.py install` from command prompt.


To verify success, execute
```
  cd tests
  make
```
If the tests pass, you can try out the "Example" project below.

# Example #

A typical C/C++ project consists of three parts: application source file containing the `main` function, source file(s) of computational functions, and header file(s) of the corresponding prototypes.
All source files are compiled and linked together resulting an application program.
When running this application program, the `main` function calls computational functions
and outputs the results. Our aim is that when `main` function calls computational functions then they are actually executed in remote host. For that we use RPC technique to send function arguments and then receive function results over network. The current project _Simple RPC C++_ provides a Python script `simple_rpc` that constructs RPC wrapper functions to computational functions and generates the corresponding RPC source code. By design, modifications to existing source files are minimal.
In fact, in a typical usage case only the application source file requires minor editing while no modifications are needed to the rest of source or header files, as will be demonstrated below.

To illustrate this, consider the following example project consisting of three files:
<table border='1'>
<tr>
<th>Source file: example_dot.cpp</th>
<th>Header file: example_dot.hpp</th>
<th>Application source file: example_dot_app.cpp</th>
</tr>
<tr>
<td>
<pre><code>#include "example_dot.hpp"<br>
<br>
double dot_product(const vector&lt;double&gt; &amp; a,<br>
		   const vector&lt;double&gt; &amp; b<br>
		   )<br>
{<br>
  double sum = 0;<br>
  for (int i = 0; i &lt; a.size(); i++)<br>
    sum += a[i] * b[i];<br>
  return sum;<br>
}<br>
</code></pre>
</td>
<td>
<pre><code>#ifndef EXAMPLE_DOT_HPP_DEFINED<br>
#define EXAMPLE_DOT_HPP_DEFINED<br>
<br>
#include &lt;vector&gt;<br>
using namespace std;<br>
<br>
double dot_product(const vector&lt;double&gt; &amp; a,<br>
		   const vector&lt;double&gt; &amp; b<br>
		   );<br>
<br>
#endif<br>
</code></pre>
</td>
<td>
<pre><code>#include &lt;iostream&gt;<br>
<br>
#include "example_dot.hpp"<br>
<br>
main()<br>
{<br>
  vector&lt;double&gt; a(3);<br>
  a[0] = 1.2; a[1] = 3.4; a[2] = 5.6;<br>
  cout &lt;&lt; "dot_product(a,a) -&gt; ";<br>
  cout &lt;&lt; dot_product(a,a) &lt;&lt; endl;<br>
}<br>
</code></pre>
</td>
</tr>
</table>
The corresponding application can be compiled and executed:
```
$ c++ example_dot.cpp example_dot_app.cpp -o example_dot_app
$ ./example_dot_app
dot_product(a,a) -> 44.36
```

In order to call `dot_product` via RPC server, first, we generate wrapper codes:
```
$ simple_rpc example_dot.hpp
Creating RPC wrappers to functions:
    double dot_product(const vector<double> & a,
		       const vector<double> & b
		      )
creating file example_dot-rpc.hpp
creating file example_dot-rpc.cpp
creating file example_dot-rpc-server.cpp
```
Notice that the `simple_rpc` script takes header files for input and generates
three files as shown above. These files will be used to compile and build two
executable programs: one for application and one for RPC server.

Next, we will modify the application source code as follows.
<table border='1'>
<tr>
<th>Source file: example_dot.cpp</th>
<th>Header file: example_dot.hpp</th>
<th>Application source file: example_dot_app.cpp</th>
</tr>
<tr>
<td>
<pre><code>#include "example_dot.hpp"<br>
<br>
double dot_product(const vector&lt;double&gt; &amp; a,<br>
		   const vector&lt;double&gt; &amp; b<br>
		   )<br>
{<br>
  double sum = 0;<br>
  for (int i = 0; i &lt; a.size(); i++)<br>
    sum += a[i] * b[i];<br>
  return sum;<br>
}<br>
</code></pre>
</td>
<td>
<pre><code>#ifndef EXAMPLE_DOT_HPP_DEFINED<br>
#define EXAMPLE_DOT_HPP_DEFINED<br>
<br>
#include &lt;vector&gt;<br>
using namespace std;<br>
<br>
double dot_product(const vector&lt;double&gt; &amp; a,<br>
		   const vector&lt;double&gt; &amp; b<br>
		   );<br>
<br>
#endif<br>
</code></pre>
</td>
<td>
<pre><code>#include &lt;iostream&gt;<br>
<br>
#include "example_dot-rpc.hpp"              // &lt;-- (1)<br>
<br>
#ifdef SimpleRPC                            // &lt;-- (2)<br>
using namespace simple_rpc::example_dot;    // &lt;-- (2)<br>
#endif                                      // &lt;-- (2)<br>
<br>
main()<br>
{<br>
  SIMPLE_RPC_CONNECT("127.0.0.1", 2340, 2); // &lt;-- (3)<br>
  vector&lt;double&gt; a(3);<br>
  a[0] = 1.2; a[1] = 3.4; a[2] = 5.6;<br>
  cout &lt;&lt; "dot_product(a,a) -&gt; ";<br>
  cout &lt;&lt; dot_product(a,a) &lt;&lt; endl;<br>
}<br>
</code></pre>
</td>
</tr>
</table>
The application source code is modified in three places indicated with `// <-- (#)`:
  1. The name of the header file is appended with `-rpc` suffix. The generated header file contains RPC wrapper functions to functions found in the original header file.
  1. `ifdef SimpleRPC` block is inserted. This is done for convenience as it will make easy to disable (use `-DDISABLE_SIMPLE_RPC` when compiling application code) and enable RPC in the application code. Following `using namespace` declaration exposes the RPC wrapper of `compute_dot` function to current namespace. In general, RPC wrappers are defined in namespace `simple_rpc::<headerfile name>`.
  1. `SIMPLE_RPC_CONNECT` macro is used to specify the RPC server host IP, port number and debug level (0 means no debug messages are shown, increasing this number will increase verbosity). Here we use debug level 2 in order to illustrate the connection between the application code and RPC server, see below.

Next,  the application and the RPC server programs must be built. In the given example
we use RPC server local host (the corresponding host IP is 127.0.0.1) but, in general,
the application program must be built on local host while the RPC server program on
server host, especially, if these hosts run different operating systems.
The following table illustrates the build process:
<table border='1'>
<tr>
<th>Remote host</th>
<th>Local host</th>
</tr>
<tr>
<td>
<pre><code>$ c++ example_dot.cpp example_dot-rpc-server.cpp \<br>
   -o example_dot-rpc-server -pthread \<br>
   -lboost_system -lboost_serialization \<br>
   -I`simple_rpc --include-dir`<br>
</code></pre>
</td>
<td>
<pre><code>$ c++ example_dot-rpc.cpp example_dot_app.cpp \<br>
   -o example_dot_app-rpc -pthread \<br>
   -lboost_system -lboost_serialization \<br>
   -I`simple_rpc --include-dir`<br>
</code></pre>
</td>
</tr>
</table>
Notice that all source codes of functions must be compiled on remote host while the application source code with RPC wrapper source is compiled on local host.

Finally, we run the RPC server in remote host, and subsequently, run the application program:
<table border='1'>
<tr>
<th>Remote host</th>
<th>Local host</th>
</tr>
<tr>
<td>
<pre><code>$ ./example_dot-rpc-server<br>
rpc-server[2] waits connection via port 2340...connected!<br>
rpc-server:read_scalar&lt;j&gt;(a.size) &lt;- 4 bytes<br>
rpc-server:read_vector&lt;d&gt;(a) &lt;- 24 bytes<br>
rpc-server:read_scalar&lt;j&gt;(b.size) &lt;- 4 bytes<br>
rpc-server:read_vector&lt;d&gt;(b) &lt;- 24 bytes<br>
rpc-server:write_buffer_list(dot_product(a, b)) -&gt; 16 bytes<br>
rpc-server[3] waits connection via port 2340...<br>
</code></pre>
</td>
<td>
<pre><code>$ ./example_dot_app-rpc<br>
set_debug_level:write_buffer_list(set_debug_level(debug_level)) -&gt; 4 bytes<br>
dot_product:write_buffer_list(dot_product(a, b)) -&gt; 56 bytes<br>
dot_product:read_scalar&lt;d&gt;(return_value) &lt;- 8 bytes<br>
dot_product(a,a) -&gt; 44.36<br>
</code></pre>
</td>
</tr>
</table>

Notice that RPC server can run continuously and different application programs can
execute functions from the server. This will work only when different application
programs will not execute the server functions at the same time. Server will serve the first application and during the time of execution, connections to the server by other applications will be declined.
