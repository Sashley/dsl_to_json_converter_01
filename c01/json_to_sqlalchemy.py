import json
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Mapping from JSON field types to SQLAlchemy column types
TYPE_MAPPING = {
    "Integer": Integer,
    "String": String,
    "Boolean": Boolean,
    "Float": Float,
    "DateTime": DateTime,
    "Text": Text
}

def create_model(name, fields):
    """
    Dynamically create a SQLAlchemy model class.
    """
    attrs = {"__tablename__": name}
    has_primary_key = False

    for field_name, field_def in fields.items():
        column_args = []

        # Map the type
        column_type = TYPE_MAPPING.get(field_def["type"], String)
        column_args.append(column_type)

        # Add constraints
        if field_def.get("primary_key", False):
            attrs[field_name] = Column(*column_args, primary_key=True)
            has_primary_key = True
        elif field_def.get("foreign_key"):
            attrs[field_name] = Column(*column_args, ForeignKey(field_def["foreign_key"]), nullable=field_def.get("nullable", True))
        else:
            attrs[field_name] = Column(*column_args, nullable=field_def.get("nullable", True))

    if not has_primary_key:
        raise ValueError(f"Table '{name}' must have at least one primary key.")

    # Dynamically create a class
    return type(name, (Base,), attrs)

def load_json_to_models(json_file):
    """
    Load JSON and convert to SQLAlchemy models.
    """
    with open(json_file, "r") as f:
        data = json.load(f)

    models = {}
    for model_name, model_data in data["Models"].items():
        model = create_model(model_name, model_data["Fields"])
        models[model_name] = model

    return models
