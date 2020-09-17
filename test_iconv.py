import unittest
import iconv

class TestIconvExtension(unittest.TestCase):

    def test_basic(self):
        s=iconv.open("utf-8","latin1")
        r=s.iconv(b"Hallo")
        print(repr(r),len(r))

    def test_with_length(self):
        s=iconv.open("utf-8","utf-16le")
        r=s.iconv(b"Hallo", 10)
        print(repr(r),len(r))
