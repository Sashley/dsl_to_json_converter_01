from flask import Blueprint, render_template, request, jsonify
from app.models.shipping import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Main page route."""
    return render_template('index.html', title='Home')

@bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})
