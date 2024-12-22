from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S006_ContainerHistory
from app import db

bp = Blueprint('s006_containerhistory', __name__)

@bp.route('/s006_containerhistory')
def list_s006_containerhistory():
    items = S006_ContainerHistory.query.all()
    return render_template('crud/s006_containerhistory/list.html', items=items)

@bp.route('/s006_containerhistory/create', methods=['GET', 'POST'])
def create_s006_containerhistory():
    if request.method == 'POST':
        try:
            item = S006_ContainerHistory()
            
            if 'container_id' in request.form:
                item.container_id = request.form['container_id']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'client_id' in request.form:
                item.client_id = request.form['client_id']
            if 'container_status_id' in request.form:
                item.container_status_id = request.form['container_status_id']
            if 'damage' in request.form:
                item.damage = request.form['damage']
            if 'updated' in request.form:
                item.updated = request.form['updated']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s006_containerhistory.list_s006_containerhistory")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s006_containerhistory/form.html', 
                                edit=False, 
                                form_action=url_for('s006_containerhistory.create_s006_containerhistory')
                                )
    
    return render_template('crud/s006_containerhistory/form.html', 
                         edit=False, 
                         form_action=url_for('s006_containerhistory.create_s006_containerhistory')
                         )

@bp.route('/s006_containerhistory/<int:id>/edit', methods=['GET', 'POST'])
def edit_s006_containerhistory(id):
    item = S006_ContainerHistory.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'container_id' in request.form:
                item.container_id = request.form['container_id']
            if 'port_id' in request.form:
                item.port_id = request.form['port_id']
            if 'client_id' in request.form:
                item.client_id = request.form['client_id']
            if 'container_status_id' in request.form:
                item.container_status_id = request.form['container_status_id']
            if 'damage' in request.form:
                item.damage = request.form['damage']
            if 'updated' in request.form:
                item.updated = request.form['updated']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s006_containerhistory.list_s006_containerhistory"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s006_containerhistory/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s006_containerhistory.edit_s006_containerhistory', id=id)
                                )
    
    return render_template('crud/s006_containerhistory/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s006_containerhistory.edit_s006_containerhistory', id=id)
                         )

@bp.route('/s006_containerhistory/<int:id>/delete', methods=['DELETE'])
def delete_s006_containerhistory(id):
    try:
        item = S006_ContainerHistory.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
