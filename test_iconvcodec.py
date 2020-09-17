import unittest
import iconvcodec


class TestIconvcodecModule(unittest.TestCase):
    def test_encode(self):
        bytestring = "Hallo".encode("T.61")
        self.assertEqual(bytestring, b"Hallo")

    def test_decode(self):
        string = b"Hallo".decode("T.61")
        self.assertEqual(string, "Hallo")

    def test_transliterate(self):
        string = "abc ß α € àḃç"
        bytestring = string.encode("ASCII//TRANSLIT")
        self.assertEqual(bytestring, b"abc ss ? EUR abc")
