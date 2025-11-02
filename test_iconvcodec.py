import unittest
import iconvcodec
import codecs
import sys


class TestIconvcodecModule(unittest.TestCase):
    def test_encode(self):
        bytestring = "Hallo".encode("Georgian-PS")
        self.assertEqual(bytestring, b"Hallo")

    def test_encode_with_long_out(self):
        """Edge case where output has more bytes than input as utf-8"""
        bytestring = "™".encode("ASCII//TRANSLIT")
        if sys.platform.startswith("linux"):
            self.assertEqual(bytestring, b"(TM)")
        else:
            self.assertEqual(bytestring, b"TM")

    def test_decode(self):
        string = b"Hallo".decode("Georgian-PS")
        self.assertEqual(string, "Hallo")

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux only test")
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

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux only test")
    def test_incremental_decode(self):
        decoder = codecs.getincrementaldecoder("UCS2")()
        first = decoder.decode(b"\x41")
        second = decoder.decode(b"\x01", final=True)

        self.assertEqual(first, "")
        self.assertEqual(second, "\u0141")

    def test_available_encodings(self):
        # Some from the list on https://www.gnu.org/software/libiconv/
        encodings = (
            *[f"ISO-8859-{i}" for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 16)],
            *[
                f"CP{i}"
                for i in (
                    437,
                    737,
                    775,
                    852,
                    855,
                    857,
                    858,
                    860,
                    861,
                    862,
                    863,
                    865,
                    869,
                    1125,
                    1133,
                    1250,
                    1251,
                    1252,
                    1253,
                    1254,
                    1257,
                )
            ],
            "Georgian-PS",
            "ARMSCII-8",
            "KOI8-T",
            "PT154",
            "RK1048",
            "VISCII",
            "TCVN",
            "Macintosh",
        )
        for encoding in encodings:
            with self.subTest(encoding=encoding):
                codec_info = iconvcodec.lookup(encoding)
                if codec_info is None:
                    self.fail(f"Unsupported codec: '{encoding}'")
                # Actually test that encoding works
                try:
                    "a".encode(encoding)
                except Exception as e:
                    raise AssertionError(
                        f"Codec lookup succeeded but encode failed for '{encoding}'"
                    ) from None
