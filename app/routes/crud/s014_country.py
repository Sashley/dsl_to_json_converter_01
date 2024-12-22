from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S014_Country
from app import db

bp = Blueprint('s014_country', __name__)

@bp.route('/s014_country')
def list_s014_country():
    items = S014_Country.query.all()
    return render_template('crud/s014_country/list.html', items=items)

@bp.route('/s014_country/create', methods=['GET', 'POST'])
def create_s014_country():
    if request.method == 'POST':
        try:
            item = S014_Country()
            
            if 'name' in request.form:
                item.name = request.form['name']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s014_country.list_s014_country")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s014_country/form.html', 
                                edit=False, 
                                form_action=url_for('s014_country.create_s014_country')
                                )
    
    return render_template('crud/s014_country/form.html', 
                         edit=False, 
                         form_action=url_for('s014_country.create_s014_country')
                         )

@bp.route('/s014_country/<int:id>/edit', methods=['GET', 'POST'])
def edit_s014_country(id):
    item = S014_Country.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s014_country.list_s014_country"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s014_country/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s014_country.edit_s014_country', id=id)
                                )
    
    return render_template('crud/s014_country/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s014_country.edit_s014_country', id=id)
                         )

@bp.route('/s014_country/<int:id>/delete', methods=['DELETE'])
def delete_s014_country(id):
    try:
        item = S014_Country.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
