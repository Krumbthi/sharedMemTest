from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("share.pyx")
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from distutils.core import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

#compile_args = ['-std=c++17', '-DLOGGING']
compile_args = ['-std=c++17']

basic_module = Extension("pyltc2983",
        sources=['pyltc2983.pyx', 'LTC2983.cpp', 'spi.cpp', 'logger.cpp'],
        extra_compile_args=compile_args,
        language="c++")

setup(
    name='pyltc2983',
    #cmdclass = {'build_ext': build_ext},
    ext_modules=cythonize(basic_module)
)