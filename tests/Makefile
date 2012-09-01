
INCLUDE = -I../simple_rpc/include

all: tests
tests: test_std_scalars

all_apps : std_scalars_app std_scalars_app-rpc std_scalars_app-rpc-server

std_scalars.hpp : std_scalars.cpp ../scripts/make_hpp 
	../scripts/make_hpp std_scalars.cpp

std_scalars-rpc.cpp  : std_scalars.hpp
	simple_rpc std_scalars.hpp
std_scalars-rpc-server.cpp  : std_scalars.hpp
	simple_rpc std_scalars.hpp

std_scalars_app : std_scalars.hpp std_scalars_app.cpp
	g++ std_scalars_app.cpp std_scalars.cpp -o std_scalars_app


std_scalars_app-rpc : std_scalars-rpc.cpp std_scalars_app.cpp
	g++ -g $(INCLUDE) -DSimpleRPC=SimpleRPC_std_scalars std_scalars_app.cpp std_scalars-rpc.cpp  -pthread -lboost_system -o std_scalars_app-rpc

std_scalars_app-rpc-server : std_scalars-rpc-server.cpp std_scalars.cpp
	g++ -g $(INCLUDE) std_scalars-rpc-server.cpp std_scalars.cpp -pthread -lboost_system -o std_scalars_app-rpc-server

test_std_scalars: all_apps
	./std_scalars_app                          # executes C/C++ functions directly
	killall std_scalars_app-rpc-server || exit 0       # stop RPC server
	./std_scalars_app-rpc-server  & # start RPC server
	@sleep 0.2
	./std_scalars_app-rpc                      # executes C/C++ functions via RPC server
	killall std_scalars_app-rpc-server || exit 0       # stop RPC server

clean:
	rm -fv *.o *_app *_app-rpc* *-rpc*.cpp