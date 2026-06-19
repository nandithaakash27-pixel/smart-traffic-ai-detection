import cv2
import numpy as np
from typing import Tuple, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Process video frames for detection"""
    
    def __init__(self, frame_width: int = 640, frame_height: int = 480):
        """
        Initialize video processor
        
        Args:
            frame_width: Frame width
            frame_height: Frame height
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
    
    def read_frame(self, source) -> Tuple[bool, np.ndarray]:
        """
        Read frame from video source
        
        Args:
            source: Video source (webcam index, video file, or IP camera)
            
        Returns:
            Tuple of (success, frame)
        """
        try:
            if isinstance(source, str):
                # File or IP camera
                cap = cv2.VideoCapture(source)
            else:
                # Webcam index
                cap = cv2.VideoCapture(source)
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                frame = cv2.resize(frame, (self.frame_width, self.frame_height))
            
            return ret, frame
        except Exception as e:
            logger.error(f'Error reading frame: {str(e)}')
            return False, None
    
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for detection
        
        Args:
            frame: Input frame
            
        Returns:
            Preprocessed frame
        """
        # Resize
        frame = cv2.resize(frame, (self.frame_width, self.frame_height))
        
        # Normalize
        frame = frame.astype('float32') / 255.0
        
        return frame
    
    def postprocess_frame(
        self,
        frame: np.ndarray,
        detections: Dict
    ) -> np.ndarray:
        """
        Postprocess frame with annotations
        
        Args:
            frame: Input frame
            detections: Detection results
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        # Add detection info
        if 'helmet' in detections:
            helmet_count = len(detections['helmet'])
            cv2.putText(
                annotated,
                f"Helmets: {helmet_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        
        return annotated
    
    @staticmethod
    def frame_to_bytes(frame: np.ndarray) -> bytes:
        """
        Convert frame to bytes for transmission
        
        Args:
            frame: Input frame
            
        Returns:
            JPEG encoded bytes
        """
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()
    
    @staticmethod
    def bytes_to_frame(frame_bytes: bytes) -> np.ndarray:
        """
        Convert bytes to frame
        
        Args:
            frame_bytes: JPEG encoded bytes
            
        Returns:
            Frame array
        """
        nparr = np.frombuffer(frame_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
