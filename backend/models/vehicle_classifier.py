from ultralytics import YOLO
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class VehicleClassifier:
    """Classify vehicles as 2-wheeler or 4-wheeler"""
    
    def __init__(self, model_path: str = 'yolov8n.pt', confidence: float = 0.5):
        """
        Initialize vehicle classifier
        
        Args:
            model_path: Path to YOLOv8 model
            confidence: Confidence threshold
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.vehicle_classes = {
            0: 'person',
            2: 'car',          # 4-wheeler
            3: 'motorcycle',   # 2-wheeler
            5: 'bus',          # 4+ wheeler
            7: 'truck',        # 4+ wheeler
            9: 'bicycle',      # 2-wheeler
        }
        logger.info(f'Vehicle classifier initialized with model: {model_path}')
    
    def classify(self, frame: np.ndarray) -> Dict:
        """
        Classify vehicles in frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Classification results
        """
        results = self.model(frame, conf=self.confidence)
        classifications = {
            'two_wheeler': [],
            'four_wheeler': [],
            'other': [],
            'raw_results': results
        }
        
        if results and len(results) > 0:
            boxes = results[0].boxes
            for box in boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                bbox = box.xyxy[0].cpu().numpy()
                
                detection = {
                    'class_id': class_id,
                    'class_name': self.vehicle_classes.get(class_id, 'unknown'),
                    'confidence': confidence,
                    'bbox': bbox.astype(int).tolist()
                }
                
                # Classify as 2-wheeler or 4-wheeler
                if class_id in [3, 9]:  # motorcycle, bicycle
                    classifications['two_wheeler'].append(detection)
                elif class_id in [2, 5, 7]:  # car, bus, truck
                    classifications['four_wheeler'].append(detection)
                else:
                    classifications['other'].append(detection)
        
        return classifications
    
    def get_vehicle_type(self, classification: Dict) -> str:
        """
        Get primary vehicle type from classifications
        
        Args:
            classification: Classification results
            
        Returns:
            Vehicle type string
        """
        if len(classification['four_wheeler']) > 0:
            return 'four_wheeler'
        elif len(classification['two_wheeler']) > 0:
            return 'two_wheeler'
        else:
            return 'unknown'
