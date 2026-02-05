"""
Unit tests for SystemTools
"""

import unittest
import tempfile
import os
from openclaw_tools import SystemTools


class TestSystemTools(unittest.TestCase):
    
    def test_get_system_info(self):
        """Test system information retrieval"""
        info = SystemTools.get_system_info()
        
        self.assertIn('platform', info)
        self.assertIn('architecture', info)
        self.assertIn('python_version', info)
        self.assertIsInstance(info['platform'], str)
    
    def test_environment_variables(self):
        """Test environment variable operations"""
        var_name = "TEST_OPENCLAW_VAR"
        var_value = "test_value"
        
        SystemTools.set_environment_variable(var_name, var_value)
        retrieved = SystemTools.get_environment_variable(var_name)
        
        self.assertEqual(retrieved, var_value)
    
    def test_get_environment_variable_default(self):
        """Test environment variable with default value"""
        value = SystemTools.get_environment_variable("NONEXISTENT_VAR_12345", "default")
        self.assertEqual(value, "default")
    
    def test_get_current_directory(self):
        """Test getting current directory"""
        current_dir = SystemTools.get_current_directory()
        self.assertIsInstance(current_dir, str)
        self.assertTrue(os.path.isdir(current_dir))
    
    def test_execute_command(self):
        """Test command execution"""
        result = SystemTools.execute_command("echo 'test'")
        
        self.assertIn('stdout', result)
        self.assertIn('stderr', result)
        self.assertIn('returncode', result)
        self.assertIn('success', result)
        self.assertTrue(result['success'])
    
    def test_get_timestamp(self):
        """Test timestamp generation"""
        timestamp = SystemTools.get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertIn('T', timestamp)  # ISO format contains 'T'
    
    def test_get_unix_timestamp(self):
        """Test Unix timestamp generation"""
        timestamp = SystemTools.get_unix_timestamp()
        self.assertIsInstance(timestamp, int)
        self.assertGreater(timestamp, 0)
    
    def test_hash_string(self):
        """Test string hashing"""
        text = "OpenClaw"
        
        md5_hash = SystemTools.hash_string(text, 'md5')
        sha256_hash = SystemTools.hash_string(text, 'sha256')
        
        self.assertEqual(len(md5_hash), 32)  # MD5 is 32 chars
        self.assertEqual(len(sha256_hash), 64)  # SHA256 is 64 chars
    
    def test_hash_file(self):
        """Test file hashing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Test content")
            temp_file = f.name
        
        try:
            file_hash = SystemTools.hash_file(temp_file, 'sha256')
            self.assertEqual(len(file_hash), 64)
        finally:
            os.unlink(temp_file)
    
    def test_generate_uuid(self):
        """Test UUID generation"""
        uuid1 = SystemTools.generate_uuid()
        uuid2 = SystemTools.generate_uuid()
        
        self.assertNotEqual(uuid1, uuid2)
        self.assertEqual(len(uuid1), 36)  # Standard UUID length
        self.assertIn('-', uuid1)
    
    def test_get_file_extension(self):
        """Test file extension extraction"""
        self.assertEqual(SystemTools.get_file_extension("file.txt"), "txt")
        self.assertEqual(SystemTools.get_file_extension("document.pdf"), "pdf")
        self.assertEqual(SystemTools.get_file_extension("path/to/file.json"), "json")
    
    def test_join_paths(self):
        """Test path joining"""
        path = SystemTools.join_paths("home", "user", "documents")
        self.assertIn("home", path)
        self.assertIn("user", path)
        self.assertIn("documents", path)


if __name__ == '__main__':
    unittest.main()
