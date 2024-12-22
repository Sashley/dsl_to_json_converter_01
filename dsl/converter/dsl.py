import json
import re
from collections import defaultdict

DEFAULT_PARAMS = {
    "nullable": True,
    "default": None,
}

def parse_foreign_key(ref_part, model_map):
    """Parse foreign key references."""
    match = re.search(r'ref: > (\w+)\.(\w+)', ref_part)
    if match:
        target_model, target_field = match.groups()
        return model_map.get(target_model, target_model), target_field
    return None, None

def first_pass_create_model_map(file_path):
    """First pass: Create a mapping of table names to prefixed names."""
    model_map = {}
    model_counter = 1
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("table"):
                table_name = line.split()[1]
                model_map[table_name] = f"S{model_counter:03}_{table_name}"
                model_counter += 1
    return model_map

def second_pass_generate_models(file_path, model_map):
    """Second pass: Process fields, menus, and indices."""
    result = {"version": "1.0", "Models": {}, "Menus": {"Main": [], "Context": {}, "Statistics": {}}}
    current_model = None

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("table"):
                # Start of a new table
                table_name = line.split()[1]
                prefixed_name = model_map[table_name]
                current_model = {
                    "Fields": {},
                    "Indices": {},
                    "Menus": {"Context": [], "Statistics": []}
                }
                result["Models"][prefixed_name] = current_model

                # Add main menu entry
                result["Menus"]["Main"].append({"table": table_name, "route": f"/view/{table_name}"})

            elif current_model:
                parts = line.split(maxsplit=2)
                # print('parts: ', parts)
                if len(parts) < 2:
                    continue  # Skip invalid or incomplete lines
                field_name, field_type = parts[0], parts[1]

                # Handle one-to-many relationships (type ending with []) first
                if "[]" in field_type and len(parts) == 3:
                    # Ensure valid drill-down reference exists in parts[2]
                    print('field type: ', field_type)
                    match = re.search(r'(\w+)\[\]', field_type)
                    if match:
                        related_table = match.group(1)  # Extract related table name
                        current_model["Menus"]["Context"].append(
                            {"drill_down": related_table, "route": f"/view/{related_table}?filter={field_name}"}
                        )
                    continue  # Skip regular field processing for array types

                # Process regular fields
                field_def = {"type": "Integer" if "Int" in field_type else "String"}

                # Handle field attributes
                if len(parts) == 3:
                    if "[pk" in parts[2]:
                        field_def["primary_key"] = True
                        field_def["nullable"] = False
                    if "increment" in parts[2]:
                        field_def["auto_increment"] = True
                    if "unique" in parts[2]:
                        field_def["unique"] = True
                    target_model, target_field = parse_foreign_key(parts[2], model_map)
                    if target_model and target_field:
                        field_def["foreign_key"] = f"{target_model}.{target_field}".lower()
                        field_def["nullable"] = True

                        # Context menu link for related table
                        current_model["Menus"]["Context"].append(
                            {"related_table": target_model, "route": f"/view/{target_model}?filter={field_name}"}
                        )

                # Add default parameters for non-primary, non-foreign fields
                if "primary_key" not in field_def and "foreign_key" not in field_def:
                    field_def.update(DEFAULT_PARAMS)
                
                current_model["Fields"][field_name] = field_def
                print('field def: ', field_def)

    # Add indices for foreign keys
    for model, data in result["Models"].items():
        for field, details in data["Fields"].items():
            if "foreign_key" in details:
                data["Indices"][f"idx_{field}"] = [field]

    return result

def convert_dsl_to_json(input_file, output_file):
    """Convert DSL file to JSON format."""
    model_map = first_pass_create_model_map(input_file)
    dsl_json = second_pass_generate_models(input_file, model_map)

    # Write to output JSON
    with open(output_file, "w") as f:
        json.dump(dsl_json, f, indent=4)
    
    return dsl_json
