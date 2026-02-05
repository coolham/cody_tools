# OpenClaw Tools

A comprehensive collection of utility tools for the [OpenClaw](https://openclaw.im/) AI automation framework.

## Overview

OpenClaw Tools provides a set of Python utilities designed to extend and enhance your OpenClaw automation capabilities. This package includes tools for file operations, text processing, web interactions, and system utilities.

## Features

### 📁 File Tools
- Read, write, and append files
- Copy, move, and delete files
- Directory operations
- JSON file handling
- File existence checks
- File size queries

### 📝 Text Tools
- Word, character, and line counting
- Case conversions (upper, lower, title)
- Text reversal and manipulation
- Email, URL, and phone number extraction
- Regular expression operations
- HTML tag removal
- URL slug generation

### 🌐 Web Tools
- URL encoding/decoding
- URL parsing and building
- HTTP content fetching
- JSON API interactions
- Query string parsing
- URL validation
- Domain extraction

### 💻 System Tools
- System information retrieval
- Environment variable management
- Command execution
- Timestamp generation
- File and string hashing (MD5, SHA256, etc.)
- UUID generation
- Path operations

## Installation

### From Source

```bash
git clone https://github.com/coolham/cody_tools.git
cd cody_tools
pip install -e .
```

### Using pip (when published)

```bash
pip install openclaw-tools
```

## Usage

### File Operations

```python
from openclaw_tools import FileTools

# Read a file
content = FileTools.read_file("example.txt")

# Write to a file
FileTools.write_file("output.txt", "Hello, OpenClaw!")

# Work with JSON
data = {"name": "OpenClaw", "type": "AI Assistant"}
FileTools.write_json("config.json", data)
config = FileTools.read_json("config.json")

# List files in a directory
files = FileTools.list_directory("./data", "*.txt")
```

### Text Processing

```python
from openclaw_tools import TextTools

# Count words
word_count = TextTools.count_words("Hello world from OpenClaw")

# Extract information
text = "Contact us at info@openclaw.im or visit https://openclaw.im"
emails = TextTools.extract_emails(text)
urls = TextTools.extract_urls(text)

# Format text
slug = TextTools.slug_from_text("My Awesome Blog Post")  # "my-awesome-blog-post"
truncated = TextTools.truncate("This is a long text", 10)  # "This is..."
```

### Web Operations

```python
from openclaw_tools import WebTools

# Parse URLs
components = WebTools.parse_url("https://openclaw.im/docs?page=1")
print(components['hostname'])  # openclaw.im

# Build URLs with parameters
url = WebTools.build_url("https://api.example.com/search", {
    "q": "openclaw",
    "limit": "10"
})

# Fetch content
html = WebTools.fetch_url("https://openclaw.im")
json_data = WebTools.fetch_json("https://api.example.com/data")

# URL validation
is_valid = WebTools.is_valid_url("https://openclaw.im")  # True
```

### System Utilities

```python
from openclaw_tools import SystemTools

# Get system information
info = SystemTools.get_system_info()
print(f"Platform: {info['platform']}")

# Execute commands
result = SystemTools.execute_command("ls -la")
if result['success']:
    print(result['stdout'])

# Generate hashes
text_hash = SystemTools.hash_string("OpenClaw", "sha256")
file_hash = SystemTools.hash_file("document.pdf", "md5")

# Work with timestamps
timestamp = SystemTools.get_timestamp()  # ISO format
unix_time = SystemTools.get_unix_timestamp()

# Generate unique IDs
uuid = SystemTools.generate_uuid()
```

## API Reference

### FileTools

| Method | Description |
|--------|-------------|
| `read_file(file_path, encoding='utf-8')` | Read content from a file |
| `write_file(file_path, content, encoding='utf-8')` | Write content to a file |
| `append_to_file(file_path, content, encoding='utf-8')` | Append content to a file |
| `list_directory(directory, pattern='*')` | List files in a directory |
| `copy_file(source, destination)` | Copy a file |
| `move_file(source, destination)` | Move a file |
| `delete_file(file_path)` | Delete a file |
| `file_exists(file_path)` | Check if a file exists |
| `directory_exists(directory)` | Check if a directory exists |
| `create_directory(directory)` | Create a directory |
| `get_file_size(file_path)` | Get file size in bytes |
| `read_json(file_path)` | Read JSON from a file |
| `write_json(file_path, data, indent=2)` | Write JSON to a file |

### TextTools

| Method | Description |
|--------|-------------|
| `count_words(text)` | Count words in text |
| `count_characters(text, include_spaces=True)` | Count characters in text |
| `count_lines(text)` | Count lines in text |
| `to_uppercase(text)` | Convert text to uppercase |
| `to_lowercase(text)` | Convert text to lowercase |
| `to_title_case(text)` | Convert text to title case |
| `reverse_text(text)` | Reverse text |
| `remove_whitespace(text)` | Remove all whitespace |
| `normalize_whitespace(text)` | Normalize whitespace |
| `extract_emails(text)` | Extract email addresses |
| `extract_urls(text)` | Extract URLs |
| `extract_phone_numbers(text)` | Extract phone numbers (US format) |
| `replace_text(text, old, new)` | Replace substring |
| `find_and_replace_regex(text, pattern, replacement)` | Regex find and replace |
| `split_into_sentences(text)` | Split text into sentences |
| `truncate(text, length, suffix='...')` | Truncate text |
| `remove_html_tags(text)` | Remove HTML tags |
| `slug_from_text(text)` | Create URL-friendly slug |

### WebTools

| Method | Description |
|--------|-------------|
| `encode_url(url)` | URL encode a string |
| `decode_url(url)` | URL decode a string |
| `parse_url(url)` | Parse URL into components |
| `build_url(base, params)` | Build URL with query parameters |
| `fetch_url(url, headers=None, timeout=30)` | Fetch content from URL |
| `fetch_json(url, headers=None, timeout=30)` | Fetch and parse JSON |
| `parse_query_string(query_string)` | Parse query string |
| `is_valid_url(url)` | Check if string is valid URL |
| `get_domain(url)` | Extract domain from URL |
| `sanitize_filename(filename)` | Sanitize filename |

### SystemTools

| Method | Description |
|--------|-------------|
| `get_system_info()` | Get system information |
| `get_environment_variable(name, default=None)` | Get environment variable |
| `set_environment_variable(name, value)` | Set environment variable |
| `get_current_directory()` | Get current working directory |
| `change_directory(path)` | Change working directory |
| `execute_command(command, shell=True, timeout=None)` | Execute shell command |
| `get_timestamp()` | Get current timestamp (ISO format) |
| `get_unix_timestamp()` | Get Unix timestamp |
| `hash_string(text, algorithm='sha256')` | Generate hash of string |
| `hash_file(file_path, algorithm='sha256')` | Generate hash of file |
| `generate_uuid()` | Generate UUID |
| `sleep(seconds)` | Sleep for specified seconds |
| `get_file_extension(filename)` | Get file extension |
| `join_paths(*paths)` | Join path components |

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [OpenClaw Official Website](https://openclaw.im/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/coolham/cody_tools).
