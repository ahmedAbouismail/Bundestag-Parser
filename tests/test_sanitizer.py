import unittest
from source.sanitizer import sanitize_string, sanitize_json


class TestSanitizer(unittest.TestCase):

    def test_html_entities(self):
        self.assertEqual(sanitize_string("Dies &amp; das"), "Dies & das")
        self.assertEqual(sanitize_string("Weniger &lt; Mehr"), "Weniger < Mehr")

    def test_line_endings(self):
        self.assertEqual(sanitize_string("Hello\r\nWorld\r!"), "Hello World !")

    def test_non_printable_characters(self):
        self.assertEqual(sanitize_string("Hello\x00World\x07"), "HelloWorld")

    def test_smart_quotes(self):
        self.assertEqual(sanitize_string("“Hello” ‘World’"), '"Hello" \'World\'')

    def test_html_tags(self):
        self.assertEqual(sanitize_string("<b>Hello</b> <i>World</i>"), "Hello World")

    def test_redundant_spaces(self):
        self.assertEqual(sanitize_string("  Too   many   spaces  "), "Too many spaces")

    def test_sanitize_json(self):
        input_data = {
            "key1": "  Hello  <b>World</b>! ",
            "key2": ["This &amp; That", "Line\r\nEndings"],
            "key3": {"nested": "Non\x00Printable"}
        }
        expected_data = {
            "key1": "Hello World!",
            "key2": ["This & That", "Line Endings"],
            "key3": {"nested": "NonPrintable"}
        }
        self.assertEqual(sanitize_json(input_data), expected_data)


if __name__ == "__main__":
    unittest.main()
