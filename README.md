Iconv-based codec library for Python
====================================
Written by Martin v. Loewis<br>
Ported to Python 3 by Bodo Graumann

This package provides a set of codecs to Python based on the
underlying iconv library of the operating system, as available on
glibc 2, Solaris, or other Unix variants. It consists of two modules:
`iconv` and `iconvcodec`.
For common usage the codec interface is more convenient and should be preferred.

Installation
------------
To install the module use

    pip install python-iconv

This module package requires atleast Python 3.6.

Module iconv
------------
The iconv module exposes a global function to create iconv objects:

    open(tocode, fromcode)

Return descriptor for character set conversion. If the conversion
of fromcode to tocode is not known to the system, a ValueError is
raised.

Iconv objects provide a single method to convert a string

    iconv(in[, outlen[, count_only]])

Return the string resulting from the conversion of `in`. The parameter
`in` must be a byte string.
It is the caller's responsibility to guarantee that the internal
representation of the `in` object indeed uses fromcode of the `Iconv`
object. The parameter `outlen` represents an estimate of the resulting
string size in bytes.
If the buffer is to small, an exception is thrown. If `count_only` is set,
no conversion is attempted, but the number of necessary bytes is
returned.

In case of an error, the `iconv` method raises the exception `iconv.error`.
This exception has four arguments:

- the error string as returned from strerror
- the error number
- the number of input bytes processed
- the output string produced so far

Module iconvcodecs
------------------
This module encapsulates the iconv module into a set of codecs. To use it,
simply import it. As a result, the C library's codecs will be available:

```python
b"Hello".decode("T.61")
"World".encode("JOHAB")
```

Contributing
------------

Contributions are always welcome.
Setting up a local dev environment is as simple as:

```sh
python -m venv env
source env/bin/activate
pip install -e .
python -m unittest
```

Code should be auto-formatted with [black](https://black.readthedocs.io/en/stable/).
```python
pip install black
black *.py
```

Publishing
----------

We currently only publish source distributions.
```sh
pip install twine
python setup.py sdist
twine upload dist/*
```

License
-------
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Author
------
Bodo Graumann
mail@bodograumann.de
