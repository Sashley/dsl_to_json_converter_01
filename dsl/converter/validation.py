import json
from dsl.schemas.validation.schema import DSLValidation

def validate_dsl(file_path):
    """
    Validate a DSL schema file.
    """
    try:
        with open(file_path, "r") as f:
            dsl_content = f.read()
        
        # Basic validation - check if it's a valid DSL file
        if not dsl_content.strip().startswith('table '):
            raise ValueError("DSL file must start with table definitions")
        
        # Check for balanced braces
        if dsl_content.count('{') != dsl_content.count('}'):
            raise ValueError("Unbalanced braces in DSL file")
        
        print("DSL validation passed successfully!")
        return True

    except Exception as e:
        print(f"DSL validation failed: {e}")
        return False


if __name__ == "__main__":
    # Path to the DSL JSON file
    dsl_json_file = "shipping_converted.json"

    # Validate the DSL file
    validated_data = validate_dsl(dsl_json_file)

    # Optionally, print the validated data
    # if validated_data:
    #     print(validated_data.model_dump_json(indent=4))
