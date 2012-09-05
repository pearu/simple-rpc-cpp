
# Author: Pearu Peterson
# Created: August 2012

import re
from utils import tabulate, collect, joinlist, uniquestr, nextint
import templates



def isvector (typespec):
    return re.search(r'(\A|(?<![\w_]))vector\s*[<]', typespec) is not None

def vector_item_typespec(typespec):
    i = typespec.find('<')
    return typespec[i+1:-1].strip()

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
    if isscalar (typespec): return 'read_scalar', 'buffers_add_scalar'
    if isstring (typespec): return 'read_string', 'buffers_add_string'
    if isvector(typespec) and isscalar(vector_item_typespec(typespec)): 
        return 'read_vector', 'buffers_add_vector'
    return 'read_serial', 'buffers_add_serial'

def make_interface_source(server_name, namespace, (function_name, return_type, arguments, body)):
    srpc = uniquestr('srpc_')

    typedecl_args = joinlist(sep=', ')
    variables = joinlist(sep=', ')
    variable_declarations = joinlist(sep='\n')
    typespec_names = joinlist(sep=', ')
    recieve_arguments = joinlist(sep='\n         && ')
    send_arguments = 'true'
    buffers_add_arguments = joinlist(sep='\n        ')
    buffers_add_results = joinlist(sep='\n        ')
    recieve_results = joinlist(sep='\n              && ')

    for name, typespec in arguments:
        if name=='' and typespec=='void':
            continue
        typespec_names.append('%s %s' % (typespec, name))
        variables.append(name)
        variable_typespec = get_variable_typespec (typespec)

        variable_declarations.append('%s %s;' % (variable_typespec, name))
        read_mth, write_mth = get_socket_io_methods(typespec)
        buffers_add_arguments.extend((getattr (templates, write_mth) % (locals ())).split ('\n'))
        recieve_arguments.append('%(srpc)ssocket.%(read_mth)s(%(name)s, "%(name)s")' % (locals()))
        if isresult(typespec):
            recieve_results.append('%(srpc)ssocket.%(read_mth)s(%(name)s, "%(name)s")' % (locals()))
            buffers_add_results.extend((getattr(templates, write_mth) % (locals ())).split ('\n'))

    if return_type=='void':
        return_declaration = ''
        return_statement = 'return;'
        function_call = '%(function_name)s(%(variables)s);' % (locals ())
    else:
        name = '%(srpc)sreturn_value' % (locals ())
        return_declaration = '%(return_type)s %(srpc)sreturn_value;' % (locals())
        return_statement = 'return %(srpc)sreturn_value;' % (locals())
        function_call = '%(srpc)sreturn_value = %(function_name)s(%(variables)s);' % (locals ())
        read_mth, write_mth = get_socket_io_methods(return_type)
        recieve_results.append('%(srpc)ssocket.%(read_mth)s(%(srpc)sreturn_value, "return_value")' % (locals()))
        buffers_add_results.extend((getattr(templates, write_mth) % (locals ())).split ('\n'))

    if (buffers_add_arguments):
        buffers_add_arguments.insert(0, 'std::list< boost::asio::const_buffer > %(srpc)sbuffers;' %(locals ()))
        send_arguments = '%(srpc)ssocket.write_buffer_list(%(srpc)sbuffers, "%(function_name)s(%(variables)s)")' % (locals())


    if (buffers_add_results):
        buffers_add_results.insert(0, 'std::list< boost::asio::const_buffer > %(srpc)sbuffers;' %(locals ()))
        buffers_add_results.append ('%(srpc)sbuffers.push_back( boost::asio::buffer( &%(srpc)sconnection_magic, sizeof(%(srpc)sconnection_magic) ) );' % (locals()))
        send_results = ('%(srpc)ssocket.write_buffer_list(%(srpc)sbuffers, "%(function_name)s(%(variables)s)")' % (locals()))
    else:
        send_results = ('%(srpc)ssocket.write_scalar(%(srpc)sconnection_magic, "connection_magic", -1)' % (locals ()))

    if not recieve_results: recieve_results = 'true'
    if not recieve_arguments: recieve_arguments = 'true'

    function_prototype = '%(return_type)s %(namespace)s::%(function_name)s(%(typespec_names)s)' % locals()
    special_prototype = '  %(return_type)s %(function_name)s(%(typespec_names)s);' % locals()

    server_magic   = uniquestr(str2magic(server_name))
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
        special_prototype = special_prototype,
        )
