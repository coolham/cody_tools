#!/usr/bin/env python3
"""
Example usage of OpenClaw Text Tools
"""

from openclaw_tools import TextTools

def main():
    print("=== OpenClaw Text Tools Examples ===\n")
    
    # Example 1: Word and character counting
    print("1. Counting operations:")
    text = "Hello, OpenClaw! Welcome to AI automation."
    print(f"   Text: '{text}'")
    print(f"   Words: {TextTools.count_words(text)}")
    print(f"   Characters: {TextTools.count_characters(text)}")
    print(f"   Characters (no spaces): {TextTools.count_characters(text, include_spaces=False)}\n")
    
    # Example 2: Case conversions
    print("2. Case conversions:")
    print(f"   Uppercase: {TextTools.to_uppercase(text)}")
    print(f"   Lowercase: {TextTools.to_lowercase(text)}")
    print(f"   Title Case: {TextTools.to_title_case('hello world from openclaw')}\n")
    
    # Example 3: Extracting information
    print("3. Information extraction:")
    contact_text = """
    Contact us at support@openclaw.im or info@example.com
    Visit our website: https://openclaw.im
    Call us: 555-123-4567 or 555.987.6543
    """
    print(f"   Emails found: {TextTools.extract_emails(contact_text)}")
    print(f"   URLs found: {TextTools.extract_urls(contact_text)}")
    print(f"   Phone numbers found: {TextTools.extract_phone_numbers(contact_text)}\n")
    
    # Example 4: Text manipulation
    print("4. Text manipulation:")
    long_text = "This is a very long text that needs to be truncated for display purposes."
    print(f"   Original: '{long_text}'")
    print(f"   Truncated: '{TextTools.truncate(long_text, 30)}'")
    print(f"   Reversed: '{TextTools.reverse_text('OpenClaw')}'")
    print(f"   Normalized whitespace: '{TextTools.normalize_whitespace('Too    many     spaces')}'\n")
    
    # Example 5: URL slug generation
    print("5. Slug generation:")
    titles = [
        "My Awesome Blog Post!",
        "10 Tips for AI Automation",
        "Getting Started with OpenClaw (Tutorial)"
    ]
    for title in titles:
        slug = TextTools.slug_from_text(title)
        print(f"   '{title}' -> '{slug}'")
    print()
    
    # Example 6: HTML tag removal
    print("6. HTML tag removal:")
    html = "<h1>Welcome</h1><p>This is <strong>bold</strong> text.</p>"
    clean_text = TextTools.remove_html_tags(html)
    print(f"   HTML: {html}")
    print(f"   Clean: {clean_text}\n")
    
    # Example 7: Sentence splitting
    print("7. Sentence splitting:")
    paragraph = "First sentence. Second sentence! Third sentence? Fourth sentence."
    sentences = TextTools.split_into_sentences(paragraph)
    print(f"   Found {len(sentences)} sentences:")
    for i, sentence in enumerate(sentences, 1):
        print(f"      {i}. {sentence}")
    print()
    
    print("✓ All examples completed successfully!")

if __name__ == "__main__":
    main()
