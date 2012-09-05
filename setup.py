#!/usr/bin/env python

from glob import glob
import os
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

def getfile():
    try:
        return __file__
    except NameError:
        import inspect
        return inspect.getsourcefile(getfile)
setup_dir = os.path.dirname(getfile())
print setup_dir
from numpy.distutils.core import setup

setup(name='simple_rpc',
      version='0.1',
      description='Simple RPC C++ --- a simple RPC wrapper generator to C/C++ functions',
      author='Pearu Peterson',
      author_email='pearu.peterson@gmail.com',
      url='http://code.google.com/p/simple-rpc-cpp/',
      packages=['simple_rpc'],
      scripts = [os.path.join(setup_dir, 'scripts/simple_rpc')],
      data_files=[('simple_rpc/include', glob(os.path.join(setup_dir,'simple_rpc','include','*.hpp')))]
     )
