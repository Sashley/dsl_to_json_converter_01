from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S002_LineItem
from app import db
from app.utils.relationships import get_related_data, create_s002_lineitem, update_s002_lineitem, delete_s002_lineitem

bp = Blueprint('s002_lineitem', __name__)

@bp.route('/s002_lineitem')
def list_s002_lineitem():
    items = S002_LineItem.query.all()
    return render_template('crud/s002_lineitem/list.html', items=items)

@bp.route('/s002_lineitem/create', methods=['GET', 'POST'])
def create_s002_lineitem():
    if request.method == 'POST':
        try:
            success, item = create_s002_lineitem(request.form)
            if success:
                return redirect(url_for("s002_lineitem.list_s002_lineitem")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s002_lineitem/form.html', 
                                edit=False, 
                                form_action=url_for('s002_lineitem.create_s002_lineitem')
                                , **get_related_data())
    
    return render_template('crud/s002_lineitem/form.html', 
                         edit=False, 
                         form_action=url_for('s002_lineitem.create_s002_lineitem')
                         , **get_related_data())

@bp.route('/s002_lineitem/<int:id>/edit', methods=['GET', 'POST'])
def edit_s002_lineitem(id):
    item = S002_LineItem.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            if update_s002_lineitem(item, request.form):
                return redirect(url_for("s002_lineitem.list_s002_lineitem"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s002_lineitem/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s002_lineitem.edit_s002_lineitem', id=id)
                                , **get_related_data())
    
    return render_template('crud/s002_lineitem/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s002_lineitem.edit_s002_lineitem', id=id)
                         , **get_related_data())

@bp.route('/s002_lineitem/<int:id>/delete', methods=['DELETE'])
def delete_s002_lineitem(id):
    try:
        item = S002_LineItem.query.get_or_404(id)
        success = delete_s002_lineitem(item)
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
