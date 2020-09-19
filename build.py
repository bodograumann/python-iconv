"""Build C extension with poetry"""
from distutils.core import Extension

def build(setup_kwargs):
    setup_kwargs.update({
        'ext_modules': [
            Extension("iconv", sources=["iconvmodule.c"])
        ],
    })
