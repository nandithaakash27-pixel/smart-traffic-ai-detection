from ultralytics import YOLO
import cv2
import numpy as np
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)

class HelmetDetector:
    """Detect helmets on 2-wheeler riders using YOLOv8"""
    
    def __init__(self, model_path: str = 'yolov8n.pt', confidence: float = 0.6):
        """
        Initialize helmet detector
        
        Args:
            model_path: Path to YOLOv8 model
            confidence: Confidence threshold for detections
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.class_names = {
            0: 'person',
            1: 'helmet',
            2: 'no_helmet'
        }
        logger.info(f'Helmet detector initialized with model: {model_path}')
    
    def detect(self, frame: np.ndarray) -> Dict:
        """
        Detect helmets in frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Detection results dictionary
        """
        results = self.model(frame, conf=self.confidence)
        detections = {
            'helmet': [],
            'no_helmet': [],
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
                
                if class_id == 1:  # Helmet detected
                    detections['helmet'].append(detection)
                elif class_id == 2:  # No helmet
                    detections['no_helmet'].append(detection)
        
        return detections
    
    def is_helmet_compliant(self, detections: Dict) -> bool:
        """
        Check if helmet compliance is met
        
        Args:
            detections: Detection results
            
        Returns:
            True if helmet is properly worn, False otherwise
        """
        # If helmet detected and no "no_helmet" detection, compliant
        if len(detections['helmet']) > 0 and len(detections['no_helmet']) == 0:
            return True
        return False
    
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
        
        # Draw helmet detections (green)
        for det in detections['helmet']:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated_frame,
                f"Helmet {det['confidence']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
        
        # Draw no-helmet detections (red)
        for det in detections['no_helmet']:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                annotated_frame,
                f"No Helmet {det['confidence']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )
        
        return annotated_frame
