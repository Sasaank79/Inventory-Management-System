from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db
from app.auth import token_required

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/top-selling', methods=['GET'])
@token_required
def top_selling(current_user):
    # Raw SQL to get top selling products (most OUT quantity)
    sql = text("""
        SELECT p.name, SUM(t.quantity) as total_sold
        FROM inventory_transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.transaction_type = 'OUT'
        GROUP BY p.id, p.name
        ORDER BY total_sold DESC
        LIMIT 10
    """)
    
    result = db.session.execute(sql)
    data = [{'name': row[0], 'total_sold': int(row[1])} for row in result]
    return jsonify(data), 200

@analytics_bp.route('/api/analytics/low-stock', methods=['GET'])
@token_required
def low_stock(current_user):
    # Raw SQL to calculate stock and filter by threshold (e.g., < 20)
    # Using a subquery or CTE would be cleaner, but standard SQL works
    sql = text("""
        SELECT p.name, p.sku, 
               (COALESCE(SUM(CASE WHEN t.transaction_type = 'IN' THEN t.quantity ELSE 0 END), 0) - 
                COALESCE(SUM(CASE WHEN t.transaction_type = 'OUT' THEN t.quantity ELSE 0 END), 0)) as current_stock
        FROM products p
        LEFT JOIN inventory_transactions t ON p.id = t.product_id
        GROUP BY p.id, p.name, p.sku
        HAVING current_stock < 20
        ORDER BY current_stock ASC
    """)
    
    result = db.session.execute(sql)
    data = [{'name': row[0], 'sku': row[1], 'stock': int(row[2])} for row in result]
    return jsonify(data), 200

@analytics_bp.route('/api/analytics/stock-value', methods=['GET'])
@token_required
def stock_value(current_user):
    # Raw SQL for total value
    sql = text("""
        SELECT SUM(
            (COALESCE(in_sum, 0) - COALESCE(out_sum, 0)) * p.unit_price
        ) as total_value
        FROM products p
        LEFT JOIN (
            SELECT product_id, SUM(quantity) as in_sum 
            FROM inventory_transactions 
            WHERE transaction_type = 'IN' 
            GROUP BY product_id
        ) in_t ON p.id = in_t.product_id
        LEFT JOIN (
            SELECT product_id, SUM(quantity) as out_sum 
            FROM inventory_transactions 
            WHERE transaction_type = 'OUT' 
            GROUP BY product_id
        ) out_t ON p.id = out_t.product_id
    """)
    
    result = db.session.execute(sql)
    total_value = result.scalar() or 0
    return jsonify({'total_stock_value': float(total_value)}), 200
@analytics_bp.route('/api/analytics/recent-products', methods=['GET'])
@token_required
def recent_products(current_user):
    # Get 5 most recently added products
    sql = text("""
        SELECT p.name, p.sku, p.unit_price, s.name as supplier
        FROM products p
        JOIN suppliers s ON p.supplier_id = s.id
        ORDER BY p.id DESC
        LIMIT 5
    """)
    
    result = db.session.execute(sql)
    data = [{'name': row[0], 'sku': row[1], 'price': float(row[2]), 'supplier': row[3]} for row in result]
    return jsonify(data), 200
