import json
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Text, Index
from sqlalchemy.orm import declarative_base, relationship

# Mapping from JSON field types to SQLAlchemy column types
TYPE_MAPPING = {
    "Integer": Integer,
    "String": String,
    "Boolean": Boolean,
    "Float": Float,
    "DateTime": DateTime,
    "Text": Text
}

def create_model(name, model_data, base_cls=None):
    """
    Dynamically create a SQLAlchemy model class.
    
    Args:
        name: Name of the model/table
        fields: Field definitions
        base_cls: SQLAlchemy declarative base class to use (optional)
    """
    if base_cls is None:
        base_cls = declarative_base()
        
    attrs = {
        "__tablename__": name,
        "__table_args__": {"extend_existing": True}
    }
    
    relationships = {}
    has_primary_key = False
    columns = {}  # Store columns temporarily to reference in relationships

    fields = model_data["Fields"]
    # First pass: create all columns
    for field_name, field_def in fields.items():
        column_args = []

        # Map the type
        column_type = TYPE_MAPPING.get(field_def["type"], String)
        
        # Handle length for String type
        if field_def["type"] == "String" and field_def.get("length"):
            column_args.append(column_type(field_def["length"]))
        else:
            column_args.append(column_type)

        # Handle foreign key
        if field_def.get("foreign_key"):
            column_args.append(ForeignKey(field_def["foreign_key"]))

        # Add constraints
        column_kwargs = {}
        
        # Handle primary key
        if field_def.get("primary_key", False):
            column_kwargs["primary_key"] = True
            has_primary_key = True
            if field_def.get("auto_increment", False):
                column_kwargs["autoincrement"] = True
        
        # Handle nullable
        column_kwargs["nullable"] = field_def.get("nullable", True)

        # Handle unique constraint
        if field_def.get("unique", False):
            column_kwargs["unique"] = True

        # Create column
        column = Column(*column_args, **column_kwargs)
        attrs[field_name] = column
        columns[field_name] = column

    # Second pass: create relationships with explicit foreign keys
    for field_name, field_def in fields.items():
        if field_def.get("foreign_key"):
            # Extract relationship name from foreign key
            related_table = field_def["foreign_key"].split('.')[0]
            relationship_name = f"{field_name}_rel"
            # Create relationship with explicit foreign key
            relationships[relationship_name] = relationship(
                related_table,
                foreign_keys=[columns[field_name]]
            )

    # Add relationships
    attrs.update(relationships)

    if not has_primary_key:
        raise ValueError(f"Table '{name}' must have at least one primary key.")

    # Create the model class
    model = type(name, (base_cls,), attrs)

    # Add indexes if defined
    if "Indices" in model_data:
        for index_name, index_columns in model_data["Indices"].items():
            Index(
                index_name,
                *[getattr(model, col_name) for col_name in index_columns],
            )

    return model

def load_json_to_models(json_file, base_cls=None):
    """
    Load JSON and convert to SQLAlchemy models.
    
    Args:
        json_file: Path to the JSON file
        base_cls: SQLAlchemy declarative base class to use (optional)
    """
    with open(json_file, "r") as f:
        data = json.load(f)

    models = {}
    for model_name, model_data in data["Models"].items():
        model = create_model(model_name, model_data, base_cls)
        models[model_name] = model

    return models
