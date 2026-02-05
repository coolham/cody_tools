"""
Text processing tools for OpenClaw
"""

import re
from typing import List, Dict, Any


class TextTools:
    """Tools for text manipulation and processing"""
    
    @staticmethod
    def count_words(text: str) -> int:
        """
        Count words in text
        
        Args:
            text: Input text
            
        Returns:
            Number of words
        """
        return len(text.split())
    
    @staticmethod
    def count_characters(text: str, include_spaces: bool = True) -> int:
        """
        Count characters in text
        
        Args:
            text: Input text
            include_spaces: Whether to include spaces (default: True)
            
        Returns:
            Number of characters
        """
        if include_spaces:
            return len(text)
        return len(text.replace(' ', ''))
    
    @staticmethod
    def count_lines(text: str) -> int:
        """
        Count lines in text
        
        Args:
            text: Input text
            
        Returns:
            Number of lines
        """
        return len(text.splitlines())
    
    @staticmethod
    def to_uppercase(text: str) -> str:
        """
        Convert text to uppercase
        
        Args:
            text: Input text
            
        Returns:
            Uppercase text
        """
        return text.upper()
    
    @staticmethod
    def to_lowercase(text: str) -> str:
        """
        Convert text to lowercase
        
        Args:
            text: Input text
            
        Returns:
            Lowercase text
        """
        return text.lower()
    
    @staticmethod
    def to_title_case(text: str) -> str:
        """
        Convert text to title case
        
        Args:
            text: Input text
            
        Returns:
            Title case text
        """
        return text.title()
    
    @staticmethod
    def reverse_text(text: str) -> str:
        """
        Reverse text
        
        Args:
            text: Input text
            
        Returns:
            Reversed text
        """
        return text[::-1]
    
    @staticmethod
    def remove_whitespace(text: str) -> str:
        """
        Remove all whitespace from text
        
        Args:
            text: Input text
            
        Returns:
            Text without whitespace
        """
        return re.sub(r'\s+', '', text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace (replace multiple spaces with single space)
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        return re.sub(r'\s+', ' ', text).strip()
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """
        Extract email addresses from text
        
        Args:
            text: Input text
            
        Returns:
            List of email addresses
        """
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text
        
        Args:
            text: Input text
            
        Returns:
            List of URLs
        """
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)
    
    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """
        Extract phone numbers from text (US format)
        
        Args:
            text: Input text
            
        Returns:
            List of phone numbers
        """
        pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def replace_text(text: str, old: str, new: str) -> str:
        """
        Replace all occurrences of a substring
        
        Args:
            text: Input text
            old: Text to replace
            new: Replacement text
            
        Returns:
            Text with replacements
        """
        return text.replace(old, new)
    
    @staticmethod
    def find_and_replace_regex(text: str, pattern: str, replacement: str) -> str:
        """
        Find and replace using regex
        
        Args:
            text: Input text
            pattern: Regex pattern
            replacement: Replacement text
            
        Returns:
            Text with replacements
        """
        return re.sub(pattern, replacement, text)
    
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        pattern = r'[.!?]+\s+'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def truncate(text: str, length: int, suffix: str = "...") -> str:
        """
        Truncate text to specified length
        
        Args:
            text: Input text
            length: Maximum length
            suffix: Suffix to append if truncated (default: ...)
            
        Returns:
            Truncated text
        """
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove HTML tags from text
        
        Args:
            text: Input text
            
        Returns:
            Text without HTML tags
        """
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def slug_from_text(text: str) -> str:
        """
        Create a URL-friendly slug from text
        
        Args:
            text: Input text
            
        Returns:
            Slug
        """
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')
