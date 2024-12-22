from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S010_Voyage
from app import db

bp = Blueprint('s010_voyage', __name__)

@bp.route('/s010_voyage')
def list_s010_voyage():
    items = S010_Voyage.query.all()
    return render_template('crud/s010_voyage/list.html', items=items)

@bp.route('/s010_voyage/create', methods=['GET', 'POST'])
def create_s010_voyage():
    if request.method == 'POST':
        try:
            item = S010_Voyage()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'vessel_id' in request.form:
                item.vessel_id = request.form['vessel_id']
            if 'rotation_number' in request.form:
                item.rotation_number = request.form['rotation_number']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s010_voyage.list_s010_voyage")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s010_voyage/form.html', 
                                edit=False, 
                                form_action=url_for('s010_voyage.create_s010_voyage')
                                )
    
    return render_template('crud/s010_voyage/form.html', 
                         edit=False, 
                         form_action=url_for('s010_voyage.create_s010_voyage')
                         )

@bp.route('/s010_voyage/<int:id>/edit', methods=['GET', 'POST'])
def edit_s010_voyage(id):
    item = S010_Voyage.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'vessel_id' in request.form:
                item.vessel_id = request.form['vessel_id']
            if 'rotation_number' in request.form:
                item.rotation_number = request.form['rotation_number']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s010_voyage.list_s010_voyage"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s010_voyage/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s010_voyage.edit_s010_voyage', id=id)
                                )
    
    return render_template('crud/s010_voyage/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s010_voyage.edit_s010_voyage', id=id)
                         )

@bp.route('/s010_voyage/<int:id>/delete', methods=['DELETE'])
def delete_s010_voyage(id):
    try:
        item = S010_Voyage.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
