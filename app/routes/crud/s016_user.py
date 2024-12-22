from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S016_User
from app import db

bp = Blueprint('s016_user', __name__)

@bp.route('/s016_user')
def list_s016_user():
    items = S016_User.query.all()
    return render_template('crud/s016_user/list.html', items=items)

@bp.route('/s016_user/create', methods=['GET', 'POST'])
def create_s016_user():
    if request.method == 'POST':
        try:
            item = S016_User()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'email' in request.form:
                item.email = request.form['email']
            if 'password_hash' in request.form:
                item.password_hash = request.form['password_hash']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s016_user.list_s016_user")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s016_user/form.html', 
                                edit=False, 
                                form_action=url_for('s016_user.create_s016_user')
                                )
    
    return render_template('crud/s016_user/form.html', 
                         edit=False, 
                         form_action=url_for('s016_user.create_s016_user')
                         )

@bp.route('/s016_user/<int:id>/edit', methods=['GET', 'POST'])
def edit_s016_user(id):
    item = S016_User.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'email' in request.form:
                item.email = request.form['email']
            if 'password_hash' in request.form:
                item.password_hash = request.form['password_hash']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s016_user.list_s016_user"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s016_user/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s016_user.edit_s016_user', id=id)
                                )
    
    return render_template('crud/s016_user/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s016_user.edit_s016_user', id=id)
                         )

@bp.route('/s016_user/<int:id>/delete', methods=['DELETE'])
def delete_s016_user(id):
    try:
        item = S016_User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
