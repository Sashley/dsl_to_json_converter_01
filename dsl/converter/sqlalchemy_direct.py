from typing import Dict, List, Tuple
import re
from pathlib import Path

class DSLConverter:
    def __init__(self):
        self.models: Dict[str, Dict] = {}
        self.relationships: Dict[str, List[Tuple[str, str, str]]] = {}
        self.model_counter = 1

    def parse_field_type(self, field_type: str) -> str:
        """Convert DSL types to SQLAlchemy types."""
        type_mapping = {
            "Int": "Integer",
            "String": "String",
            "DateTime": "DateTime",
            "Float": "Float",
            "Boolean": "Boolean"
        }
        return type_mapping.get(field_type, "String")

    def parse_relationship(self, field_type: str, attrs: str) -> Tuple[str, str, str]:
        """Parse relationship definitions from DSL."""
        rel_match = re.search(r'relationship: "([^"]+)"', attrs)
        back_pop_match = re.search(r'back_populates: "([^"]+)"', attrs)
        
        if rel_match and back_pop_match:
            rel_type = rel_match.group(1)
            back_populates = back_pop_match.group(1)
            target_model = field_type.replace("[]", "")
            return (rel_type, target_model, back_populates)
        return None

    def parse_foreign_key(self, ref_part: str) -> Tuple[str, str]:
        """Parse foreign key references."""
        match = re.search(r'ref: > (\w+)\.(\w+)', ref_part)
        if match:
            return match.groups()
        return None, None

    def convert_dsl_to_models(self, dsl_file: str | Path) -> str:
        """Convert DSL file directly to SQLAlchemy models."""
        current_model = None
        
        with open(dsl_file, "r") as f:
            for line in line_content := f.readlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("table"):
                    # Start new model definition
                    model_name = line.split()[1]
                    prefixed_name = f"S{self.model_counter:03}_{model_name}"
                    self.model_counter += 1
                    current_model = {
                        "name": model_name,
                        "fields": [],
                        "relationships": []
                    }
                    self.models[prefixed_name] = current_model

                elif current_model and line:
                    parts = line.split(maxsplit=2)
                    if len(parts) < 2:
                        continue

                    field_name, field_type = parts[0], parts[1]
                    attrs = parts[2] if len(parts) > 2 else ""

                    # Handle relationships
                    if "[]" in field_type:
                        rel_info = self.parse_relationship(field_type, attrs)
                        if rel_info:
                            self.models[prefixed_name]["relationships"].append(
                                (field_name, *rel_info)
                            )
                        continue

                    # Handle regular fields
                    field_def = {
                        "name": field_name,
                        "type": self.parse_field_type(field_type),
                        "primary_key": "pk" in attrs,
                        "autoincrement": "increment" in attrs,
                        "unique": "unique" in attrs,
                        "nullable": "nullable" not in attrs
                    }

                    # Handle foreign keys
                    if "ref:" in attrs:
                        target_model, target_field = self.parse_foreign_key(attrs)
                        if target_model and target_field:
                            field_def["foreign_key"] = (target_model, target_field)

                    self.models[prefixed_name]["fields"].append(field_def)

        return self.generate_models_code()

    def generate_models_code(self) -> str:
        """Generate SQLAlchemy models code."""
        imports = [
            "from app import db",
            "from datetime import datetime",
            "",
            "# Auto-generated SQLAlchemy models",
            ""
        ]

        model_codes = []
        for prefixed_name, model_data in self.models.items():
            class_lines = [f"class {prefixed_name}(db.Model):"]
            class_lines.append(f"    __tablename__ = '{prefixed_name.lower()}'")
            
            # Add relationships
            for rel_name, rel_type, target, back_populates in model_data.get("relationships", []):
                target_prefixed = f"S{self.model_counter:03}_{target}"
                if rel_type == "one-to-many":
                    class_lines.append(
                        f"    {rel_name} = db.relationship('{target_prefixed}', "
                        f"backref='{back_populates}', lazy='dynamic')"
                    )

            # Add fields
            for field in model_data["fields"]:
                constraints = []
                if field["primary_key"]:
                    constraints.append("primary_key=True")
                if field["autoincrement"]:
                    constraints.append("autoincrement=True")
                if not field["nullable"]:
                    constraints.append("nullable=False")
                if field["unique"]:
                    constraints.append("unique=True")
                
                if "foreign_key" in field:
                    target_model, target_field = field["foreign_key"]
                    target_prefixed = f"s{self.model_counter:03}_{target_model.lower()}"
                    constraints.append(f'db.ForeignKey("{target_prefixed}.{target_field}")')

                constraints_str = ", ".join(constraints)
                class_lines.append(
                    f"    {field['name']} = db.Column(db.{field['type']}"
                    f"{', ' + constraints_str if constraints_str else ''})"
                )

            model_codes.append("\n".join(class_lines) + "\n")

        return "\n".join(imports + model_codes)

def convert_dsl_to_sqlalchemy(input_file: str | Path, output_file: str | Path) -> None:
    """Convert DSL file to SQLAlchemy models file."""
    converter = DSLConverter()
    models_code = converter.convert_dsl_to_models(input_file)
    
    with open(output_file, "w") as f:
        f.write(models_code)
    
    print(f"SQLAlchemy models generated in {output_file}")

if __name__ == "__main__":
    # Example usage
    convert_dsl_to_sqlalchemy(
        "dsl/schemas/shipping/current/schema.dsl",
        "app/models/shipping.py"
    )
