# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:46:18 2017

@author: zynda
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("project2.pyx"),
)