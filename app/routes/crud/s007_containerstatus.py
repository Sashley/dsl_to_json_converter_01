from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S007_ContainerStatus
from app import db

bp = Blueprint('s007_containerstatus', __name__)

@bp.route('/s007_containerstatus')
def list_s007_containerstatus():
    items = S007_ContainerStatus.query.all()
    return render_template('crud/s007_containerstatus/list.html', items=items)

@bp.route('/s007_containerstatus/create', methods=['GET', 'POST'])
def create_s007_containerstatus():
    if request.method == 'POST':
        try:
            item = S007_ContainerStatus()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s007_containerstatus.list_s007_containerstatus")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s007_containerstatus/form.html', 
                                edit=False, 
                                form_action=url_for('s007_containerstatus.create_s007_containerstatus')
                                )
    
    return render_template('crud/s007_containerstatus/form.html', 
                         edit=False, 
                         form_action=url_for('s007_containerstatus.create_s007_containerstatus')
                         )

@bp.route('/s007_containerstatus/<int:id>/edit', methods=['GET', 'POST'])
def edit_s007_containerstatus(id):
    item = S007_ContainerStatus.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s007_containerstatus.list_s007_containerstatus"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s007_containerstatus/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s007_containerstatus.edit_s007_containerstatus', id=id)
                                )
    
    return render_template('crud/s007_containerstatus/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s007_containerstatus.edit_s007_containerstatus', id=id)
                         )

@bp.route('/s007_containerstatus/<int:id>/delete', methods=['DELETE'])
def delete_s007_containerstatus(id):
    try:
        item = S007_ContainerStatus.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
