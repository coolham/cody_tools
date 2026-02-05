#!/usr/bin/env python3
"""
Example usage of OpenClaw System Tools
"""

from openclaw_tools import SystemTools
import tempfile
import os

def main():
    print("=== OpenClaw System Tools Examples ===\n")
    
    # Example 1: System information
    print("1. System information:")
    info = SystemTools.get_system_info()
    print(f"   Platform: {info['platform']}")
    print(f"   Architecture: {info['architecture']}")
    print(f"   Python version: {info['python_version']}\n")
    
    # Example 2: Environment variables
    print("2. Environment variables:")
    test_var = "OPENCLAW_TEST_VAR"
    SystemTools.set_environment_variable(test_var, "test_value")
    value = SystemTools.get_environment_variable(test_var)
    print(f"   Set and retrieved: {test_var}={value}")
    default_value = SystemTools.get_environment_variable("NONEXISTENT_VAR", "default")
    print(f"   With default: {default_value}\n")
    
    # Example 3: Timestamps
    print("3. Timestamp generation:")
    iso_time = SystemTools.get_timestamp()
    unix_time = SystemTools.get_unix_timestamp()
    print(f"   ISO timestamp: {iso_time}")
    print(f"   Unix timestamp: {unix_time}\n")
    
    # Example 4: Hashing
    print("4. Hashing:")
    text = "OpenClaw is awesome!"
    print(f"   Text: '{text}'")
    print(f"   MD5: {SystemTools.hash_string(text, 'md5')}")
    print(f"   SHA256: {SystemTools.hash_string(text, 'sha256')[:32]}...")
    
    # Hash a file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test file content")
        temp_file = f.name
    
    try:
        file_hash = SystemTools.hash_file(temp_file, 'sha256')
        print(f"   File hash: {file_hash[:32]}...\n")
    finally:
        os.unlink(temp_file)
    
    # Example 5: UUID generation
    print("5. UUID generation:")
    uuids = [SystemTools.generate_uuid() for _ in range(3)]
    for i, uuid in enumerate(uuids, 1):
        print(f"   UUID {i}: {uuid}")
    print()
    
    # Example 6: Path operations
    print("6. Path operations:")
    current_dir = SystemTools.get_current_directory()
    print(f"   Current directory: {current_dir}")
    
    joined_path = SystemTools.join_paths("/home", "user", "documents", "file.txt")
    print(f"   Joined path: {joined_path}")
    
    extension = SystemTools.get_file_extension("document.pdf")
    print(f"   File extension of 'document.pdf': {extension}\n")
    
    # Example 7: Command execution
    print("7. Command execution:")
    # Safe command that works on most systems
    result = SystemTools.execute_command("echo 'Hello from OpenClaw'")
    if result['success']:
        print(f"   Command output: {result['stdout'].strip()}")
        print(f"   Return code: {result['returncode']}")
    else:
        print(f"   Command failed: {result['stderr']}")
    print()
    
    print("✓ All examples completed successfully!")

if __name__ == "__main__":
    main()
