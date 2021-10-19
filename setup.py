from setuptools import setup, Extension

setup(
    name="python-iconv",
    version="1.1.2",
    description="iconv-based Unicode converter",
    author="Bodo Graumann",
    author_email="mail@bodograumann.de",
    url="https://github.com/bodograumann/python-iconv",
    long_description="""This is a port of Martin v. Loewis’ original iconv package to Python 3.

The iconv module exposes the operating system's iconv character
conversion routine to Python. This package provides an iconv wrapper
as well as a Python codec to convert between Unicode objects and
all iconv-provided encodings.
""",
    py_modules=["iconvcodec"],
    ext_modules=[Extension("iconv", sources=["iconvmodule.c"])],
)
