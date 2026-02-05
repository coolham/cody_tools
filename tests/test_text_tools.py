"""
Unit tests for TextTools
"""

import unittest
from openclaw_tools import TextTools


class TestTextTools(unittest.TestCase):
    
    def test_count_words(self):
        """Test word counting"""
        self.assertEqual(TextTools.count_words("Hello world"), 2)
        self.assertEqual(TextTools.count_words("One two three four"), 4)
        self.assertEqual(TextTools.count_words(""), 0)
    
    def test_count_characters(self):
        """Test character counting"""
        text = "Hello World"
        self.assertEqual(TextTools.count_characters(text), 11)
        self.assertEqual(TextTools.count_characters(text, include_spaces=False), 10)
    
    def test_count_lines(self):
        """Test line counting"""
        text = "Line 1\nLine 2\nLine 3"
        self.assertEqual(TextTools.count_lines(text), 3)
    
    def test_case_conversions(self):
        """Test case conversion methods"""
        text = "Hello World"
        self.assertEqual(TextTools.to_uppercase(text), "HELLO WORLD")
        self.assertEqual(TextTools.to_lowercase(text), "hello world")
        self.assertEqual(TextTools.to_title_case("hello world"), "Hello World")
    
    def test_reverse_text(self):
        """Test text reversal"""
        self.assertEqual(TextTools.reverse_text("Hello"), "olleH")
        self.assertEqual(TextTools.reverse_text("12345"), "54321")
    
    def test_remove_whitespace(self):
        """Test whitespace removal"""
        text = "Hello   World  Test"
        self.assertEqual(TextTools.remove_whitespace(text), "HelloWorldTest")
    
    def test_normalize_whitespace(self):
        """Test whitespace normalization"""
        text = "Hello   World    Test  "
        self.assertEqual(TextTools.normalize_whitespace(text), "Hello World Test")
    
    def test_extract_emails(self):
        """Test email extraction"""
        text = "Contact us at support@openclaw.im or info@example.com"
        emails = TextTools.extract_emails(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("support@openclaw.im", emails)
        self.assertIn("info@example.com", emails)
    
    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Visit https://openclaw.im or http://example.com"
        urls = TextTools.extract_urls(text)
        self.assertEqual(len(urls), 2)
        self.assertIn("https://openclaw.im", urls)
    
    def test_extract_phone_numbers(self):
        """Test phone number extraction"""
        text = "Call 555-123-4567 or 555.987.6543"
        phones = TextTools.extract_phone_numbers(text)
        self.assertEqual(len(phones), 2)
    
    def test_replace_text(self):
        """Test text replacement"""
        text = "Hello World World"
        result = TextTools.replace_text(text, "World", "OpenClaw")
        self.assertEqual(result, "Hello OpenClaw OpenClaw")
    
    def test_find_and_replace_regex(self):
        """Test regex find and replace"""
        text = "Date: 2024-01-01"
        result = TextTools.find_and_replace_regex(text, r'\d{4}', "YYYY")
        self.assertEqual(result, "Date: YYYY-01-01")
    
    def test_split_into_sentences(self):
        """Test sentence splitting"""
        text = "First sentence. Second sentence! Third sentence?"
        sentences = TextTools.split_into_sentences(text)
        self.assertEqual(len(sentences), 3)
    
    def test_truncate(self):
        """Test text truncation"""
        text = "This is a long text"
        self.assertEqual(TextTools.truncate(text, 10), "This is...")
        self.assertEqual(TextTools.truncate(text, 50), text)
    
    def test_remove_html_tags(self):
        """Test HTML tag removal"""
        html = "<p>Hello <strong>World</strong></p>"
        clean = TextTools.remove_html_tags(html)
        self.assertEqual(clean, "Hello World")
    
    def test_slug_from_text(self):
        """Test slug generation"""
        self.assertEqual(TextTools.slug_from_text("Hello World"), "hello-world")
        self.assertEqual(TextTools.slug_from_text("My Blog Post!"), "my-blog-post")
        self.assertEqual(TextTools.slug_from_text("Test   Multiple   Spaces"), "test-multiple-spaces")


if __name__ == '__main__':
    unittest.main()
