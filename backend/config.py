import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///traffic_ai.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Detection Settings
    HELMET_CONFIDENCE_THRESHOLD = 0.6
    SEATBELT_CONFIDENCE_THRESHOLD = 0.6
    VEHICLE_CONFIDENCE_THRESHOLD = 0.5
    
    # Signal Control
    GREEN_LIGHT_DURATION = 10  # seconds
    RED_LIGHT_DURATION = 5     # seconds
    
    # Video Processing
    VIDEO_SOURCE = 0  # 0 for webcam, or path to video file
    FRAME_SKIP = 2    # Process every nth frame
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 30

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Detection Settings
    HELMET_CONFIDENCE_THRESHOLD = 0.75
    SEATBELT_CONFIDENCE_THRESHOLD = 0.75
    VEHICLE_CONFIDENCE_THRESHOLD = 0.65
    
    # Signal Control
    GREEN_LIGHT_DURATION = 15
    RED_LIGHT_DURATION = 8
    
    # Video Processing
    VIDEO_SOURCE = 'rtsp://camera-ip:554/stream'  # IP camera
    FRAME_SKIP = 1
    FRAME_WIDTH = 1280
    FRAME_HEIGHT = 720
    FPS = 30

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Load config based on environment
env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    config = ProductionConfig()
elif env == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
