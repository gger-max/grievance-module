#!/usr/bin/env python3
"""Fix test files to expect 201 status code for POST requests."""

import re
from pathlib import Path

def fix_test_file(filepath):
    """Fix POST request status code expectations in test file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix POST requests to expect 201
    # Pattern: client.post(...) followed by assert response.status_code == 200
    pattern = r'(response = client\.post\([^)]+\))\s+(assert response\.status_code == )200'
    replacement = r'\1\n    \g<2>201'
    
    modified_content = re.sub(pattern, replacement, content)
    
    if modified_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        print(f"Fixed {filepath}")
        return True
    return False

# Fix all test files
test_dir = Path(__file__).parent / 'tests'
fixed_count = 0

for test_file in test_dir.glob('test_*.py'):
    if fix_test_file(test_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} test file(s)")
