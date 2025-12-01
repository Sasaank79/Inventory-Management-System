from flask import Blueprint, request, jsonify
from app.models import Product, Supplier, InventoryTransaction
from app import db
from app.auth import token_required

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
@token_required
def get_products(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('q', '', type=str)
    sort_by = request.args.get('sort', 'id', type=str)
    
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%') | Product.sku.ilike(f'%{search}%'))
    
    if sort_by == 'name':
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.id.asc())
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    products = pagination.items
    
    output = []
    for product in products:
        # Calculate current stock
        # Optimization: In a real app, this should be a joined query or cached field
        stock_in = db.session.query(db.func.sum(InventoryTransaction.quantity))\
            .filter_by(product_id=product.id, transaction_type='IN').scalar() or 0
        stock_out = db.session.query(db.func.sum(InventoryTransaction.quantity))\
            .filter_by(product_id=product.id, transaction_type='OUT').scalar() or 0
        current_stock = stock_in - stock_out
        
        output.append({
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'category': product.category,
            'supplier': product.supplier.name,
            'unit_price': float(product.unit_price),
            'stock': current_stock,
            'is_active': product.is_active
        })
        
    return jsonify({
        'products': output,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@products_bp.route('/api/products/<int:id>', methods=['GET'])
@token_required
def get_product(current_user, id):
    product = Product.query.get_or_404(id)
    stock_in = db.session.query(db.func.sum(InventoryTransaction.quantity))\
        .filter_by(product_id=product.id, transaction_type='IN').scalar() or 0
    stock_out = db.session.query(db.func.sum(InventoryTransaction.quantity))\
        .filter_by(product_id=product.id, transaction_type='OUT').scalar() or 0
    current_stock = stock_in - stock_out
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'sku': product.sku,
        'category': product.category,
        'supplier_id': product.supplier_id,
        'unit_price': float(product.unit_price),
        'stock': current_stock
    }), 200

@products_bp.route('/api/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.get_json()
    # Basic validation
    required = ['name', 'sku', 'category', 'supplier_id', 'unit_price']
    if not all(k in data for k in required):
        return jsonify({'message': 'Missing fields'}), 400
        
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({'message': 'SKU already exists'}), 400
        
    new_product = Product(
        name=data['name'],
        sku=data['sku'],
        category=data['category'],
        supplier_id=data['supplier_id'],
        unit_price=data['unit_price']
    )
    db.session.add(new_product)
    db.session.commit()
    
    # Optional: Add initial stock if provided
    if 'initial_stock' in data and int(data['initial_stock']) > 0:
        trans = InventoryTransaction(
            product_id=new_product.id,
            quantity=int(data['initial_stock']),
            transaction_type='IN',
            notes='Initial stock'
        )
        db.session.add(trans)
        db.session.commit()
        
    return jsonify({'message': 'Product created', 'id': new_product.id}), 201

@products_bp.route('/api/products/<int:id>', methods=['PUT'])
@token_required
def update_product(current_user, id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: product.name = data['name']
    if 'category' in data: product.category = data['category']
    if 'unit_price' in data: product.unit_price = data['unit_price']
    # SKU update might be restricted in real world, but allowing here
    if 'sku' in data and data['sku'] != product.sku:
        if Product.query.filter_by(sku=data['sku']).first():
            return jsonify({'message': 'SKU already exists'}), 400
        product.sku = data['sku']
        
    db.session.commit()
    return jsonify({'message': 'Product updated'}), 200

@products_bp.route('/api/products/<int:id>/toggle-active', methods=['PATCH'])
@token_required
def toggle_product_active(current_user, id):
    product = Product.query.get_or_404(id)
    product.is_active = not product.is_active
    db.session.commit()
    status = 'activated' if product.is_active else 'archived'
    return jsonify({'message': f'Product {status}', 'is_active': product.is_active}), 200

@products_bp.route('/api/products/<int:id>', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

