"""
Unit tests for FileTools
"""

import unittest
import tempfile
import os
import json
from openclaw_tools import FileTools


class TestFileTools(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_write_and_read_file(self):
        """Test writing and reading a file"""
        file_path = os.path.join(self.temp_dir, "test.txt")
        content = "Test content"
        
        FileTools.write_file(file_path, content)
        read_content = FileTools.read_file(file_path)
        
        self.assertEqual(content, read_content)
    
    def test_append_to_file(self):
        """Test appending to a file"""
        file_path = os.path.join(self.temp_dir, "test.txt")
        
        FileTools.write_file(file_path, "Line 1\n")
        FileTools.append_to_file(file_path, "Line 2\n")
        
        content = FileTools.read_file(file_path)
        self.assertEqual(content, "Line 1\nLine 2\n")
    
    def test_file_exists(self):
        """Test file existence check"""
        file_path = os.path.join(self.temp_dir, "test.txt")
        
        self.assertFalse(FileTools.file_exists(file_path))
        FileTools.write_file(file_path, "content")
        self.assertTrue(FileTools.file_exists(file_path))
    
    def test_directory_operations(self):
        """Test directory operations"""
        dir_path = os.path.join(self.temp_dir, "subdir")
        
        self.assertFalse(FileTools.directory_exists(dir_path))
        FileTools.create_directory(dir_path)
        self.assertTrue(FileTools.directory_exists(dir_path))
    
    def test_copy_file(self):
        """Test copying a file"""
        source = os.path.join(self.temp_dir, "source.txt")
        dest = os.path.join(self.temp_dir, "dest.txt")
        
        FileTools.write_file(source, "content")
        FileTools.copy_file(source, dest)
        
        self.assertTrue(FileTools.file_exists(dest))
        self.assertEqual(FileTools.read_file(dest), "content")
    
    def test_move_file(self):
        """Test moving a file"""
        source = os.path.join(self.temp_dir, "source.txt")
        dest = os.path.join(self.temp_dir, "dest.txt")
        
        FileTools.write_file(source, "content")
        FileTools.move_file(source, dest)
        
        self.assertFalse(FileTools.file_exists(source))
        self.assertTrue(FileTools.file_exists(dest))
    
    def test_delete_file(self):
        """Test deleting a file"""
        file_path = os.path.join(self.temp_dir, "test.txt")
        
        FileTools.write_file(file_path, "content")
        self.assertTrue(FileTools.file_exists(file_path))
        
        FileTools.delete_file(file_path)
        self.assertFalse(FileTools.file_exists(file_path))
    
    def test_get_file_size(self):
        """Test getting file size"""
        file_path = os.path.join(self.temp_dir, "test.txt")
        content = "Hello World"
        
        FileTools.write_file(file_path, content)
        size = FileTools.get_file_size(file_path)
        
        self.assertEqual(size, len(content.encode('utf-8')))
    
    def test_json_operations(self):
        """Test JSON read/write operations"""
        file_path = os.path.join(self.temp_dir, "test.json")
        data = {"name": "OpenClaw", "version": "1.0"}
        
        FileTools.write_json(file_path, data)
        loaded_data = FileTools.read_json(file_path)
        
        self.assertEqual(data, loaded_data)
    
    def test_list_directory(self):
        """Test listing directory contents"""
        # Create some test files
        for i in range(3):
            FileTools.write_file(os.path.join(self.temp_dir, f"file{i}.txt"), "content")
        FileTools.write_file(os.path.join(self.temp_dir, "file.md"), "content")
        
        txt_files = FileTools.list_directory(self.temp_dir, "*.txt")
        all_files = FileTools.list_directory(self.temp_dir)
        
        self.assertEqual(len(txt_files), 3)
        self.assertEqual(len(all_files), 4)


if __name__ == '__main__':
    unittest.main()
