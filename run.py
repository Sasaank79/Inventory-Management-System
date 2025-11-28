from app import create_app

app = create_app()

with app.app_context():
    from app.models import db
    db.create_all()
    print("✅ Database tables ready")

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
