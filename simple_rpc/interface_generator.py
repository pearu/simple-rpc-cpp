
# Author: Pearu Peterson
# Created: August 2012

import re
from utils import tabulate, collect, joinlist, uniquestr, nextint
import templates

def isvector (typespec):
    return re.search(r'(\A|(?<![\w_]))vector\s*[<]', typespec) is not None

def iscontainer(typespec):
    return re.search(r'(\A|(?<![\w_]))(vector|deque|list|stack|queue|priority_queue|set|multiset|map|multimap|bitset|array|unordered_(map|multimap|set|multiset))\s*[<]', typespec) is not None

def isstring (typespec):
    if iscontainer(typespec): return False
    return re.search(r'(\A|(?<![\w_]))string(\Z|(?![\w_]))', typespec) is not None

def isscalar(typespec):
    return not (iscontainer(typespec) or isstring(typespec))

def isresult(typespec):
    if typespec.startswith('const '):
        return False
    return typespec.endswith('&')
    if isscalar(typespec):
        return typespec.endswith('&')
    raise NotImplementedError (`typespec`)

def str2magic(s, _cache={}):
    magic = hash(s) & 0xffffffff
    if magic in _cache:
        if s==_cache[magic]:
            return magic
        while magic in _cache:
            magic = (magic + 1) & 0xffffffff
    _cache[magic] = s
    return magic

def get_variable_typespec (typespec):
    if typespec.endswith('&'):
        variable_typespec = typespec[:-1].rstrip()            
    else:
        variable_typespec = typespec
    if typespec.startswith ('const '):
        variable_typespec = variable_typespec[6:].lstrip()
    return variable_typespec

def get_socket_io_methods(typespec):
    if isscalar (typespec): return 'read_scalar', 'write_scalar'
    if isstring (typespec): return 'read_string', 'write_string'
    #if isstring (typespec): return 'read_string', 'write_container'
    return 'read_serial', 'write_serial'
    #return 'read_container', 'write_container'

def make_interface_source(code_name, (function_name, return_type, arguments, body)):
    srpc = uniquestr('srpc_')

    typedecl_args = joinlist(sep=', ')
    variables = joinlist(sep=', ')
    variable_declarations = joinlist(sep='\n')
    typespec_names = joinlist(sep=', ')
    recieve_arguments = joinlist(['true'], sep='\n         && ')
    send_results = joinlist(['true'],      sep='\n           && ')
    send_arguments = joinlist(['true'],  sep='\n            && ')
    recieve_results = joinlist(['true'], sep='\n              && ')


    for name, typespec in arguments:
        typespec_names.append('%s %s' % (typespec, name))
        variables.append(name)
        variable_typespec = get_variable_typespec (typespec)

        variable_declarations.append('%s %s;' % (variable_typespec, name))
        read_mth, write_mth = get_socket_io_methods(typespec)
        
        send_arguments.append('%(srpc)ssocket.%(write_mth)s(%(name)s, "%(name)s")' % (locals()))
        recieve_arguments.append('%(srpc)ssocket.%(read_mth)s(%(name)s, "%(name)s")' % (locals()))
        #if not isscalar (typespec):
        #    pass
        if isresult(typespec):
            recieve_results.append('%(srpc)ssocket.%(read_mth)s(%(name)s, "%(name)s")' % (locals()))
            send_results.append('%(srpc)ssocket.%(write_mth)s(%(name)s, "%(name)s")' % (locals()))

    if return_type=='void':
        return_declaration = ''
        return_statement = 'return;'
        function_call = '%(function_name)s(%(variables)s);' % (locals ())
    else:
        return_declaration = '%(return_type)s %(srpc)sreturn_value;' % (locals())
        return_statement = 'return %(srpc)sreturn_value;' % (locals())
        function_call = '%(srpc)sreturn_value = %(function_name)s(%(variables)s);' % (locals ())
        read_mth, write_mth = get_socket_io_methods(return_type)
        recieve_results.append('%(srpc)ssocket.%(read_mth)s(%(srpc)sreturn_value, "return_value")' % (locals()))
        send_results.append('%(srpc)ssocket.%(write_mth)s(%(srpc)sreturn_value, "return_value")' % (locals()))

    function_prototype = '%(return_type)s %(function_name)s(%(typespec_names)s)' % locals()

    server_magic   = uniquestr(str2magic(code_name))
    function_magic = str2magic(function_prototype)
    if body is not None:
        function_call = body % (locals())
    server_switch_case = templates.server_switch_case % (locals ())

    return dict(
        srpc = srpc, # manglin prefix
        server_magic = server_magic,
        wrapper_function_prototype = function_prototype,
        function_implementation = templates.function_implementation % (locals()),
        server_switch_case = tabulate(server_switch_case, tabs=10),
        )
