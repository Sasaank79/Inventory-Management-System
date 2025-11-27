from app import create_app

app = create_app()

with app.app_context():
    from app.models import db, User
    from werkzeug.security import generate_password_hash
    import os
    
    db.create_all()
    
    # Auto-create admin user if none exists
    if User.query.count() == 0:
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin')
        admin = User(
            username=admin_username,
            password_hash=generate_password_hash(admin_password)
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Created admin user: {admin_username}")
    else:
        print(f"✅ Database ready with {User.query.count()} users")

# Add a root route to render the login page or dashboard
from flask import render_template

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/products-page')
def products_page():
    return render_template('products.html')

@app.route('/transactions-page')
def transactions_page():
    return render_template('transactions.html')

@app.route('/analytics-page')
def analytics_page():
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
