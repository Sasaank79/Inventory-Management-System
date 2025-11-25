import csv
import random
from faker import Faker
from app import create_app, db
from app.models import Supplier, Product, InventoryTransaction, User
from werkzeug.security import generate_password_hash

fake = Faker()

def generate_seed_data(num_products=500):
    suppliers = []
    for _ in range(20):
        suppliers.append({
            'name': fake.company(),
            'contact_email': fake.company_email(),
            'phone': fake.phone_number(),
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
        print("Creating database tables...")
        db.create_all()
        
        if User.query.first():
            print("Database already seeded.")
            return

        print("Seeding Users...")
        admin = User(username='admin', password_hash=generate_password_hash('admin'))
        db.session.add(admin)
        
        suppliers_data, products_data = generate_seed_data()
        
        print("Seeding Suppliers...")
        supplier_map = {} # name -> id
        for s_data in suppliers_data:
            if s_data['name'] not in supplier_map:
                supplier = Supplier(
                    name=s_data['name'],
                    contact_email=s_data['contact_email'],
                    phone=s_data['phone'],
                    address=s_data['address']
                )
                db.session.add(supplier)
                db.session.flush() # get ID
                supplier_map[s_data['name']] = supplier.id
        
        print("Seeding Products and Initial Transactions...")
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
            
            # Initial stock transaction
            transaction = InventoryTransaction(
                product_id=product.id,
                quantity=p_data['initial_stock'],
                transaction_type='IN',
                notes='Initial stock seeding'
            )
            db.session.add(transaction)
            
        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_database()
