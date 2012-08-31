
# Author: Pearu Peterson
# Created: August 2012

import re
from utils import tabulate, collect, joinlist, uniquestr, nextint
import templates

def isvector (typespec):
    return re.search(r'vector\s*[<]', typespec) is not None

def isscalar(typespec):
    return not (isvector(typespec))

def isresult(typespec):
    if typespec.startswith('const '):
        return False
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


def make_interface_source(code_name, (function_name, return_type, arguments)):
    srpc = uniquestr('srpc_')
    CodeName = uniquestr(code_name.title().replace('_','').replace('.','_'))

    typedecl_args = joinlist(sep=', ')
    variables = joinlist(sep=', ')
    variable_declarations = joinlist(sep='\n')
    typespec_names = joinlist(sep=', ')
    recieve_arguments = joinlist(['true'], sep='\n         && ')
    send_results = joinlist(['true'],      sep='\n           && ')
    send_arguments = joinlist(['true'],  sep='\n            && ')
    recieve_results = joinlist(['true'], sep='\n              && ')

    print '  generating interface data for', function_name,'...'

    for name, typespec in arguments:
        typespec_names.append('%s %s' % (typespec, name))
        variables.append(name)
        if typespec.endswith('&'):
            variable_typespec = typespec[:-1].rstrip()            
        else:
            variable_typespec = typespec
        if typespec.startswith ('const '):
            variable_typespec = variable_typespec[6:].lstrip()

        variable_declarations.append('%s %s;' % (variable_typespec, name))
        if isscalar(typespec):
            send_arguments.append('%(srpc)ssocket.write_scalar(%(name)s, "%(name)s")' % (locals()))
            recieve_arguments.append('%(srpc)ssocket.read_scalar(%(name)s, "%(name)s")' % (locals()))
            if isresult(typespec):
                recieve_results.append('%(srpc)ssocket.read_scalar(%(name)s, "%(name)s")' % (locals()))
                send_results.append('%(srpc)ssocket.write_scalar(%(name)s, "%(name)s")' % (locals()))
        else:
            raise NotImplementedError (`typespec`)

    if return_type=='void':
        return_declaration = ''
        return_statement = 'return;'
        function_call = '%(function_name)s(%(variables)s);' % (locals ())
    else:
        return_declaration = '%(return_type)s %(srpc)sreturn_value;' % (locals())
        return_statement = 'return %(srpc)sreturn_value;' % (locals())
        function_call = '%(srpc)sreturn_value = %(function_name)s(%(variables)s);' % (locals ())
        if isscalar(return_type):
            
            recieve_results.append('%(srpc)ssocket.read_scalar(%(srpc)sreturn_value, "return_value")' % (locals()))
            send_results.append('%(srpc)ssocket.write_scalar(%(srpc)sreturn_value, "return_value")' % (locals()))
        else:
            raise NotImplementedError (`return_type`)
    function_prototype = '%(return_type)s %(function_name)s(%(typespec_names)s)' % locals()

    server_magic   = uniquestr(str2magic(code_name))
    function_magic = str2magic(function_prototype)
    server_switch_case = templates.server_switch_case % (locals ())


    return dict(
        srpc = srpc, # manglin prefix
        CodeName = CodeName,
        server_magic = server_magic,
        wrapper_function_prototype = function_prototype,
        function_method = templates.function_method % (locals()),
        redefine_original_function = '#define %s SimpleRPC_ORIGINAL_%s' % (function_name, function_name),
        define_wrapper_function = '#define %s SimpleRPC_%s::%s' % (function_name, CodeName, function_name),
        undefine_original_function = '#undef %s' % (function_name),
        server_switch_case = tabulate(server_switch_case, tabs=10),
        )
