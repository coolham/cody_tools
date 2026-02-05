"""
File manipulation tools for OpenClaw
"""

import os
import json
import shutil
from pathlib import Path
from typing import Union, List, Dict, Any


class FileTools:
    """Tools for file and directory operations"""
    
    @staticmethod
    def read_file(file_path: str, encoding: str = "utf-8") -> str:
        """
        Read content from a file
        
        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)
            
        Returns:
            File content as string
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Write content to a file
        
        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding (default: utf-8)
            
        Returns:
            True if successful
        """
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    
    @staticmethod
    def append_to_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Append content to a file
        
        Args:
            file_path: Path to the file
            content: Content to append
            encoding: File encoding (default: utf-8)
            
        Returns:
            True if successful
        """
        with open(file_path, 'a', encoding=encoding) as f:
            f.write(content)
        return True
    
    @staticmethod
    def list_directory(directory: str, pattern: str = "*") -> List[str]:
        """
        List files in a directory
        
        Args:
            directory: Directory path
            pattern: Glob pattern (default: *)
            
        Returns:
            List of file paths
        """
        path = Path(directory)
        return [str(p) for p in path.glob(pattern)]
    
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """
        Copy a file
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful
        """
        os.makedirs(os.path.dirname(destination) or '.', exist_ok=True)
        shutil.copy2(source, destination)
        return True
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """
        Move a file
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful
        """
        os.makedirs(os.path.dirname(destination) or '.', exist_ok=True)
        shutil.move(source, destination)
        return True
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        Check if a file exists
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file exists
        """
        return os.path.isfile(file_path)
    
    @staticmethod
    def directory_exists(directory: str) -> bool:
        """
        Check if a directory exists
        
        Args:
            directory: Directory path
            
        Returns:
            True if directory exists
        """
        return os.path.isdir(directory)
    
    @staticmethod
    def create_directory(directory: str) -> bool:
        """
        Create a directory
        
        Args:
            directory: Directory path
            
        Returns:
            True if successful
        """
        os.makedirs(directory, exist_ok=True)
        return True
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes
        
        Args:
            file_path: Path to the file
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(file_path)
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """
        Read JSON from a file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Parsed JSON as dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
        """
        Write JSON to a file
        
        Args:
            file_path: Path to the JSON file
            data: Data to write
            indent: JSON indentation (default: 2)
            
        Returns:
            True if successful
        """
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        return True
