import os
import random
import logging
from faker import Faker
from app import create_app, db
from app.models import Supplier, Product, InventoryTransaction, User
from werkzeug.security import generate_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()

def generate_seed_data(num_products=500):
    suppliers = []
    for _ in range(20):
        suppliers.append({
            'name': fake.company(),
            'contact_email': fake.company_email(),
            'phone': fake.phone_number()[:20],  # Truncate to fit VARCHAR(20)
            'address': fake.address()
        })

    
    products = []
    categories = ['Electronics', 'Clothing', 'Home', 'Toys', 'Books', 'Tools']
    seen_skus = set()
    
    for _ in range(num_products):
        while True:
            sku = fake.ean13()
            if sku not in seen_skus:
                seen_skus.add(sku)
                break
        
        products.append({
            'name': fake.catch_phrase(),
            'sku': sku,
            'category': random.choice(categories),
            'supplier_name': random.choice(suppliers)['name'],
            'unit_price': round(random.uniform(10.0, 500.0), 2),
            'initial_stock': random.randint(10, 100)
        })
        
    return suppliers, products

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        logger.info("Creating database tables")
        
        # Check if database is already seeded by checking suppliers (not users)
        if Supplier.query.count() > 0:
            logger.info("Database already seeded")
            return
        
        # Create admin user if it doesn't exist
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin')
        
        if not User.query.filter_by(username=admin_username).first():
            admin = User(
                username=admin_username,
                password_hash=generate_password_hash(admin_password)
            )
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Creating admin user: {admin_username}")
        else:
            logger.info(f"Admin user {admin_username} already exists")
        
        # Always seed suppliers and products (100 in production, 500 in dev)
        is_dev = os.getenv('FLASK_ENV', 'production') == 'development'
        product_count = 500 if is_dev else 100
        
        logger.info(f"Seeding {product_count} products...")
        suppliers_data, products_data = generate_seed_data(product_count)
        
        # Insert suppliers
        logger.info("Seeding suppliers")
        supplier_map = {}
        for s_data in suppliers_data:
            if s_data['name'] not in supplier_map:
                supplier = Supplier(
                    name=s_data['name'],
                    contact_email=s_data['contact_email'],
                    phone=s_data['phone'],
                    address=s_data['address']
                )
                db.session.add(supplier)
                db.session.flush()
                supplier_map[s_data['name']] = supplier.id
        
        # Insert products and initial stock
        logger.info("Seeding products and initial transactions")
        for p_data in products_data:
            product = Product(
                name=p_data['name'],
                sku=p_data['sku'],
                category=p_data['category'],
                supplier_id=supplier_map[p_data['supplier_name']],
                unit_price=p_data['unit_price']
            )
            db.session.add(product)
            db.session.flush()
            
            transaction = InventoryTransaction(
                product_id=product.id,
                quantity=p_data['initial_stock'],
                transaction_type='IN',
                notes='Initial stock'
            )
            db.session.add(transaction)
        
        db.session.commit()
        logger.info("Seeding complete")

if __name__ == '__main__':
    seed_database()
