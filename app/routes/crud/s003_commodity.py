from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S003_Commodity
from app import db

bp = Blueprint('s003_commodity', __name__)

@bp.route('/s003_commodity')
def list_s003_commodity():
    items = S003_Commodity.query.all()
    return render_template('crud/s003_commodity/list.html', items=items)

@bp.route('/s003_commodity/create', methods=['GET', 'POST'])
def create_s003_commodity():
    if request.method == 'POST':
        try:
            item = S003_Commodity()
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.add(item)
            db.session.commit()
            flash('Created successfully', 'success')
            return redirect(url_for("s003_commodity.list_s003_commodity")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s003_commodity/form.html', 
                                edit=False, 
                                form_action=url_for('s003_commodity.create_s003_commodity')
                                )
    
    return render_template('crud/s003_commodity/form.html', 
                         edit=False, 
                         form_action=url_for('s003_commodity.create_s003_commodity')
                         )

@bp.route('/s003_commodity/<int:id>/edit', methods=['GET', 'POST'])
def edit_s003_commodity(id):
    item = S003_Commodity.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            
            if 'name' in request.form:
                item.name = request.form['name']
            if 'description' in request.form:
                item.description = request.form['description']
            db.session.commit()
            flash('Updated successfully', 'success')
            return redirect(url_for("s003_commodity.list_s003_commodity"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s003_commodity/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s003_commodity.edit_s003_commodity', id=id)
                                )
    
    return render_template('crud/s003_commodity/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s003_commodity.edit_s003_commodity', id=id)
                         )

@bp.route('/s003_commodity/<int:id>/delete', methods=['DELETE'])
def delete_s003_commodity(id):
    try:
        item = S003_Commodity.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        success = True
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
