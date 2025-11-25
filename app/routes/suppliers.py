from flask import Blueprint, request, jsonify
from app.models import Supplier
from app import db
from app.auth import token_required

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/api/suppliers', methods=['GET'])
@token_required
def get_suppliers(current_user):
    suppliers = Supplier.query.all()
    output = []
    for s in suppliers:
        output.append({
            'id': s.id,
            'name': s.name,
            'contact_email': s.contact_email,
            'phone': s.phone,
            'address': s.address
        })
    return jsonify(output), 200

@suppliers_bp.route('/api/suppliers', methods=['POST'])
@token_required
def create_supplier(current_user):
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'message': 'Name is required'}), 400
        
    if Supplier.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'Supplier already exists'}), 400
        
    new_supplier = Supplier(
        name=data['name'],
        contact_email=data.get('contact_email'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier created', 'id': new_supplier.id}), 201
