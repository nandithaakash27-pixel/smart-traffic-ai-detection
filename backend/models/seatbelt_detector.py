from ultralytics import YOLO
import cv2
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class SeatbeltDetector:
    """Detect seatbelts on 4-wheeler drivers using YOLOv8"""
    
    def __init__(self, model_path: str = 'yolov8n.pt', confidence: float = 0.6):
        """
        Initialize seatbelt detector
        
        Args:
            model_path: Path to YOLOv8 model
            confidence: Confidence threshold for detections
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.class_names = {
            0: 'person',
            1: 'seatbelt',
            2: 'no_seatbelt'
        }
        logger.info(f'Seatbelt detector initialized with model: {model_path}')
    
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Detect seatbelts in frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Detection results dictionary
        """
        results = self.model(frame, conf=self.confidence)
        detections = {
            'seatbelt': [],
            'no_seatbelt': [],
            'frame': frame,
            'raw_results': results
        }
        
        if results and len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                bbox = box.xyxy[0].cpu().numpy()
                
                detection = {
                    'bbox': bbox.astype(int).tolist(),
                    'confidence': confidence,
                    'class_id': class_id
                }
                
                if class_id == 1:  # Seatbelt detected
                    detections['seatbelt'].append(detection)
                elif class_id == 2:  # No seatbelt
                    detections['no_seatbelt'].append(detection)
        
        return detections
    
    def is_seatbelt_compliant(self, detections: Dict) -> bool:
        """
        Check if seatbelt compliance is met
        
        Args:
            detections: Detection results
            
        Returns:
            True if seatbelt is properly worn, False otherwise
        """
        # For 4+ wheeler, all visible passengers should have seatbelts
        if len(detections['seatbelt']) > 0 and len(detections['no_seatbelt']) == 0:
            return True
        return False
    
    def check_all_seats_compliant(self, detections: Dict) -> Dict:
        """
        Check compliance for all seats
        
        Args:
            detections: Detection results
            
        Returns:
            Compliance details
        """
        total_people = len(detections['seatbelt']) + len(detections['no_seatbelt'])
        compliant_people = len(detections['seatbelt'])
        non_compliant_people = len(detections['no_seatbelt'])
        
        return {
            'total_people': total_people,
            'compliant': compliant_people,
            'non_compliant': non_compliant_people,
            'is_fully_compliant': non_compliant_people == 0 and total_people > 0
        }
    
    def draw_detections(self, frame: np.ndarray, detections: Dict) -> np.ndarray:
        """
        Draw detection boxes on frame
        
        Args:
            frame: Input frame
            detections: Detection results
            
        Returns:
            Annotated frame
        """
        annotated_frame = frame.copy()
        
        # Draw seatbelt detections (green)
        for det in detections['seatbelt']:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated_frame,
                f"Seatbelt {det['confidence']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        # Draw no-seatbelt detections (red)
        for det in detections['no_seatbelt']:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                annotated_frame,
                f"No Seatbelt {det['confidence']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )
        
        return annotated_frame
