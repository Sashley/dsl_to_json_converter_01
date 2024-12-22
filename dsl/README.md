# DSL Tools for Shipping Domain

This directory contains the Domain Specific Language (DSL) tools for defining and managing shipping domain models.

## Directory Structure

```
dsl/
├── schemas/                   # DSL definition files
│   ├── shipping/             # Shipping domain schemas
│   │   ├── current/          # Current version of schemas
│   │   └── archive/          # Historical versions
│   └── validation/           # Schema validation rules
│
├── converter/                # Conversion tools
│   ├── dsl.py               # DSL parsing
│   ├── json.py              # JSON conversion
│   └── validation.py        # Validation logic
│
├── tests/                   # Test suite
│   ├── test_dsl.py         # DSL conversion tests
│   ├── test_json.py        # JSON conversion tests
│   └── fixtures/           # Test data
│
├── output/                  # Generated files
│   ├── json/               # Intermediate JSON
│   └── models/             # Generated SQLAlchemy models
│
└── scripts/                # Utility scripts
    ├── convert.py         # Main conversion script
    └── validate.py        # Schema validation script
```

## Installation

First, install the package in development mode:

```bash
# From the directory containing the dsl package:
pip install -e dsl

# Or with absolute path:
pip install -e /path/to/dsl

# On Windows:
pip install -e C:\path\to\dsl
```

## Usage

1. Place your DSL schema in `dsl/schemas/shipping/current/schema.dsl`
2. Run validation:
   ```bash
   python -m dsl.scripts.validate
   ```
3. Convert to SQLAlchemy models:
   ```bash
   python -m dsl.scripts.convert
   ```

Generated files will be placed in:

- JSON schema: `dsl/output/json/shipping.json`
- SQLAlchemy models: `dsl/output/models/shipping.py`
- Flask-SQLAlchemy models: `app/models/shipping.py`

## Development

- All conversion logic is in the `converter` package
- Add tests in the `tests` directory
- Generated files go to `output` directory
- Use `archive` directory for version history
