from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from config.logging import setup_logging

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging(app)
    db.init_app(app)

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.suppliers import suppliers_bp
    from app.routes.transactions import transactions_bp
    from app.routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(analytics_bp)

    return app
