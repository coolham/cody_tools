#!/usr/bin/env python3
"""
Example usage of OpenClaw File Tools
"""

from openclaw_tools import FileTools
import tempfile
import os

def main():
    print("=== OpenClaw File Tools Examples ===\n")
    
    # Create a temporary directory for examples
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Working in temporary directory: {tmpdir}\n")
        
        # Example 1: Write and read a text file
        print("1. Writing and reading a text file:")
        file_path = os.path.join(tmpdir, "example.txt")
        FileTools.write_file(file_path, "Hello, OpenClaw!\nThis is a test file.")
        content = FileTools.read_file(file_path)
        print(f"   Content: {content[:50]}...")
        print(f"   File size: {FileTools.get_file_size(file_path)} bytes\n")
        
        # Example 2: Append to a file
        print("2. Appending to a file:")
        FileTools.append_to_file(file_path, "\nAppended line.")
        content = FileTools.read_file(file_path)
        print(f"   Updated content: {content}\n")
        
        # Example 3: Working with JSON
        print("3. Working with JSON files:")
        json_path = os.path.join(tmpdir, "config.json")
        data = {
            "name": "OpenClaw",
            "version": "1.0",
            "features": ["automation", "AI", "chat"]
        }
        FileTools.write_json(json_path, data)
        loaded_data = FileTools.read_json(json_path)
        print(f"   Loaded JSON: {loaded_data}\n")
        
        # Example 4: Directory operations
        print("4. Directory operations:")
        subdir = os.path.join(tmpdir, "subdir")
        FileTools.create_directory(subdir)
        print(f"   Directory exists: {FileTools.directory_exists(subdir)}")
        
        # Create some test files
        for i in range(3):
            FileTools.write_file(os.path.join(subdir, f"file{i}.txt"), f"Content {i}")
        
        files = FileTools.list_directory(subdir, "*.txt")
        print(f"   Files in directory: {len(files)} files")
        for f in files:
            print(f"      - {os.path.basename(f)}")
        print()
        
        # Example 5: Copy and move files
        print("5. Copy and move operations:")
        source = os.path.join(tmpdir, "source.txt")
        copy_dest = os.path.join(tmpdir, "copied.txt")
        move_dest = os.path.join(tmpdir, "moved.txt")
        
        FileTools.write_file(source, "Original content")
        FileTools.copy_file(source, copy_dest)
        print(f"   File copied: {FileTools.file_exists(copy_dest)}")
        
        FileTools.move_file(copy_dest, move_dest)
        print(f"   File moved: {FileTools.file_exists(move_dest)}")
        print(f"   Original copy deleted: {not FileTools.file_exists(copy_dest)}\n")
        
        print("✓ All examples completed successfully!")

if __name__ == "__main__":
    main()
