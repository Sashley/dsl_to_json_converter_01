#!/usr/bin/env python3
"""
Script to validate DSL schema files.
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from dsl.converter.validation import validate_dsl

def main():
    base_dir = Path(__file__).parent.parent
    schema_file = base_dir / 'schemas' / 'shipping' / 'current' / 'schema.dsl'
    
    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)
    
    print(f"Validating schema file: {schema_file}")
    validate_dsl(schema_file)
    print("✓ Schema validation passed")

if __name__ == '__main__':
    main()
