
# Author: Pearu Peterson
# Created: August 2012

import os
import sys
import re

re_prototype = re.compile(r'(?P<rtype>([\w_:<>*\s]+|))\s+(?P<fname>[\w_:]+)\s*\(\s*(?P<args>[^)]*)\s*\)\s*({|;)', re.I | re.S)

re_namespace = re.compile(r'namespace\s+(?P<namespace>\w+)\s*{(?P<content>.*)}', re.I | re.S)

def parse_string (text, namespace = [], functions=None):
    prototypes = []
    for m in re_namespace.finditer(text):
        prototypes += parse_string(m.group('content'),
                                   namespace = namespace + [m.group('namespace')],
                                   functions = functions)
        text = text[:m.start()] + text[m.end()]
    for m in re_prototype.finditer(text):
        fname = m.group('fname')
        if functions is not None and fname not in functions:
            continue
        rtype = m.group('rtype').strip()
        args = []
        names = []
        for a in m.group ('args').split(','):
            a = a.strip()
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
            names.append(aname)
        ns = '::'.join (namespace)
        print '  ', ns, m.group(0)[:-1].strip()#, (fname, rtype, args, None)

        if ns.startswith('simple_rpc::'):
            if rtype=='void':
                body = '%s(%s);' % (fname, ', '.join (names))
            else:
                body = '%%(srpc)sreturn_value = %s(%s);' % (fname, ', '.join (names))
            fname = ns + '::' + fname
            prototypes.append ((fname, rtype, args, body))
        else:
            prototypes.append ((fname, rtype, args, None))
    return prototypes

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
    text = ''
    f = open (filename, 'r')
    for line in f.readlines ():
        i = line.find('//')
        if i!=-1:
            line = line[:i] + '\n'
        if line.startswith ('#'):
            continue
        text += line
    f.close()
    
    # TODO: get rid of /*..*/ comment blocks
    print 'Creating RPC wrappers to functions:'
    return parse_string(text, [], functions = functions)

if __name__=='__main__':
    filename = sys.argv[1]
    print parse_prototypes(filename)
