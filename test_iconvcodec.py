import unittest
import iconvcodec

class TestIconvcodecModule(unittest.TestCase):

    def test_encode(self):
        print("Hallo".encode("T.61"))

    def test_decode(self):
        print(repr(b"Hallo".decode("T.61")))
