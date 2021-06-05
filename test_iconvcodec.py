import unittest
import iconvcodec
import codecs


class TestIconvcodecModule(unittest.TestCase):
    def test_encode(self):
        bytestring = "Hallo".encode("T.61")
        self.assertEqual(bytestring, b"Hallo")

    def test_encode_with_long_out(self):
        """Edge case where output has more bytes than input as utf-8"""
        bytestring = "™".encode("ASCII//TRANSLIT")
        self.assertEqual(bytestring, b"(TM)")

    def test_decode(self):
        string = b"Hallo".decode("T.61")
        self.assertEqual(string, "Hallo")

    def test_transliterate(self):
        string = "abc ß α € àḃç"
        bytestring = string.encode("ASCII//TRANSLIT")
        self.assertEqual(bytestring, b"abc ss ? EUR abc")

    def test_incremental_encode(self):
        encoder = codecs.getincrementalencoder("ASCII//TRANSLIT")()
        first = encoder.encode("Foo")
        second = encoder.encode("bar", final=True)

        self.assertEqual(first, b"Foo")
        self.assertEqual(second, b"bar")

    def test_incremental_decode(self):
        decoder = codecs.getincrementaldecoder("UCS2")()
        first = decoder.decode(b"\x41")
        second = decoder.decode(b"\x01", final=True)

        self.assertEqual(first, "")
        self.assertEqual(second, "\u0141")
