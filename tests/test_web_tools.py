"""
Unit tests for WebTools
"""

import unittest
from openclaw_tools import WebTools


class TestWebTools(unittest.TestCase):
    
    def test_encode_url(self):
        """Test URL encoding"""
        text = "Hello World!"
        encoded = WebTools.encode_url(text)
        self.assertIn("%20", encoded)
    
    def test_decode_url(self):
        """Test URL decoding"""
        encoded = "Hello%20World%21"
        decoded = WebTools.decode_url(encoded)
        self.assertEqual(decoded, "Hello World!")
    
    def test_parse_url(self):
        """Test URL parsing"""
        url = "https://openclaw.im:443/docs?page=1#section"
        components = WebTools.parse_url(url)
        
        self.assertEqual(components['scheme'], 'https')
        self.assertEqual(components['hostname'], 'openclaw.im')
        self.assertEqual(components['path'], '/docs')
        self.assertEqual(components['query'], 'page=1')
        self.assertEqual(components['fragment'], 'section')
    
    def test_build_url(self):
        """Test URL building"""
        base = "https://api.example.com/search"
        params = {"q": "test", "limit": "10"}
        url = WebTools.build_url(base, params)
        
        self.assertIn("q=test", url)
        self.assertIn("limit=10", url)
    
    def test_parse_query_string(self):
        """Test query string parsing"""
        query = "name=OpenClaw&version=1.0"
        parsed = WebTools.parse_query_string(query)
        
        self.assertEqual(parsed['name'], 'OpenClaw')
        self.assertEqual(parsed['version'], '1.0')
    
    def test_is_valid_url(self):
        """Test URL validation"""
        self.assertTrue(WebTools.is_valid_url("https://openclaw.im"))
        self.assertTrue(WebTools.is_valid_url("http://example.com/path"))
        self.assertFalse(WebTools.is_valid_url("not a url"))
        self.assertFalse(WebTools.is_valid_url("just-text"))
    
    def test_get_domain(self):
        """Test domain extraction"""
        url = "https://openclaw.im/docs/guide"
        domain = WebTools.get_domain(url)
        self.assertEqual(domain, "openclaw.im")
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        filename = "file: <with> invalid* chars?.txt"
        sanitized = WebTools.sanitize_filename(filename)
        
        self.assertNotIn("<", sanitized)
        self.assertNotIn(">", sanitized)
        self.assertNotIn("*", sanitized)
        self.assertNotIn("?", sanitized)


if __name__ == '__main__':
    unittest.main()
