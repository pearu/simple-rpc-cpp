
# Author: Pearu Peterson
# Created: August 2012

def tabulate(string, tabs=0):
    ''' Helper function to prepend tabulation to source string'''
    if isinstance (tabs, int):
        tabs = ' '*tabs
    elif isinstance (tabs, str):
        pass
    else:
        raise TypeError ('second argument must be str|int, got %s' % (type(tabs)))
    lines = []
    for line in string.splitlines ():
        lines.append (tabs + line)
    return '\n'.join (lines)

def collect(target, source):
    ''' Helper function to append source dict to target dict '''
    for source_key, value in source.iteritems ():
        target_key = source_key + 's'
        if isinstance(value, list):
            if target_key in target:
                assert type (target[target_key])==type (value),`type (target[target_key]),type (value)`
                target[target_key].extend(value)
            else:
                target[target_key] = value
        elif isinstance (value, (uniquestr, int)):
            if source_key in target:
                assert target[source_key] == value,`target[source_key], value`
            else:
                target[source_key] = value
        elif isinstance (value, str):
            if target_key in target:
                target[target_key] += '\n' + value
            else:
                target[target_key] = value
        else:
            raise NotImplementedError (`value`)

class joinlist(list):
    def __init__ (self, *args, **kws):
        sep = kws.pop ('sep', '\n')
        list.__init__(self, *args, **kws)
        self.sep = sep
    def __str__(self):
        return self.sep.join (map (str, self))

class uniquestr(str): pass

def nextint(_cache=[0]):
    _cache[0] += 1
    return _cache[0]
