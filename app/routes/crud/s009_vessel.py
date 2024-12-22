from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S009_Vessel
from app import db

bp = Blueprint('s009_vessel', __name__)

@bp.route('/s009_vessel')
def list_s009_vessel():
    items = S009_Vessel.query.all()
    return render_template('crud/s009_vessel/list.html', items=items)

@bp.route('/s009_vessel/create', methods=['GET', 'POST'])
def create_s009_vessel():
    if request.method == 'POST':
        try:
            item = S009_Vessel()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'shipping_company_id' in request.form:
                item.shipping_company_id = request.form['shipping_company_id']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s009_vessel.list_s009_vessel")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s009_vessel/form.html', 
                                edit=False, 
                                form_action=url_for('s009_vessel.create_s009_vessel')
                                )
    
    return render_template('crud/s009_vessel/form.html', 
                         edit=False, 
                         form_action=url_for('s009_vessel.create_s009_vessel')
                         )

@bp.route('/s009_vessel/<int:id>/edit', methods=['GET', 'POST'])
def edit_s009_vessel(id):
    item = S009_Vessel.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'shipping_company_id' in request.form:
                item.shipping_company_id = request.form['shipping_company_id']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s009_vessel.list_s009_vessel"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s009_vessel/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s009_vessel.edit_s009_vessel', id=id)
                                )
    
    return render_template('crud/s009_vessel/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s009_vessel.edit_s009_vessel', id=id)
                         )

@bp.route('/s009_vessel/<int:id>/delete', methods=['DELETE'])
def delete_s009_vessel(id):
    try:
        item = S009_Vessel.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
