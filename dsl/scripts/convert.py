#!/usr/bin/env python3
"""
Main conversion script that orchestrates the DSL to SQLAlchemy model conversion process.
Uses existing conversion tools in their new locations.
"""
import os
import sys
import json
from pathlib import Path

# Add parent directory to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

from converter.validation import validate_dsl
from converter.dsl import convert_dsl_to_json
from converter.sqlalchemy import load_json_to_models

# Define model relationships
model_relationships = {
    'S001_Manifest': [
        "    shipper = db.relationship('S015_Client', foreign_keys=[shipper_id], backref='shipments_as_shipper')",
        "    consignee = db.relationship('S015_Client', foreign_keys=[consignee_id], backref='shipments_as_consignee')",
        "    vessel = db.relationship('S009_Vessel', backref='manifests')",
        "    voyage = db.relationship('S010_Voyage', backref='manifests')",
        "    port_of_loading = db.relationship('S012_Port', foreign_keys=[port_of_loading_id], backref='manifests_as_loading')",
        "    port_of_discharge = db.relationship('S012_Port', foreign_keys=[port_of_discharge_id], backref='manifests_as_discharge')",
        "    line_items = db.relationship('S002_LineItem', backref='manifest', lazy='dynamic')"
    ],
    'S002_LineItem': [
        "    pack_type = db.relationship('S004_PackType', backref='line_items')",
        "    commodity = db.relationship('S003_Commodity', backref='line_items')",
        "    container = db.relationship('S005_Container', backref='line_items')"
    ],
    'S005_Container': [
        "    port = db.relationship('S012_Port', backref='containers')",
        "    history = db.relationship('S006_ContainerHistory', backref='container', lazy='dynamic')"
    ],
    'S006_ContainerHistory': [
        "    port = db.relationship('S012_Port', backref='container_history')",
        "    client = db.relationship('S015_Client', backref='container_history')",
        "    status = db.relationship('S007_ContainerStatus', backref='container_history')"
    ],
    'S009_Vessel': [
        "    company = db.relationship('S008_ShippingCompany', backref='vessels')"
    ],
    'S010_Voyage': [
        "    vessel = db.relationship('S009_Vessel', backref='voyages')",
        "    legs = db.relationship('S011_Leg', backref='voyage', lazy='dynamic')"
    ],
    'S012_Port': [
        "    country = db.relationship('S014_Country', backref='ports')"
    ],
    'S013_PortPair': [
        "    port_of_loading = db.relationship('S012_Port', foreign_keys=[pol_id], backref='port_pairs_as_loading')",
        "    port_of_discharge = db.relationship('S012_Port', foreign_keys=[pod_id], backref='port_pairs_as_discharge')"
    ],
    'S015_Client': [
        "    country = db.relationship('S014_Country', backref='clients')"
    ],
    'S017_Rate': [
        "    commodity = db.relationship('S003_Commodity', backref='rates')",
        "    pack_type = db.relationship('S004_PackType', backref='rates')",
        "    client = db.relationship('S015_Client', backref='rates')"
    ]
}

def main():
    # Get paths relative to this script
    base_dir = Path(__file__).parent.parent
    schema_file = base_dir / 'schemas' / 'shipping' / 'current' / 'schema.dsl'
    json_file = base_dir / 'output' / 'json' / 'shipping.json'
    models_file = base_dir / 'output' / 'models' / 'shipping.py'
    flask_models_file = base_dir.parent / 'app' / 'models' / 'shipping.py'
    
    print("Starting DSL to SQLAlchemy model conversion process...")
    
    # Step 1: Validate DSL
    print("\n1. Validating DSL file...")
    if not schema_file.exists():
        print(f"Error: Schema file not found at {schema_file}")
        sys.exit(1)
    validate_dsl(schema_file)
    print("✓ DSL validation passed")
    
    # Step 2: Convert DSL to JSON
    print("\n2. Converting DSL to JSON...")
    convert_dsl_to_json(schema_file, json_file)
    print("✓ DSL converted to JSON")
    
    # Step 3: Load JSON data
    print("\n3. Loading JSON data...")
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    print("✓ JSON data loaded")
    
    # Step 4: Generate Flask-SQLAlchemy models
    print("\n4. Generating Flask-SQLAlchemy models...")
    content = 'from app import db\nfrom datetime import datetime\n\n# Auto-generated models using Flask-SQLAlchemy\n\n'
    
    # Generate Flask-SQLAlchemy models
    for model_name, model_data in json_data['Models'].items():
        class_lines = [f"class {model_name}(db.Model):", f"    __tablename__ = '{model_name.lower()}'"]
        
        # Add relationships first
        if model_name in model_relationships:
            class_lines.extend(model_relationships[model_name])
            class_lines.append("")
        
        # Add columns
        for field_name, field_info in model_data['Fields'].items():
            field_args = []
            
            # Map field type
            if field_info['type'] == 'String':
                field_args.append('db.String(255)')
            elif field_info['type'] == 'Integer':
                field_args.append('db.Integer')
            elif field_info['type'] == 'Float':
                field_args.append('db.Float')
            elif field_info['type'] == 'DateTime':
                field_args.append('db.DateTime')
            elif field_info['type'] == 'Boolean':
                field_args.append('db.Boolean')
            
            # Add constraints
            if field_info.get('primary_key'):
                field_args.append('primary_key=True')
            if field_info.get('auto_increment'):
                field_args.append('autoincrement=True')
            if not field_info.get('nullable', True):
                field_args.append('nullable=False')
            if field_info.get('unique'):
                field_args.append('unique=True')
            
            # Add foreign key if present
            if 'foreign_key' in field_info:
                field_args.append(f'db.ForeignKey("{field_info["foreign_key"]}")')
            
            field_def = f"    {field_name} = db.Column({', '.join(field_args)})"
            class_lines.append(field_def)
        
        class_lines.extend(["", "", ""])  # Add spacing between classes
        content += "\n".join(class_lines)
    
    # Write to Flask app
    with open(flask_models_file, 'w') as f:
        f.write(content)
    
    print("✓ Models copied to Flask app")
    print("\nConversion process completed successfully!")
    print(f"\nGenerated files:")
    print(f"- JSON schema: {json_file}")
    print(f"- SQLAlchemy models: {models_file}")
    print(f"- Flask-SQLAlchemy models: {flask_models_file}")

if __name__ == '__main__':
    main()
