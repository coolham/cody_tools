"""
Web-related tools for OpenClaw
"""

import json
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional


class WebTools:
    """Tools for web operations"""
    
    @staticmethod
    def encode_url(url: str) -> str:
        """
        URL encode a string
        
        Args:
            url: String to encode
            
        Returns:
            URL-encoded string
        """
        return urllib.parse.quote(url)
    
    @staticmethod
    def decode_url(url: str) -> str:
        """
        URL decode a string
        
        Args:
            url: String to decode
            
        Returns:
            URL-decoded string
        """
        return urllib.parse.unquote(url)
    
    @staticmethod
    def parse_url(url: str) -> Dict[str, Any]:
        """
        Parse a URL into components
        
        Args:
            url: URL to parse
            
        Returns:
            Dictionary with URL components
        """
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'hostname': parsed.hostname,
            'port': parsed.port,
        }
    
    @staticmethod
    def build_url(base: str, params: Dict[str, str]) -> str:
        """
        Build a URL with query parameters
        
        Args:
            base: Base URL
            params: Dictionary of query parameters
            
        Returns:
            Complete URL with parameters
        """
        query_string = urllib.parse.urlencode(params)
        separator = '&' if '?' in base else '?'
        return f"{base}{separator}{query_string}"
    
    @staticmethod
    def fetch_url(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> str:
        """
        Fetch content from a URL
        
        Args:
            url: URL to fetch
            headers: Optional HTTP headers
            timeout: Request timeout in seconds (default: 30)
            
        Returns:
            Response content as string
        """
        req = urllib.request.Request(url)
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    
    @staticmethod
    def fetch_json(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> Dict[str, Any]:
        """
        Fetch and parse JSON from a URL
        
        Args:
            url: URL to fetch
            headers: Optional HTTP headers
            timeout: Request timeout in seconds (default: 30)
            
        Returns:
            Parsed JSON as dictionary
        """
        content = WebTools.fetch_url(url, headers, timeout)
        return json.loads(content)
    
    @staticmethod
    def parse_query_string(query_string: str) -> Dict[str, str]:
        """
        Parse a query string into a dictionary
        
        Args:
            query_string: Query string to parse
            
        Returns:
            Dictionary of query parameters
        """
        return dict(urllib.parse.parse_qsl(query_string))
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Check if a string is a valid URL
        
        Args:
            url: String to validate
            
        Returns:
            True if valid URL
        """
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def get_domain(url: str) -> str:
        """
        Extract domain from URL
        
        Args:
            url: URL to parse
            
        Returns:
            Domain name
        """
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing invalid characters
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename
        """
        import re
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'_{2,}', '_', filename)
        return filename.strip('_')
