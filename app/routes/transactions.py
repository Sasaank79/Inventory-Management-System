from flask import Blueprint, request, jsonify
from app.models import InventoryTransaction, Product
from app import db
from app.auth import token_required

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/api/transactions', methods=['POST'])
@token_required
def create_transaction(current_user):
    data = request.get_json()
    required = ['product_id', 'quantity', 'transaction_type']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
        
    if data['transaction_type'] not in ['IN', 'OUT']:
        return jsonify({'message': 'Invalid transaction type'}), 400
        
    if int(data['quantity']) <= 0:
        return jsonify({'message': 'Quantity must be positive'}), 400
        
    # Check if product exists
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'message': 'Product not found'}), 404
        
    # For OUT transactions, check stock
    if data['transaction_type'] == 'OUT':
        stock_in = db.session.query(db.func.sum(InventoryTransaction.quantity))\
            .filter_by(product_id=product.id, transaction_type='IN').scalar() or 0
        stock_out = db.session.query(db.func.sum(InventoryTransaction.quantity))\
            .filter_by(product_id=product.id, transaction_type='OUT').scalar() or 0
        current_stock = stock_in - stock_out
        
        if current_stock < int(data['quantity']):
            return jsonify({'message': 'Insufficient stock'}), 400

    new_trans = InventoryTransaction(
        product_id=data['product_id'],
        quantity=data['quantity'],
        transaction_type=data['transaction_type'],
        notes=data.get('notes')
    )
    db.session.add(new_trans)
    db.session.commit()
    
    return jsonify({'message': 'Transaction recorded', 'id': new_trans.id}), 201

@transactions_bp.route('/api/transactions', methods=['GET'])
@token_required
def get_transactions(current_user):
    # Optional filters
    product_id = request.args.get('product_id')
    
    query = InventoryTransaction.query
    if product_id:
        query = query.filter_by(product_id=product_id)
        
    transactions = query.order_by(InventoryTransaction.transaction_date.desc()).limit(100).all()
    
    output = []
    for t in transactions:
        output.append({
            'id': t.id,
            'product_name': t.product.name,
            'quantity': t.quantity,
            'type': t.transaction_type,
            'date': t.transaction_date.isoformat(),
            'notes': t.notes
        })
    return jsonify(output), 200
