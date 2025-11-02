import unittest
import iconv


class TestIconvExtension(unittest.TestCase):
    def test_basic(self):
        s = iconv.open("latin1", "utf-8")
        r = s.iconv(b"Hallo")
        self.assertEqual(r, b"Hallo")

    def test_with_length(self):
        s = iconv.open("utf-16le", "utf-8")
        r = s.iconv(b"Hallo", 11)
        self.assertEqual(r, "Hallo".encode("utf-16le"))

    def test_incorrect_input_type(self):
        s = iconv.open("latin1", "utf-8")
        with self.assertRaisesRegex(
            TypeError, "iconv expects byte object as first argument"
        ):
            r = s.iconv("Hallo")
