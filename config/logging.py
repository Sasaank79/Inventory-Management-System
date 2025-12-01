import logging
import sys


def setup_logging(app):
    log_level = logging.INFO if app.config.get('FLASK_ENV') == 'production' else logging.DEBUG
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    app.logger.setLevel(log_level)
    app.logger.addHandler(console_handler)
    
    if not app.debug:
        app.logger.info('Inventory Management System startup')
