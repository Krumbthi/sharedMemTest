#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import sys
from distutils.core import setup, Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

compile_args = ['-std=c++17']

basic_module = Extension(
    "share", 
    sources=['share.pyx'], 
    extra_compile_args=compile_args,
    libraries=['rt']
)

setup(
    name='share',
    #cmdclass = {'build_ext': build_ext},
    ext_modules=cythonize(basic_module)
)