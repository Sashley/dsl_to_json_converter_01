from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S005_Container
from app import db

bp = Blueprint('s005_container', __name__)

@bp.route('/s005_container')
def list_s005_container():
    items = S005_Container.query.all()
    return render_template('crud/s005_container/list.html', items=items)

@bp.route('/s005_container/create', methods=['GET', 'POST'])
def create_s005_container():
    if request.method == 'POST':
        try:
            item = S005_Container()
            
            if 'number' in request.form:
                item.number = request.form['number']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'updated' in request.form:
                item.updated = request.form['updated']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s005_container.list_s005_container")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s005_container/form.html', 
                                edit=False, 
                                form_action=url_for('s005_container.create_s005_container')
                                )
    
    return render_template('crud/s005_container/form.html', 
                         edit=False, 
                         form_action=url_for('s005_container.create_s005_container')
                         )

@bp.route('/s005_container/<int:id>/edit', methods=['GET', 'POST'])
def edit_s005_container(id):
    item = S005_Container.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'number' in request.form:
                item.number = request.form['number']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'updated' in request.form:
                item.updated = request.form['updated']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s005_container.list_s005_container"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s005_container/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s005_container.edit_s005_container', id=id)
                                )
    
    return render_template('crud/s005_container/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s005_container.edit_s005_container', id=id)
                         )

@bp.route('/s005_container/<int:id>/delete', methods=['DELETE'])
def delete_s005_container(id):
    try:
        item = S005_Container.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
