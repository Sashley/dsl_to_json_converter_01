from pathlib import Path
import json
from typing import Dict, Any

def generate_crud_templates(json_file: str | Path, output_dir: str | Path) -> None:
    """Generate CRUD templates from a JSON schema file.
    
    Args:
        json_file: Path to the JSON schema file
        output_dir: Directory where templates will be generated
    """
    json_path = Path(json_file)
    output_path = Path(output_dir)
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    models = data["Models"]
    for model_name, model_data in models.items():
        table_name = model_name.lower()
        fields = model_data["Fields"]

        # Create output directory for the model
        model_dir = output_path / table_name
        model_dir.mkdir(parents=True, exist_ok=True)

        # Generate List Template
        list_template = model_dir / "list.html"
        list_template.write_text(f"""\
{{% extends "base.html" %}}

{{% block content %}}
<div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">{model_name} List</h1>
        <a href="{{{{ url_for('create_{table_name}') }}}}" 
           class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Add New {model_name}
        </a>
    </div>

    <div class="overflow-x-auto">
        <table class="min-w-full bg-white">
            <thead>
                <tr class="bg-gray-100">
                    {''.join(f'<th class="px-6 py-3 border-b-2 border-gray-200 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">{field}</th>' for field in fields.keys())}
                    <th class="px-6 py-3 border-b-2 border-gray-200 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Actions</th>
                </tr>
            </thead>
            <tbody hx-target="closest tr" hx-swap="outerHTML">
                {{% for item in items %}}
                {{% include '{table_name}/_row.html' %}}
                {{% endfor %}}
            </tbody>
        </table>
    </div>
</div>
{{% endblock %}}
""")

        # Generate Row Template
        row_template = model_dir / "_row.html"
        row_template.write_text(f"""\
<tr class="hover:bg-gray-50">
    {''.join(f'<td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">{{{{ item.{field} }}}}</td>' for field in fields.keys())}
    <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">
        <button hx-get="{{{{ url_for('edit_{table_name}', id=item.id) }}}}"
                class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-1 px-3 rounded text-sm mr-2">
            Edit
        </button>
        <button hx-delete="{{{{ url_for('delete_{table_name}', id=item.id) }}}}"
                hx-confirm="Are you sure you want to delete this {model_name}?"
                class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-3 rounded text-sm">
            Delete
        </button>
    </td>
</tr>
""")

        # Generate Form Template
        # Check if this is a complex model that needs relationship helpers
        is_complex = model_name in ['S001_Manifest', 'S002_LineItem']
        
        # Get relationship fields
        relationship_fields = []
        if is_complex:
            if model_name == 'S001_Manifest':
                relationship_fields = [
                    ('shipper_id', 'shippers', 'S015_Client'),
                    ('consignee_id', 'consignees', 'S015_Client'),
                    ('vessel_id', 'vessels', 'S009_Vessel'),
                    ('voyage_id', 'voyages', 'S010_Voyage'),
                    ('port_of_loading_id', 'ports', 'S012_Port'),
                    ('port_of_discharge_id', 'ports', 'S012_Port')
                ]
            elif model_name == 'S002_LineItem':
                relationship_fields = [
                    ('pack_type_id', 'pack_types', 'S004_PackType'),
                    ('commodity_id', 'commodities', 'S003_Commodity'),
                    ('container_id', 'containers', 'S005_Container'),
                    ('manifest_id', 'manifests', 'S001_Manifest')
                ]
        
        form_template = model_dir / "form.html"
        form_template.write_text(f"""\
{{% extends "base.html" %}}

{{% block content %}}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-6">{{{{ 'Edit ' if edit else 'Add New ' }}}}{model_name}</h1>

    <form hx-post="{{{{ form_action }}}}" hx-target="#main-content" class="max-w-lg">
        {''.join(f"""
        <div class="mb-4">
            <label for="{field}" class="block text-gray-700 text-sm font-bold mb-2">{field.title().replace('_', ' ')}</label>
            {'<select' if any(field == rel[0] for rel in relationship_fields) else '<input type="text"'} 
                   id="{field}" 
                   name="{field}"
                   class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                   {'>' if any(field == rel[0] for rel in relationship_fields) else f'value="{{{{ item.{field} if edit else \'\' }}}}">'}{'''
                <option value="">Select...</option>
                {{% for related in ''' + next(rel[1] for rel in relationship_fields if rel[0] == field) + ''' %}}
                <option value="{{{{ related.id }}}}" {{{{ 'selected' if edit and item.''' + field + ''' == related.id else '' }}}}>
                    {{{{ related.name if hasattr(related, 'name') else related.id }}}}
                </option>
                {{% endfor %}}
            </select>''' if any(field == rel[0] for rel in relationship_fields) else '</input>'}
        </div>""" for field in fields.keys())}
        
        <div class="flex items-center justify-between mt-6">
            <button type="submit" 
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                {{{{ 'Update' if edit else 'Create' }}}}
            </button>
            <a href="{{{{ url_for('{table_name}.list_{table_name}') }}}}" 
               class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                Cancel
            </a>
        </div>
    </form>
</div>
{{% endblock %}}
""")

    print(f"CRUD templates generated in {output_dir}")

if __name__ == "__main__":
    # Example usage
    generate_crud_templates("dsl/output/json/shipping.json", "app/templates")
