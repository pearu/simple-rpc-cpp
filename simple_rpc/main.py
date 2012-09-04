
# Author: Pearu Peterson
# Created: August 2012

import argparse
import sys
import os
from collections import defaultdict
from parser import parse_prototypes
from utils import collect
from interface_generator import make_interface_source
import templates

def main():
    parser = argparse.ArgumentParser(description='Simple RPC code generator.')
    parser.add_argument("-n", "--name", help="name of the RPC server code",
                        type=str)
    parser.add_argument('filepath', type=str, nargs='+', 
                   help='path to C++ header files that are scanned for prototypes')
    parser.add_argument('--functions', type=str,
                        help='comma separated list of functions to be wrapped')
    args = parser.parse_args()
    prototypes = defaultdict(list)
    for filename in args.filepath:
        original_filename = os.path.basename(filename)
        prototypes[original_filename] += parse_prototypes(filename, args.functions)

    special_list = [
        ('set_debug_level', 'void', [('debug_level', 'const int &')], '%(srpc)sdebug_level = debug_level;'),
        ('get_counter', 'uint64_t', [('', 'void')], '%(srpc)sreturn_value = %(srpc)scounter;'),
        ]

    for original_filename, prototype_list in prototypes.iteritems():
        source_info = dict(FILENAME=os.path.basename(original_filename).upper().replace('.','_'),
                           original_filename=os.path.basename(original_filename),
                           namespace = os.path.splitext(os.path.basename(original_filename))[0],
                           )
        server_name = source_info['namespace']
        source_info['NAMESPACE'] = source_info['namespace'].upper()

        for prototype in special_list:
            interface_dict = make_interface_source(server_name, 'simple_rpc', prototype)
            collect(source_info, interface_dict)

        for prototype in prototype_list:
            interface_dict = make_interface_source(server_name, 'simple_rpc::' + source_info['namespace'], prototype)
            del interface_dict['special_prototype']
            collect(source_info, interface_dict)

        client_filename = os.path.splitext(original_filename)[0] + '-rpc.hpp'
        print 'creating file', client_filename
        f = open(client_filename, 'w')
        f.write(templates.client_header % (source_info))
        f.close()

        client_filename = os.path.splitext(original_filename)[0] + '-rpc.cpp'
        print 'creating file', client_filename
        f = open(client_filename, 'w')
        f.write(templates.client_source % (source_info))
        f.close()

        server_filename = os.path.splitext(original_filename)[0] + '-rpc-server.cpp'
        print 'creating file', server_filename
        f = open(server_filename, 'w')
        f.write(templates.server_source % (source_info))
        f.close()

if __name__=='__main__':
    main ()
