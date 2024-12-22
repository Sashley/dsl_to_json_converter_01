from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S012_Port
from app import db

bp = Blueprint('s012_port', __name__)

@bp.route('/s012_port')
def list_s012_port():
    items = S012_Port.query.all()
    return render_template('crud/s012_port/list.html', items=items)

@bp.route('/s012_port/create', methods=['GET', 'POST'])
def create_s012_port():
    if request.method == 'POST':
        try:
            item = S012_Port()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'country_id' in request.form:
                item.country_id = request.form['country_id']
            if 'prefix' in request.form:
                item.prefix = request.form['prefix']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s012_port.list_s012_port")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s012_port/form.html', 
                                edit=False, 
                                form_action=url_for('s012_port.create_s012_port')
                                )
    
    return render_template('crud/s012_port/form.html', 
                         edit=False, 
                         form_action=url_for('s012_port.create_s012_port')
                         )

@bp.route('/s012_port/<int:id>/edit', methods=['GET', 'POST'])
def edit_s012_port(id):
    item = S012_Port.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'country_id' in request.form:
                item.country_id = request.form['country_id']
            if 'prefix' in request.form:
                item.prefix = request.form['prefix']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s012_port.list_s012_port"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s012_port/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s012_port.edit_s012_port', id=id)
                                )
    
    return render_template('crud/s012_port/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s012_port.edit_s012_port', id=id)
                         )

@bp.route('/s012_port/<int:id>/delete', methods=['DELETE'])
def delete_s012_port(id):
    try:
        item = S012_Port.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
