from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S017_Rate
from app import db

bp = Blueprint('s017_rate', __name__)

@bp.route('/s017_rate')
def list_s017_rate():
    items = S017_Rate.query.all()
    return render_template('crud/s017_rate/list.html', items=items)

@bp.route('/s017_rate/create', methods=['GET', 'POST'])
def create_s017_rate():
    if request.method == 'POST':
        try:
            item = S017_Rate()
            
            if 'distance_rate_code' in request.form:
                item.distance_rate_code = request.form['distance_rate_code']
            if 'commodity_id' in request.form:
                item.commodity_id = request.form['commodity_id']
            if 'pack_type_id' in request.form:
                item.pack_type_id = request.form['pack_type_id']
            if 'client_id' in request.form:
                item.client_id = request.form['client_id']
            if 'rate' in request.form:
                item.rate = request.form['rate']
            if 'effective' in request.form:
                item.effective = request.form['effective']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s017_rate.list_s017_rate")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s017_rate/form.html', 
                                edit=False, 
                                form_action=url_for('s017_rate.create_s017_rate')
                                )
    
    return render_template('crud/s017_rate/form.html', 
                         edit=False, 
                         form_action=url_for('s017_rate.create_s017_rate')
                         )

@bp.route('/s017_rate/<int:id>/edit', methods=['GET', 'POST'])
def edit_s017_rate(id):
    item = S017_Rate.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'distance_rate_code' in request.form:
                item.distance_rate_code = request.form['distance_rate_code']
            if 'commodity_id' in request.form:
                item.commodity_id = request.form['commodity_id']
            if 'pack_type_id' in request.form:
                item.pack_type_id = request.form['pack_type_id']
            if 'client_id' in request.form:
                item.client_id = request.form['client_id']
            if 'rate' in request.form:
                item.rate = request.form['rate']
            if 'effective' in request.form:
                item.effective = request.form['effective']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s017_rate.list_s017_rate"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s017_rate/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s017_rate.edit_s017_rate', id=id)
                                )
    
    return render_template('crud/s017_rate/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s017_rate.edit_s017_rate', id=id)
                         )

@bp.route('/s017_rate/<int:id>/delete', methods=['DELETE'])
def delete_s017_rate(id):
    try:
        item = S017_Rate.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
