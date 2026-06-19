from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import db

class Vehicle(db.Model):
    """Vehicle model"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False, index=True)
    vehicle_type = db.Column(db.String(20), nullable=False)  # two_wheeler, four_wheeler
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    violations = db.relationship('Violation', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    detections = db.relationship('Detection', backref='vehicle', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'license_plate': self.license_plate,
            'vehicle_type': self.vehicle_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Violation(db.Model):
    """Violation model"""
    __tablename__ = 'violations'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False, index=True)
    violation_type = db.Column(db.String(50), nullable=False)  # no_helmet, no_seatbelt
    severity = db.Column(db.String(20), default='high')  # low, medium, high
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_resolved = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'violation_type': self.violation_type,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat(),
            'is_resolved': self.is_resolved,
            'notes': self.notes
        }

class Detection(db.Model):
    """Detection model"""
    __tablename__ = 'detections'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True, index=True)
    detection_type = db.Column(db.String(50), nullable=False)  # helmet, seatbelt
    is_compliant = db.Column(db.Boolean, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    signal_state = db.Column(db.String(20), nullable=False)  # red, green, yellow
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    frame_data = db.Column(db.LargeBinary)  # Optional: store frame image
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'detection_type': self.detection_type,
            'is_compliant': self.is_compliant,
            'confidence': self.confidence,
            'signal_state': self.signal_state,
            'timestamp': self.timestamp.isoformat()
        }

class SignalLog(db.Model):
    """Signal state change log"""
    __tablename__ = 'signal_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)  # seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'reason': self.reason,
            'duration': self.duration,
            'timestamp': self.timestamp.isoformat()
        }
