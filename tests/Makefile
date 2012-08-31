
INCLUDE = -I../simple_rpc/include

all: test_std_scalars

all_apps : std_scalars_app rpc_std_scalars_app

std_scalars.hpp : std_scalars.cpp ../scripts/make_hpp 
	../scripts/make_hpp std_scalars.cpp
std_scalars_app : std_scalars.hpp std_scalars_app.cpp
	g++ std_scalars_app.cpp std_scalars.cpp -o std_scalars_app
rpc_std_scalars_app : std_scalars.hpp std_scalars_app.cpp
	simple_rpc std_scalars.hpp
	g++ $(INCLUDE) std_scalars_app.cpp -DUSE_SIMPLE_RPC -pthread -lboost_system -o rpc_std_scalars_app
	g++ $(INCLUDE) SimpleRPC_std_scalars_server.cpp std_scalars.cpp -pthread -lboost_system -o rpc_std_scalars_server_app

test_std_scalars: all_apps
	./rpc_std_scalars_server_app > /dev/null & # start RPC server
	@sleep 0.2
	./std_scalars_app                          # executes C/C++ functions directly
	./rpc_std_scalars_app                      # executes C/C++ functions via RPC server
	killall rpc_std_scalars_server_app         # stop RPC server

clean:
	rm -f *.o *_app