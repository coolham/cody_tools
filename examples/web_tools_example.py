#!/usr/bin/env python3
"""
Example usage of OpenClaw Web Tools
"""

from openclaw_tools import WebTools

def main():
    print("=== OpenClaw Web Tools Examples ===\n")
    
    # Example 1: URL encoding and decoding
    print("1. URL encoding/decoding:")
    text = "Hello World! How are you?"
    encoded = WebTools.encode_url(text)
    decoded = WebTools.decode_url(encoded)
    print(f"   Original: '{text}'")
    print(f"   Encoded: '{encoded}'")
    print(f"   Decoded: '{decoded}'\n")
    
    # Example 2: URL parsing
    print("2. URL parsing:")
    url = "https://openclaw.im/docs?page=1&section=intro#overview"
    components = WebTools.parse_url(url)
    print(f"   URL: {url}")
    print(f"   Scheme: {components['scheme']}")
    print(f"   Hostname: {components['hostname']}")
    print(f"   Path: {components['path']}")
    print(f"   Query: {components['query']}")
    print(f"   Fragment: {components['fragment']}\n")
    
    # Example 3: Building URLs with parameters
    print("3. Building URLs:")
    base_url = "https://api.example.com/search"
    params = {
        "q": "openclaw",
        "limit": "10",
        "sort": "date"
    }
    full_url = WebTools.build_url(base_url, params)
    print(f"   Base: {base_url}")
    print(f"   Parameters: {params}")
    print(f"   Full URL: {full_url}\n")
    
    # Example 4: Query string parsing
    print("4. Query string parsing:")
    query = "name=OpenClaw&version=1.0&features=ai&features=automation"
    parsed = WebTools.parse_query_string(query)
    print(f"   Query string: {query}")
    print(f"   Parsed: {parsed}\n")
    
    # Example 5: URL validation
    print("5. URL validation:")
    test_urls = [
        "https://openclaw.im",
        "http://example.com/path",
        "not a url",
        "ftp://files.example.com",
        "just-text"
    ]
    for test_url in test_urls:
        is_valid = WebTools.is_valid_url(test_url)
        print(f"   '{test_url}' -> {'✓ Valid' if is_valid else '✗ Invalid'}")
    print()
    
    # Example 6: Domain extraction
    print("6. Domain extraction:")
    urls = [
        "https://openclaw.im/docs/guide",
        "http://blog.example.com/posts/123",
        "https://api.github.com/users/openclaw"
    ]
    for url in urls:
        domain = WebTools.get_domain(url)
        print(f"   {url} -> {domain}")
    print()
    
    # Example 7: Filename sanitization
    print("7. Filename sanitization:")
    filenames = [
        "My Document.pdf",
        "File: <with> invalid* chars?.txt",
        "path/to/file.doc",
        "double__underscores.txt"
    ]
    for filename in filenames:
        sanitized = WebTools.sanitize_filename(filename)
        print(f"   '{filename}' -> '{sanitized}'")
    print()
    
    # Example 8: Fetching content (commented out to avoid network dependency)
    print("8. Fetching content (example - not executed):")
    print("   # Fetch HTML content")
    print("   # html = WebTools.fetch_url('https://openclaw.im')")
    print("   ")
    print("   # Fetch JSON from API")
    print("   # data = WebTools.fetch_json('https://api.example.com/data')")
    print()
    
    print("✓ All examples completed successfully!")

if __name__ == "__main__":
    main()
