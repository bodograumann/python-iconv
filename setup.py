from setuptools import setup, Extension
import sys

# On Linux, iconv is part of glibc and doesn't need separate linkage
# Otherwise, link against libiconv
if sys.platform.startswith('linux'):
    libraries = []
else:
    libraries = ["iconv"]

setup(
    ext_modules=[Extension("iconv", sources=["iconvmodule.c"], libraries=libraries)],
)
