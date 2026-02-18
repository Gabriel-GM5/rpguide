#!/usr/bin/env python3
"""
Simple test runner for the rpguide project.

This script runs all unit tests in the tests directory.
"""

import os
import sys
import subprocess

def run_tests():
    """Run all unit tests using pytest."""
    
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    try:
        # Run pytest on the tests directory
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', 
            '-v',
            '--tb=short'
        ], check=True, capture_output=True, text=True)
        
        print("All tests passed successfully!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("Some tests failed:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("pytest not found. Please install pytest:")
        print("  pip install pytest")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)