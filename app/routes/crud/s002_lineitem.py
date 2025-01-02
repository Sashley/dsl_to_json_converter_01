from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from app.models.shipping import S002_LineItem, S015_Client, S009_Vessel
from app import db
from sqlalchemy import or_, func
from app.utils.relationships import get_related_data, create_s002_lineitem, update_s002_lineitem, delete_s002_lineitem

bp = Blueprint('s002_lineitem', __name__)

def get_search_filter(model, search_term):
    '''Return case-insensitive search filter for the model.'''
    if not search_term:
        return None
    
    # Convert search term to lowercase for case-insensitive search
    search_term = search_term.lower()
    
    conditions = []
    
    # Search in text fields
    text_fields = ['id', 'manifest_id', 'description', 'quantity', 'weight']
    for field in text_fields:
        if hasattr(model, field):
            if field.endswith('_id'):
                # Handle relationship fields
                if field == 'shipper_id':
                    conditions.append(model.shipper.has(func.lower(S015_Client.name).like(f'%{{search_term}}%')))
                elif field == 'consignee_id':
                    conditions.append(model.consignee.has(func.lower(S015_Client.name).like(f'%{{search_term}}%')))
                elif field == 'vessel_id':
                    conditions.append(model.vessel.has(func.lower(S009_Vessel.name).like(f'%{{search_term}}%')))
            else:
                # Handle regular fields
                conditions.append(func.lower(getattr(model, field)).like(f'%{{search_term}}%'))
    
    return or_(*conditions) if conditions else None

@bp.route('/')
def list_s002_lineitem():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '')
    
    # Build query with eager loading of relationships
    query = S002_LineItem.query
    
    query = query.options(
        db.joinedload(S002_LineItem.shipper),
        db.joinedload(S002_LineItem.consignee),
        db.joinedload(S002_LineItem.vessel),
        db.joinedload(S002_LineItem.voyage),
        db.joinedload(S002_LineItem.port_of_loading),
        db.joinedload(S002_LineItem.port_of_discharge)
    )
    
    # Apply search filter if provided
    search_filter = get_search_filter(S002_LineItem, search)
    if search_filter is not None:
        query = query.filter(search_filter)
    
    # Get paginated results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    # If this is an HTMX request, return only the rows
    if request.headers.get('HX-Request'):
        return render_template('crud/s002_lineitem/_rows.html', 
                            items=items,
                            has_more=pagination.has_next,
                            page=page)
    
    # For full page request, return complete template
    return render_template('crud/s002_lineitem/list.html', 
                         items=items,
                         has_more=pagination.has_next,
                         page=page,
                         per_page=per_page)

@bp.route('/create', methods=['GET', 'POST'])
def create_s002_lineitem():
    if request.method == 'POST':
        try:
            success, item = create_s002_lineitem(request.form)
            if success:
                return redirect(url_for("crud.s002_lineitem.list_s002_lineitem")) 
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s002_lineitem/form.html', 
                                edit=False, 
                                form_action=url_for('crud.s002_lineitem.create_s002_lineitem')
                                , **get_related_data())
    
    return render_template('crud/s002_lineitem/form.html', 
                         edit=False, 
                         form_action=url_for('crud.s002_lineitem.create_s002_lineitem')
                         , **get_related_data())

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_s002_lineitem(id):
    item = S002_LineItem.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            if update_s002_lineitem(item, request.form):
                return redirect(url_for("crud.s002_lineitem.list_s002_lineitem"))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return render_template('crud/s002_lineitem/form.html', 
                                edit=True, 
                                item=item,
                                form_action=url_for('crud.s002_lineitem.edit_s002_lineitem', id=id)
                                , **get_related_data())
    
    return render_template('crud/s002_lineitem/form.html', 
                         edit=True, 
                         item=item,
                         form_action=url_for('crud.s002_lineitem.edit_s002_lineitem', id=id)
                         , **get_related_data())

@bp.route('/<int:id>/delete', methods=['DELETE'])
def delete_s002_lineitem(id):
    try:
        item = S002_LineItem.query.get_or_404(id)
        success = delete_s002_lineitem(item)
        return '', 204 if success else 500
    except Exception as e:
        db.session.rollback()
        return str(e), 500
