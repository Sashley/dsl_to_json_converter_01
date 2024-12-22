from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S015_Client
from app import db

bp = Blueprint('s015_client', __name__)

@bp.route('/s015_client')
def list_s015_client():
    items = S015_Client.query.all()
    return render_template('crud/s015_client/list.html', items=items)

@bp.route('/s015_client/create', methods=['GET', 'POST'])
def create_s015_client():
    if request.method == 'POST':
        try:
            item = S015_Client()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'address' in request.form:
                item.address = request.form['address']
            if 'town' in request.form:
                item.town = request.form['town']
            if 'country_id' in request.form:
                item.country_id = request.form['country_id']
            if 'contact_person' in request.form:
                item.contact_person = request.form['contact_person']
            if 'email' in request.form:
                item.email = request.form['email']
            if 'phone' in request.form:
                item.phone = request.form['phone']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s015_client.list_s015_client")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s015_client/form.html', 
                                edit=False, 
                                form_action=url_for('s015_client.create_s015_client')
                                )
    
    return render_template('crud/s015_client/form.html', 
                         edit=False, 
                         form_action=url_for('s015_client.create_s015_client')
                         )

@bp.route('/s015_client/<int:id>/edit', methods=['GET', 'POST'])
def edit_s015_client(id):
    item = S015_Client.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'address' in request.form:
                item.address = request.form['address']
            if 'town' in request.form:
                item.town = request.form['town']
            if 'country_id' in request.form:
                item.country_id = request.form['country_id']
            if 'contact_person' in request.form:
                item.contact_person = request.form['contact_person']
            if 'email' in request.form:
                item.email = request.form['email']
            if 'phone' in request.form:
                item.phone = request.form['phone']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s015_client.list_s015_client"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s015_client/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s015_client.edit_s015_client', id=id)
                                )
    
    return render_template('crud/s015_client/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s015_client.edit_s015_client', id=id)
                         )

@bp.route('/s015_client/<int:id>/delete', methods=['DELETE'])
def delete_s015_client(id):
    try:
        item = S015_Client.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
