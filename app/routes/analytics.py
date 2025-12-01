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
    # PostgreSQL requires repeating the aggregate expression in HAVING, or using a subquery/CTE.
    sql = text("""
        SELECT p.name, p.sku, 
               (COALESCE(SUM(CASE WHEN t.transaction_type = 'IN' THEN t.quantity ELSE 0 END), 0) - 
                COALESCE(SUM(CASE WHEN t.transaction_type = 'OUT' THEN t.quantity ELSE 0 END), 0)) as current_stock
        FROM products p
        LEFT JOIN inventory_transactions t ON p.id = t.product_id
        WHERE p.is_active = TRUE
        GROUP BY p.id, p.name, p.sku
        HAVING (COALESCE(SUM(CASE WHEN t.transaction_type = 'IN' THEN t.quantity ELSE 0 END), 0) - 
                COALESCE(SUM(CASE WHEN t.transaction_type = 'OUT' THEN t.quantity ELSE 0 END), 0)) < 20
        ORDER BY current_stock ASC
    """)
    
    result = db.session.execute(sql)
    data = [{'name': row[0], 'sku': row[1], 'stock': row[2]} for row in result]
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
    sql = text("""
        SELECT p.name, p.sku, p.unit_price, s.name as supplier
        FROM products p
        JOIN suppliers s ON p.supplier_id = s.id
        WHERE p.is_active = TRUE
        ORDER BY p.id DESC
        LIMIT 5
    """)
    
    result = db.session.execute(sql)
    data = [{'name': row[0], 'sku': row[1], 'price': float(row[2]), 'supplier': row[3]} for row in result]
    return jsonify(data), 200

@analytics_bp.route('/api/analytics/stock-by-category', methods=['GET'])
@token_required
def stock_by_category(current_user):
    sql = text("""
        SELECT 
            p.category,
            COUNT(DISTINCT p.id) as product_count,
            SUM(COALESCE(in_sum, 0) - COALESCE(out_sum, 0)) as total_units,
            SUM((COALESCE(in_sum, 0) - COALESCE(out_sum, 0)) * p.unit_price) as total_value
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
        WHERE p.is_active = TRUE
        GROUP BY p.category
        ORDER BY total_value DESC
    """)
    
    result = db.session.execute(sql)
    data = [{
        'category': row[0],
        'product_count': int(row[1]),
        'total_units': int(row[2] or 0),
        'total_value': float(row[3] or 0)
    } for row in result]
    return jsonify(data), 200

@analytics_bp.route('/api/analytics/products-by-supplier', methods=['GET'])
@token_required
def products_by_supplier(current_user):
    sql = text("""
        SELECT 
            s.name as supplier_name,
            COUNT(p.id) as product_count,
            SUM(COALESCE(in_sum, 0) - COALESCE(out_sum, 0)) as total_stock
        FROM suppliers s
        LEFT JOIN products p ON s.id = p.supplier_id AND p.is_active = TRUE
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
        GROUP BY s.id, s.name
        HAVING COUNT(p.id) > 0
        ORDER BY product_count DESC
    """)
    
    result = db.session.execute(sql)
    data = [{
        'supplier': row[0],
        'product_count': int(row[1]),
        'total_stock': int(row[2] or 0)
    } for row in result]
    return jsonify(data), 200

@analytics_bp.route('/api/analytics/stock-movement/<int:product_id>', methods=['GET'])
@token_required
def stock_movement(current_user, product_id):
    sql = text("""
        SELECT 
            t.id,
            t.transaction_date,
            t.transaction_type,
            t.quantity,
            t.notes,
            SUM(CASE 
                WHEN t2.transaction_type = 'IN' THEN t2.quantity 
                ELSE -t2.quantity 
            END) as running_stock
        FROM inventory_transactions t
        LEFT JOIN inventory_transactions t2 ON t2.product_id = t.product_id 
            AND t2.transaction_date <= t.transaction_date
            AND (t2.transaction_date < t.transaction_date OR t2.id <= t.id)
        WHERE t.product_id = :product_id
        GROUP BY t.id, t.transaction_date, t.transaction_type, t.quantity, t.notes
        ORDER BY t.transaction_date ASC, t.id ASC
    """)
    
    result = db.session.execute(sql, {'product_id': product_id})
    data = [{
        'id': row[0],
        'date': row[1].isoformat(),
        'type': row[2],
        'quantity': int(row[3]),
        'notes': row[4],
        'running_stock': int(row[5] or 0)
    } for row in result]
    return jsonify(data), 200

