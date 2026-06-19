import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('traffic_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import models and routes
from database.models import Vehicle, Violation, Detection
from api.routes import api_bp
from traffic_controller.signal_controller import SignalController

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize signal controller
signal_controller = SignalController()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Vehicle': Vehicle,
        'Violation': Violation,
        'Detection': Detection
    }

@app.before_request
def before_request():
    """Before request hook"""
    pass

@app.after_request
def after_request(response):
    """After request hook"""
    response.headers['X-Powered-By'] = 'Smart Traffic AI'
    return response

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Resource not found'}, 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f'Server error: {error}')
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        logger.info('Database tables created')
        
        # Run the app
        port = int(os.getenv('PORT', 5000))
        app.run(
            host='0.0.0.0',
            port=port,
            debug=app.config['DEBUG'],
            use_reloader=False
        )
