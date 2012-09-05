
INCLUDE = -I`simple_rpc --include-dir`
RPC_BUILD_OPTS = -pthread -lboost_system -lboost_serialization

all: tests
tests: test_std_scalars test_stdlib

stdlib-rpc.hpp : ../simple_rpc/include/stdlib.hpp
	simple_rpc ../simple_rpc/include/stdlib.hpp

stdlib-rpc.cpp : ../simple_rpc/include/stdlib.hpp
	simple_rpc ../simple_rpc/include/stdlib.hpp
stdlib-rpc-server.cpp : ../simple_rpc/include/stdlib.hpp
	simple_rpc ../simple_rpc/include/stdlib.hpp
stdlib_app : stdlib_app.cpp stdlib-rpc.hpp
	g++ $(INCLUDE) stdlib_app.cpp -o stdlib_app -DDISABLE_SIMPLE_RPC

stdlib_app-rpc : stdlib-rpc.cpp stdlib_app.cpp stdlib-rpc.hpp
	g++ $(INCLUDE) stdlib_app.cpp stdlib-rpc.cpp -o stdlib_app-rpc $(RPC_BUILD_OPTS)

stdlib_app-rpc-server : stdlib-rpc-server.cpp ../simple_rpc/include/stdlib.cpp
	g++ $(INCLUDE) stdlib-rpc-server.cpp ../simple_rpc/include/stdlib.cpp -o stdlib_app-rpc-server $(RPC_BUILD_OPTS)

test_stdlib : stdlib_app stdlib_app-rpc stdlib_app-rpc-server
	./stdlib_app
	killall ./stdlib_app-rpc-server || exit 0
	./stdlib_app-rpc-server &
	@sleep 0.2
	./stdlib_app-rpc
	killall ./stdlib_app-rpc-server || exit 0

std_scalars.hpp : std_scalars.cpp ../scripts/make_hpp 
	../scripts/make_hpp std_scalars.cpp

std_scalars-rpc.hpp : std_scalars.hpp
	simple_rpc std_scalars.hpp
std_scalars-rpc.cpp  : std_scalars.hpp
	simple_rpc std_scalars.hpp
std_scalars-rpc-server.cpp  : std_scalars.hpp
	simple_rpc std_scalars.hpp

std_scalars_app : std_scalars.hpp std_scalars_app.cpp std_scalars-rpc.hpp
	g++ std_scalars_app.cpp std_scalars.cpp -o std_scalars_app -DDISABLE_SIMPLE_RPC


std_scalars_app-rpc : std_scalars-rpc.cpp std_scalars_app.cpp
	g++ -g $(INCLUDE) -DSimpleRPC=SimpleRPC_std_scalars std_scalars_app.cpp std_scalars-rpc.cpp  -pthread -lboost_system -o std_scalars_app-rpc -lboost_serialization

std_scalars_app-rpc-server : std_scalars-rpc-server.cpp std_scalars.cpp
	g++ -g $(INCLUDE) std_scalars-rpc-server.cpp std_scalars.cpp -pthread -lboost_system -o std_scalars_app-rpc-server -lboost_serialization

test_std_scalars: std_scalars_app std_scalars_app-rpc std_scalars_app-rpc-server
	./std_scalars_app                          # executes C/C++ functions directly
	killall ./std_scalars_app-rpc-server || exit 0       # stop RPC server
	./std_scalars_app-rpc-server  & # start RPC server
	@sleep 0.2
	./std_scalars_app-rpc                      # executes C/C++ functions via RPC server
	killall ./std_scalars_app-rpc-server || exit 0       # stop RPC server

example_dot_app : example_dot.hpp example_dot.cpp example_dot_app.cpp
	g++ example_dot.cpp example_dot_app.cpp -o example_dot_app -DDISABLE_SIMPLE_RPC


example_dot-rpc.cpp example_dot-rpc.hpp example_dot-rpc-server.cpp : example_dot.hpp
	simple_rpc example_dot.hpp

example_dot-rpc example_dot-rpc-server : example_dot-rpc.cpp example_dot_app.cpp
	g++ example_dot-rpc.cpp example_dot_app.cpp -o example_dot_app-rpc $(INCLUDE) $(RPC_BUILD_OPTS)
	g++ example_dot.cpp example_dot-rpc-server.cpp -o example_dot-rpc-server $(INCLUDE) $(RPC_BUILD_OPTS)

test_example_dot : example_dot-rpc example_dot-rpc-server example_dot_app
	killall ./example_dot-rpc-server || exit 0
	./example_dot-rpc-server &
	sleep 0.2
	./example_dot_app-rpc
	killall ./example_dot-rpc-server || exit 0

clean:
	rm -fv *.o *_app *_app-rpc* *-rpc*.cpp *-rpc*.hpp