from traffic_controller.signal_states import SignalState, SignalReason, SignalConfig, SignalStatus
from datetime import datetime, timedelta
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class SignalController:
    """Controls traffic signals based on vehicle compliance"""
    
    def __init__(self, config: SignalConfig = None):
        """
        Initialize signal controller
        
        Args:
            config: Signal configuration
        """
        self.config = config or SignalConfig()
        self.current_state = SignalState.RED
        self.current_reason = SignalReason.NO_VEHICLE
        self.state_start_time = datetime.now()
        self.last_status = None
        logger.info('Signal controller initialized')
    
    def control_signal(
        self,
        vehicle_type: str,
        is_compliant: bool,
        confidence: float
    ) -> SignalStatus:
        """
        Control traffic signal based on vehicle compliance
        
        Args:
            vehicle_type: Type of vehicle ('two_wheeler', 'four_wheeler', 'unknown')
            is_compliant: Whether vehicle is compliant
            confidence: Confidence of detection
            
        Returns:
            Signal status
        """
        if vehicle_type == 'unknown':
            new_state = SignalState.RED
            reason = SignalReason.NO_VEHICLE
        elif is_compliant and confidence > 0.6:
            new_state = SignalState.GREEN
            reason = SignalReason.COMPLIANT
        else:
            new_state = SignalState.RED
            reason = SignalReason.NON_COMPLIANT
        
        # Update signal if state changed
        if new_state != self.current_state:
            self.current_state = new_state
            self.current_reason = reason
            self.state_start_time = datetime.now()
            logger.info(f'Signal changed to {new_state.value} - Reason: {reason.value}')
        
        # Create status
        status = SignalStatus(new_state, reason)
        status.duration = int((datetime.now() - self.state_start_time).total_seconds())
        status.timestamp = datetime.now().isoformat()
        
        self.last_status = status
        return status
    
    def get_current_status(self) -> Dict:
        """
        Get current signal status
        
        Returns:
            Current status dictionary
        """
        if self.last_status:
            return self.last_status.to_dict()
        else:
            status = SignalStatus(self.current_state, self.current_reason)
            status.duration = int((datetime.now() - self.state_start_time).total_seconds())
            status.timestamp = datetime.now().isoformat()
            return status.to_dict()
    
    def reset_signal(self) -> SignalStatus:
        """
        Reset signal to initial state
        
        Returns:
            New signal status
        """
        self.current_state = SignalState.RED
        self.current_reason = SignalReason.NO_VEHICLE
        self.state_start_time = datetime.now()
        
        status = SignalStatus(self.current_state, self.current_reason)
        status.timestamp = datetime.now().isoformat()
        self.last_status = status
        
        logger.info('Signal reset')
        return status
    
    def manual_override(self, state: SignalState) -> SignalStatus:
        """
        Manually override signal state
        
        Args:
            state: Desired signal state
            
        Returns:
            New signal status
        """
        self.current_state = state
        self.current_reason = SignalReason.MANUAL_OVERRIDE
        self.state_start_time = datetime.now()
        
        status = SignalStatus(self.current_state, self.current_reason)
        status.timestamp = datetime.now().isoformat()
        self.last_status = status
        
        logger.warning(f'Signal manually overridden to {state.value}')
        return status
    
    def get_signal_config(self) -> Dict:
        """
        Get signal configuration
        
        Returns:
            Configuration dictionary
        """
        return self.config.to_dict()
