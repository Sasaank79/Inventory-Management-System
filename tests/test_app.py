import pytest
from app import create_app, db
from app.models import User, Product, Supplier, InventoryTransaction
from werkzeug.security import generate_password_hash

import os

from sqlalchemy.pool import NullPool

@pytest.fixture
def app():
    app = create_app()
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.db')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "JWT_SECRET_KEY": "test-secret",
        "SQLALCHEMY_ENGINE_OPTIONS": {"poolclass": NullPool}
    })

    with app.app_context():
        db.create_all()
        
        # Check if admin exists (in case of failed previous run)
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password_hash=generate_password_hash('password'))
            db.session.add(admin)
        
        if not Supplier.query.filter_by(name='Test Supplier').first():
            supplier = Supplier(name='Test Supplier')
            db.session.add(supplier)
            
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()
        
    # Clean up file
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    # Login to get token
    res = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    return res.json['token']

def test_login(client):
    res = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    assert res.status_code == 200
    assert 'token' in res.json

def test_create_product(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    res = client.post('/api/products', json={
        'name': 'Test Widget',
        'sku': 'WIDGET-001',
        'category': 'Widgets',
        'supplier_id': 1,
        'unit_price': 19.99,
        'initial_stock': 100
    }, headers=headers)
    
    assert res.status_code == 201
    assert res.json['message'] == 'Product created'

def test_transaction_flow(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # 1. Create Product
    client.post('/api/products', json={
        'name': 'Flow Item',
        'sku': 'FLOW-001',
        'category': 'Test',
        'supplier_id': 1,
        'unit_price': 10.00,
        'initial_stock': 50
    }, headers=headers)
    
    # 2. Check Stock (Should be 50)
    res = client.get('/api/products/1', headers=headers)
    assert res.json['stock'] == 50
    
    # 3. Add Stock (IN +10)
    client.post('/api/transactions', json={
        'product_id': 1,
        'quantity': 10,
        'transaction_type': 'IN'
    }, headers=headers)
    
    # 4. Remove Stock (OUT -5)
    client.post('/api/transactions', json={
        'product_id': 1,
        'quantity': 5,
        'transaction_type': 'OUT'
    }, headers=headers)
    
    # 5. Verify Final Stock (50 + 10 - 5 = 55)
    res = client.get('/api/products/1', headers=headers)
    assert res.json['stock'] == 55

def test_analytics_top_selling(client, auth_token):
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Create Product
    client.post('/api/products', json={
        'name': 'Best Seller',
        'sku': 'BEST-001',
        'category': 'Test',
        'supplier_id': 1,
        'unit_price': 10.00,
        'initial_stock': 100
    }, headers=headers)
    
    # Sell 20
    client.post('/api/transactions', json={
        'product_id': 1,
        'quantity': 20,
        'transaction_type': 'OUT'
    }, headers=headers)
    
    # Check Analytics
    res = client.get('/api/analytics/top-selling', headers=headers)
    assert res.status_code == 200
    assert len(res.json) > 0
    assert res.json[0]['name'] == 'Best Seller'
    assert res.json[0]['total_sold'] == 20
