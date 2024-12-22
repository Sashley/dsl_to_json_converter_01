from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S004_PackType
from app import db

bp = Blueprint('s004_packtype', __name__)

@bp.route('/s004_packtype')
def list_s004_packtype():
    items = S004_PackType.query.all()
    return render_template('crud/s004_packtype/list.html', items=items)

@bp.route('/s004_packtype/create', methods=['GET', 'POST'])
def create_s004_packtype():
    if request.method == 'POST':
        try:
            item = S004_PackType()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s004_packtype.list_s004_packtype")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s004_packtype/form.html', 
                                edit=False, 
                                form_action=url_for('s004_packtype.create_s004_packtype')
                                )
    
    return render_template('crud/s004_packtype/form.html', 
                         edit=False, 
                         form_action=url_for('s004_packtype.create_s004_packtype')
                         )

@bp.route('/s004_packtype/<int:id>/edit', methods=['GET', 'POST'])
def edit_s004_packtype(id):
    item = S004_PackType.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s004_packtype.list_s004_packtype"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s004_packtype/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s004_packtype.edit_s004_packtype', id=id)
                                )
    
    return render_template('crud/s004_packtype/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s004_packtype.edit_s004_packtype', id=id)
                         )

@bp.route('/s004_packtype/<int:id>/delete', methods=['DELETE'])
def delete_s004_packtype(id):
    try:
        item = S004_PackType.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
