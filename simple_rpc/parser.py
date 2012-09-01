
# Author: Pearu Peterson
# Created: August 2012

import os
import sys
import re

re_prototype = re.compile(r'(?P<rtype>([\w_:<>]+|))\s+(?P<fname>[\w_:]+)\s*\((?P<args>[^)]*)\)\s*({|;)', re.I | re.S)
def parse_prototypes(filename, functions = None):
    """ Scan filename for C++ functions and prototypes.
    
    Parameters
    ----------
    filename : str
      File name of a C++ source or header file.

    Return
    ------
    prototypes : list
      A list of `(<function name>, <function return type spec>, <args>, <body>)` tuples
      where `<args>` is a list of `(<argument name>, <argument type spec>)` tuples.
      `<body>` is None.
    """
    f = open (filename, 'r')
    text = f.read ()
    f.close()
    prototypes = []
    print 'Creating RPC wrappers to functions:'
    for m in re_prototype.finditer(text):
        fname = m.group('fname')
        if functions is not None and fname not in functions:
            continue
        rtype = m.group('rtype')
        args = []
        for a in m.group ('args').split(','):
            aname = None
            for i,c in enumerate (reversed(a)):
                if not (c.isalnum () or c=='_'):
                    aname = a[-i:].strip()
                    atype = a[:-i].strip()
                    break
            if aname is None:
                aname = ''
                atype = a
            args.append((aname, atype))
        print '  ', m.group(0)[:-1].rstrip()
        prototypes.append ((fname, rtype, args, None))
    return prototypes

if __name__=='__main__':
    filename = sys.argv[1]
    print parse_prototypes(filename)
