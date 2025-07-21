import unittest

from website import extract_title


class TestWebsite(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a title"

        self.assertEqual(extract_title(md), "This is a title")

    def test_missing_h1_header(self):
        md = "## This is a h2 header"

        self.assertRaises(ValueError, lambda: extract_title(md))

        md = "This is a paragraph"

        self.assertRaises(ValueError, lambda: extract_title(md))
