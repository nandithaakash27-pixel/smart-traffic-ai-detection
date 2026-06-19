from enum import Enum
from typing import Dict

class SignalState(Enum):
    """Traffic signal states"""
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    OFF = 'off'

class SignalReason(Enum):
    """Reasons for signal state"""
    NO_VEHICLE = 'no_vehicle'
    NON_COMPLIANT = 'non_compliant'
    COMPLIANT = 'compliant'
    MANUAL_OVERRIDE = 'manual_override'
    SYSTEM_ERROR = 'system_error'

class SignalConfig:
    """Signal configuration"""
    
    def __init__(
        self,
        green_duration: int = 10,
        red_duration: int = 5,
        yellow_duration: int = 2
    ):
        self.green_duration = green_duration
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'green_duration': self.green_duration,
            'red_duration': self.red_duration,
            'yellow_duration': self.yellow_duration
        }

class SignalStatus:
    """Signal status"""
    
    def __init__(self, state: SignalState, reason: SignalReason):
        self.state = state
        self.reason = reason
        self.duration = 0
        self.timestamp = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'state': self.state.value,
            'reason': self.reason.value,
            'duration': self.duration,
            'timestamp': self.timestamp
        }
