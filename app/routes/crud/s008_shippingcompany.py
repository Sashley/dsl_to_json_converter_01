from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S008_ShippingCompany
from app import db

bp = Blueprint('s008_shippingcompany', __name__)

@bp.route('/s008_shippingcompany')
def list_s008_shippingcompany():
    items = S008_ShippingCompany.query.all()
    return render_template('crud/s008_shippingcompany/list.html', items=items)

@bp.route('/s008_shippingcompany/create', methods=['GET', 'POST'])
def create_s008_shippingcompany():
    if request.method == 'POST':
        try:
            item = S008_ShippingCompany()
            
            if 'name' in request.form:
                item.name = request.form['name']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s008_shippingcompany.list_s008_shippingcompany")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s008_shippingcompany/form.html', 
                                edit=False, 
                                form_action=url_for('s008_shippingcompany.create_s008_shippingcompany')
                                )
    
    return render_template('crud/s008_shippingcompany/form.html', 
                         edit=False, 
                         form_action=url_for('s008_shippingcompany.create_s008_shippingcompany')
                         )

@bp.route('/s008_shippingcompany/<int:id>/edit', methods=['GET', 'POST'])
def edit_s008_shippingcompany(id):
    item = S008_ShippingCompany.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s008_shippingcompany.list_s008_shippingcompany"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s008_shippingcompany/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s008_shippingcompany.edit_s008_shippingcompany', id=id)
                                )
    
    return render_template('crud/s008_shippingcompany/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s008_shippingcompany.edit_s008_shippingcompany', id=id)
                         )

@bp.route('/s008_shippingcompany/<int:id>/delete', methods=['DELETE'])
def delete_s008_shippingcompany(id):
    try:
        item = S008_ShippingCompany.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
