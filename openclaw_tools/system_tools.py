"""
System and utility tools for OpenClaw
"""

import os
import platform
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional


class SystemTools:
    """Tools for system operations and utilities"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            Dictionary with system information
        """
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
    
    @staticmethod
    def get_environment_variable(name: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable
        
        Args:
            name: Variable name
            default: Default value if not found
            
        Returns:
            Variable value or default
        """
        return os.environ.get(name, default)
    
    @staticmethod
    def set_environment_variable(name: str, value: str) -> bool:
        """
        Set an environment variable
        
        Args:
            name: Variable name
            value: Variable value
            
        Returns:
            True if successful
        """
        os.environ[name] = value
        return True
    
    @staticmethod
    def get_current_directory() -> str:
        """
        Get current working directory
        
        Returns:
            Current directory path
        """
        return os.getcwd()
    
    @staticmethod
    def change_directory(path: str) -> bool:
        """
        Change current working directory
        
        Args:
            path: New directory path
            
        Returns:
            True if successful
        """
        os.chdir(path)
        return True
    
    @staticmethod
    def execute_command(command: str, shell: bool = True, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute a shell command
        
        Args:
            command: Command to execute
            shell: Use shell (default: True)
            timeout: Command timeout in seconds
            
        Returns:
            Dictionary with stdout, stderr, and return code
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1,
                'success': False
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'success': False
            }
    
    @staticmethod
    def get_timestamp() -> str:
        """
        Get current timestamp
        
        Returns:
            ISO format timestamp
        """
        return datetime.now().isoformat()
    
    @staticmethod
    def get_unix_timestamp() -> int:
        """
        Get current Unix timestamp
        
        Returns:
            Unix timestamp (seconds since epoch)
        """
        return int(datetime.now().timestamp())
    
    @staticmethod
    def hash_string(text: str, algorithm: str = 'sha256') -> str:
        """
        Generate hash of a string
        
        Args:
            text: Text to hash
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Hash string
        """
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    
    @staticmethod
    def hash_file(file_path: str, algorithm: str = 'sha256') -> str:
        """
        Generate hash of a file
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Hash string
        """
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    @staticmethod
    def generate_uuid() -> str:
        """
        Generate a UUID
        
        Returns:
            UUID string
        """
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def sleep(seconds: float) -> bool:
        """
        Sleep for specified seconds
        
        Args:
            seconds: Number of seconds to sleep
            
        Returns:
            True after sleep completes
        """
        import time
        time.sleep(seconds)
        return True
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Get file extension
        
        Args:
            filename: Filename or path
            
        Returns:
            File extension (without dot)
        """
        return os.path.splitext(filename)[1].lstrip('.')
    
    @staticmethod
    def join_paths(*paths: str) -> str:
        """
        Join path components
        
        Args:
            *paths: Path components to join
            
        Returns:
            Joined path
        """
        return os.path.join(*paths)
