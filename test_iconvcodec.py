import unittest
import iconvcodec

class TestIconvcodecModule(unittest.TestCase):

    def test_encode(self):
        bytestring = "Hallo".encode("T.61")
        self.assertEqual(bytestring, b"Hallo")

    def test_decode(self):
        string = b"Hallo".decode("T.61")
        self.assertEqual(string, "Hallo")
