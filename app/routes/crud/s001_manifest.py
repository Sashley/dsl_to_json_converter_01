from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.shipping import S001_Manifest
from app import db
from app.utils.relationships import get_related_data, create_s001_manifest, update_s001_manifest, delete_s001_manifest

bp = Blueprint('s001_manifest', __name__)

@bp.route('/s001_manifest')
def list_s001_manifest():
    items = S001_Manifest.query.all()
    return render_template('crud/s001_manifest/list.html', items=items)

@bp.route('/s001_manifest/create', methods=['GET', 'POST'])
def create_s001_manifest():
    if request.method == 'POST':
        try:
            success, item = create_s001_manifest(request.form)
            if success:
                return redirect(url_for("s001_manifest.list_s001_manifest")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s001_manifest/form.html', 
                                edit=False, 
                                form_action=url_for('s001_manifest.create_s001_manifest')
                                , **get_related_data())
    
    return render_template('crud/s001_manifest/form.html', 
                         edit=False, 
                         form_action=url_for('s001_manifest.create_s001_manifest')
                         , **get_related_data())

@bp.route('/s001_manifest/<int:id>/edit', methods=['GET', 'POST'])
def edit_s001_manifest(id):
    item = S001_Manifest.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            if update_s001_manifest(item, request.form):
                return redirect(url_for("s001_manifest.list_s001_manifest"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s001_manifest/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('s001_manifest.edit_s001_manifest', id=id)
                                , **get_related_data())
    
    return render_template('crud/s001_manifest/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('s001_manifest.edit_s001_manifest', id=id)
                         , **get_related_data())

@bp.route('/s001_manifest/<int:id>/delete', methods=['DELETE'])
def delete_s001_manifest(id):
    try:
        item = S001_Manifest.query.get_or_404(id)
        success = delete_s001_manifest(item)
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
