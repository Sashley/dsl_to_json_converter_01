from pathlib import Path
import json
from typing import Dict, Any

def generate_crud_routes(json_file: str | Path, output_dir: str | Path) -> None:
    """Generate CRUD routes from a JSON schema file.
    
    Args:
        json_file: Path to the JSON schema file
        output_dir: Directory where route files will be generated
    """
    json_path = Path(json_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, "r") as f:
        data = json.load(f)
    
    # Generate routes for each model
    models = data["Models"]
    for model_name, model_data in models.items():
        table_name = model_name.lower()
        fields = model_data["Fields"]
        
        route_file = output_path / f"{table_name}.py"
        
        # Check if this is a complex model that needs relationship helpers
        is_complex = model_name in ['S001_Manifest', 'S002_LineItem']
        
        # Import statements
        imports = f"""from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import {model_name}
from app import db"""
        
        if is_complex:
            imports += f"""
from app.utils.relationships import get_related_data, create_{table_name}, update_{table_name}, delete_{table_name}"""
        
        # Route content
        route_content = f"""{imports}

bp = Blueprint('{table_name}', __name__)

@bp.route('/{table_name}')
def list_{table_name}():
    items = {model_name}.query.all()
    return render_template('crud/{table_name}/list.html', items=items)

@bp.route('/{table_name}/create', methods=['GET', 'POST'])
def create_{table_name}():
    if request.method == 'POST':
        try:
            {f'''success, item = create_{table_name}(request.form)
            if success:
                return redirect(url_for("{table_name}.list_{table_name}"))''' if is_complex else f'''item = {model_name}()
            {"".join(f"""
            if '{field}' in request.form:
                item.{field} = request.form['{field}']""" for field in fields.keys() if field != 'id')}
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("{table_name}.list_{table_name}"))'''} 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {{str(e)}}', 'error')
            return render_template('crud/{table_name}/form.html', 
                                edit=False, 
                                form_action=url_for('{table_name}.create_{table_name}')
                                {', **get_related_data()' if is_complex else ''})
    
    return render_template('crud/{table_name}/form.html', 
                         edit=False, 
                         form_action=url_for('{table_name}.create_{table_name}')
                         {', **get_related_data()' if is_complex else ''})

@bp.route('/{table_name}/<int:id>/edit', methods=['GET', 'POST'])
def edit_{table_name}(id):
    item = {model_name}.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            {f'''if update_{table_name}(item, request.form):
                return redirect(url_for("{table_name}.list_{table_name}"))''' if is_complex else f'''{"".join(f"""
            if '{field}' in request.form:
                item.{field} = request.form['{field}']""" for field in fields.keys() if field != 'id')}
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("{table_name}.list_{table_name}"))'''}
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {{str(e)}}', 'error')
            return render_template('crud/{table_name}/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('{table_name}.edit_{table_name}', id=id)
                                {', **get_related_data()' if is_complex else ''})
    
    return render_template('crud/{table_name}/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('{table_name}.edit_{table_name}', id=id)
                         {', **get_related_data()' if is_complex else ''})

@bp.route('/{table_name}/<int:id>/delete', methods=['DELETE'])
def delete_{table_name}(id):
    try:
        item = {model_name}.query.get_or_404(id)
        {f'success = delete_{table_name}(item)' if is_complex else 'db.session.delete(item)\n        db.session.commit()\n        success = True'}
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
"""
        route_file.write_text(route_content)
    
    # Generate routes/__init__.py to register all blueprints
    init_file = output_path / "__init__.py"
    init_content = """from flask import Blueprint

bp = Blueprint('crud', __name__)

"""
    
    # Import and register each model's blueprint
    for model_name in models.keys():
        table_name = model_name.lower()
        init_content += f"""from app.routes.crud import {table_name}
bp.register_blueprint({table_name}.bp)

"""
    
    init_file.write_text(init_content)
    
    print(f"CRUD routes generated in {output_dir}")

if __name__ == "__main__":
    # Example usage
    generate_crud_routes("dsl/output/json/shipping.json", "app/routes/crud")
