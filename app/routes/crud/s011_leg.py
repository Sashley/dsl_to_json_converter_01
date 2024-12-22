from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S011_Leg
from app import db

bp = Blueprint('s011_leg', __name__)

@bp.route('/s011_leg')
def list_s011_leg():
    items = S011_Leg.query.all()
    return render_template('crud/s011_leg/list.html', items=items)

@bp.route('/s011_leg/create', methods=['GET', 'POST'])
def create_s011_leg():
    if request.method == 'POST':
        try:
            item = S011_Leg()
            
            if 'voyage_id' in request.form:
                item.voyage_id = request.form['voyage_id']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'leg_number' in request.form:
                item.leg_number = request.form['leg_number']
            if 'eta' in request.form:
                item.eta = request.form['eta']
            if 'etd' in request.form:
                item.etd = request.form['etd']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s011_leg.list_s011_leg")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s011_leg/form.html', 
                                edit=False, 
                                form_action=url_for('s011_leg.create_s011_leg')
                                )
    
    return render_template('crud/s011_leg/form.html', 
                         edit=False, 
                         form_action=url_for('s011_leg.create_s011_leg')
                         )

@bp.route('/s011_leg/<int:id>/edit', methods=['GET', 'POST'])
def edit_s011_leg(id):
    item = S011_Leg.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'voyage_id' in request.form:
                item.voyage_id = request.form['voyage_id']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'leg_number' in request.form:
                item.leg_number = request.form['leg_number']
            if 'eta' in request.form:
                item.eta = request.form['eta']
            if 'etd' in request.form:
                item.etd = request.form['etd']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s011_leg.list_s011_leg"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s011_leg/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s011_leg.edit_s011_leg', id=id)
                                )
    
    return render_template('crud/s011_leg/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s011_leg.edit_s011_leg', id=id)
                         )

@bp.route('/s011_leg/<int:id>/delete', methods=['DELETE'])
def delete_s011_leg(id):
    try:
        item = S011_Leg.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
