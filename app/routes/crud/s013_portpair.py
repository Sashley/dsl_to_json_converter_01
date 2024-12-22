from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S013_PortPair
from app import db

bp = Blueprint('s013_portpair', __name__)

@bp.route('/s013_portpair')
def list_s013_portpair():
    items = S013_PortPair.query.all()
    return render_template('crud/s013_portpair/list.html', items=items)

@bp.route('/s013_portpair/create', methods=['GET', 'POST'])
def create_s013_portpair():
    if request.method == 'POST':
        try:
            item = S013_PortPair()
            
            if 'pol_id' in request.form:
                item.pol_id = request.form['pol_id']
            if 'pod_id' in request.form:
                item.pod_id = request.form['pod_id']
            if 'distance' in request.form:
                item.distance = request.form['distance']
            if 'distance_rate_code' in request.form:
                item.distance_rate_code = request.form['distance_rate_code']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s013_portpair.list_s013_portpair")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s013_portpair/form.html', 
                                edit=False, 
                                form_action=url_for('s013_portpair.create_s013_portpair')
                                )
    
    return render_template('crud/s013_portpair/form.html', 
                         edit=False, 
                         form_action=url_for('s013_portpair.create_s013_portpair')
                         )

@bp.route('/s013_portpair/<int:id>/edit', methods=['GET', 'POST'])
def edit_s013_portpair(id):
    item = S013_PortPair.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'pol_id' in request.form:
                item.pol_id = request.form['pol_id']
            if 'pod_id' in request.form:
                item.pod_id = request.form['pod_id']
            if 'distance' in request.form:
                item.distance = request.form['distance']
            if 'distance_rate_code' in request.form:
                item.distance_rate_code = request.form['distance_rate_code']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s013_portpair.list_s013_portpair"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s013_portpair/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s013_portpair.edit_s013_portpair', id=id)
                                )
    
    return render_template('crud/s013_portpair/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s013_portpair.edit_s013_portpair', id=id)
                         )

@bp.route('/s013_portpair/<int:id>/delete', methods=['DELETE'])
def delete_s013_portpair(id):
    try:
        item = S013_PortPair.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
