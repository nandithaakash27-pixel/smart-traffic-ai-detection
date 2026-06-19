from flask import Blueprint, request, jsonify, current_app
from database.models import Vehicle, Violation, Detection, SignalLog
from traffic_controller.signal_controller import SignalController
from traffic_controller.signal_states import SignalState
from models.helmet_detector import HelmetDetector
from models.seatbelt_detector import SeatbeltDetector
from models.vehicle_classifier import VehicleClassifier
from main import db
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize detectors
helmet_detector = HelmetDetector()
seatbelt_detector = SeatbeltDetector()
vehicle_classifier = VehicleClassifier()
signal_controller = SignalController()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@api_bp.route('/detect', methods=['POST'])
def detect():
    """
    Process detection from frame
    Expected: base64 encoded image or file upload
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        # Process file with detectors
        # This is a simplified version - implement full processing as needed
        
        return jsonify({
            'status': 'detected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Detection error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/signal/status', methods=['GET'])
def get_signal_status():
    """Get current traffic signal status"""
    try:
        status = signal_controller.get_current_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f'Error getting signal status: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/signal/control', methods=['POST'])
def control_signal():
    """
    Control traffic signal
    Expected JSON: {
        'vehicle_type': 'two_wheeler' or 'four_wheeler',
        'is_compliant': boolean,
        'confidence': float
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        vehicle_type = data.get('vehicle_type')
        is_compliant = data.get('is_compliant', False)
        confidence = data.get('confidence', 0.0)
        
        status = signal_controller.control_signal(
            vehicle_type=vehicle_type,
            is_compliant=is_compliant,
            confidence=confidence
        )
        
        # Log signal change
        signal_log = SignalLog(
            state=status.state.value,
            reason=status.reason.value,
            duration=status.duration
        )
        db.session.add(signal_log)
        db.session.commit()
        
        return jsonify(status.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Signal control error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/violations', methods=['GET'])
def get_violations():
    """
    Get recent violations
    Query params: limit (default 50), offset (default 0)
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        violations = Violation.query.order_by(
            Violation.timestamp.desc()
        ).limit(limit).offset(offset).all()
        
        total = Violation.query.count()
        
        return jsonify({
            'violations': [v.to_dict() for v in violations],
            'total': total,
            'limit': limit,
            'offset': offset
        }), 200
    except Exception as e:
        logger.error(f'Error fetching violations: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get violation and compliance statistics
    Query params: days (default 7)
    """
    try:
        days = request.args.get('days', 7, type=int)
        since = datetime.utcnow() - timedelta(days=days)
        
        total_violations = Violation.query.filter(
            Violation.timestamp >= since
        ).count()
        
        helmet_violations = Violation.query.filter(
            Violation.violation_type == 'no_helmet',
            Violation.timestamp >= since
        ).count()
        
        seatbelt_violations = Violation.query.filter(
            Violation.violation_type == 'no_seatbelt',
            Violation.timestamp >= since
        ).count()
        
        compliant_detections = Detection.query.filter(
            Detection.is_compliant == True,
            Detection.timestamp >= since
        ).count()
        
        non_compliant_detections = Detection.query.filter(
            Detection.is_compliant == False,
            Detection.timestamp >= since
        ).count()
        
        total_detections = compliant_detections + non_compliant_detections
        compliance_rate = (compliant_detections / total_detections * 100) if total_detections > 0 else 0
        
        return jsonify({
            'period_days': days,
            'statistics': {
                'total_violations': total_violations,
                'helmet_violations': helmet_violations,
                'seatbelt_violations': seatbelt_violations,
                'total_detections': total_detections,
                'compliant_detections': compliant_detections,
                'non_compliant_detections': non_compliant_detections,
                'compliance_rate': round(compliance_rate, 2)
            }
        }), 200
    except Exception as e:
        logger.error(f'Error fetching statistics: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/signal/reset', methods=['POST'])
def reset_signal():
    """Reset traffic signal"""
    try:
        status = signal_controller.reset_signal()
        return jsonify(status.to_dict()), 200
    except Exception as e:
        logger.error(f'Signal reset error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/signal/override', methods=['POST'])
def override_signal():
    """
    Manually override signal state
    Expected JSON: {'state': 'red', 'green', 'yellow', or 'off'}
    """
    try:
        data = request.get_json()
        state_str = data.get('state', '').lower()
        
        state_map = {
            'red': SignalState.RED,
            'green': SignalState.GREEN,
            'yellow': SignalState.YELLOW,
            'off': SignalState.OFF
        }
        
        if state_str not in state_map:
            return jsonify({'error': f'Invalid state: {state_str}'}), 400
        
        state = state_map[state_str]
        status = signal_controller.manual_override(state)
        
        return jsonify(status.to_dict()), 200
    except Exception as e:
        logger.error(f'Signal override error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@api_bp.route('/config', methods=['GET'])
def get_config():
    """Get system configuration"""
    try:
        config = {
            'signal_config': signal_controller.get_signal_config(),
            'detection_thresholds': {
                'helmet': current_app.config.get('HELMET_CONFIDENCE_THRESHOLD', 0.6),
                'seatbelt': current_app.config.get('SEATBELT_CONFIDENCE_THRESHOLD', 0.6),
                'vehicle': current_app.config.get('VEHICLE_CONFIDENCE_THRESHOLD', 0.5)
            }
        }
        return jsonify(config), 200
    except Exception as e:
        logger.error(f'Error fetching config: {str(e)}')
        return jsonify({'error': str(e)}), 500
