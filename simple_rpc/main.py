
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
        target_filename, ext = os.path.splitext(original_filename)
        target_filename = 'SimpleRPC_' + original_filename
        prototypes[original_filename, target_filename] += parse_prototypes(filename, args.functions)

    for (original_filename, target_filename), prototype_list in prototypes.iteritems():
        source_info = dict(FILENAME=os.path.basename(target_filename).upper().replace('.','_'),
                           original_filename=os.path.basename(original_filename),
                           )

        for prototype in prototype_list:
            code_name = os.path.splitext(os.path.basename(args.filepath[0]))[0]
            interface_dict = make_interface_source(code_name, prototype)
            collect(source_info, interface_dict)
        print 'creating file', target_filename
        f = open(target_filename, 'w')
        f.write(templates.client_header % (source_info))
        f.close()

        server_filename = os.path.splitext(target_filename)[0] + '_server.cpp'
        print 'creating file', server_filename
        f = open(server_filename, 'w')
        f.write(templates.server_source % (source_info))
        f.close()

if __name__=='__main__':
    main ()
