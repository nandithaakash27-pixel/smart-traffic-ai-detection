const API_BASE_URL = 'http://localhost:5000/api';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Smart Traffic AI System Loaded');
    updateSignalStatus();
    loadStatistics();
    loadViolations();
    
    // Refresh every 5 seconds
    setInterval(() => {
        updateSignalStatus();
    }, 5000);
    
    setInterval(() => {
        loadStatistics();
        loadViolations();
    }, 30000);
});

/**
 * Update traffic signal status
 */
async function updateSignalStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/signal/status`);
        const data = await response.json();
        
        // Update signal light
        const signalLight = document.getElementById('signalLight');
        signalLight.className = `signal-light ${data.state}`;
        
        // Update status text
        document.getElementById('signalState').textContent = 
            `Signal: ${data.state.toUpperCase()}`;
        document.getElementById('signalReason').textContent = 
            `Reason: ${data.reason.replace('_', ' ').toUpperCase()}`;
    } catch (error) {
        console.error('Error updating signal status:', error);
        document.getElementById('signalState').textContent = 'Error loading status';
    }
}

/**
 * Test detection with vehicle type and compliance
 */
async function testDetection(vehicleType, isCompliant) {
    try {
        const response = await fetch(`${API_BASE_URL}/signal/control`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                vehicle_type: vehicleType,
                is_compliant: isCompliant,
                confidence: 0.95
            })
        });
        
        const data = await response.json();
        console.log('Detection result:', data);
        updateSignalStatus();
        
        // Show notification
        const message = isCompliant ? '✓ Compliant Vehicle Detected' : '✗ Non-Compliant Vehicle Detected';
        showNotification(message, isCompliant ? 'success' : 'danger');
    } catch (error) {
        console.error('Error in detection:', error);
        showNotification('Error in detection', 'danger');
    }
}

/**
 * Load statistics
 */
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics?days=7`);
        const data = await response.json();
        const stats = data.statistics;
        
        document.getElementById('totalViolations').textContent = stats.total_violations;
        document.getElementById('helmetViolations').textContent = stats.helmet_violations;
        document.getElementById('seatbeltViolations').textContent = stats.seatbelt_violations;
        document.getElementById('complianceRate').textContent = `${stats.compliance_rate}%`;
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

/**
 * Load recent violations
 */
async function loadViolations() {
    try {
        const response = await fetch(`${API_BASE_URL}/violations?limit=10`);
        const data = await response.json();
        
        const tbody = document.getElementById('violationsBody');
        tbody.innerHTML = '';
        
        if (data.violations.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No violations</td></tr>';
            return;
        }
        
        data.violations.forEach(violation => {
            const row = document.createElement('tr');
            const date = new Date(violation.timestamp).toLocaleString();
            const violationType = violation.violation_type.replace('_', ' ').toUpperCase();
            const severityColor = violation.severity === 'high' ? '#e74c3c' : 
                                 violation.severity === 'medium' ? '#f39c12' : '#3498db';
            
            row.innerHTML = `
                <td>${date}</td>
                <td>${violationType}</td>
                <td><span style="color: ${severityColor}; font-weight: bold;">${violation.severity.toUpperCase()}</span></td>
                <td>${violation.is_resolved ? '✓ Resolved' : 'Pending'}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading violations:', error);
    }
}

/**
 * Control signal state
 */
async function controlSignal(state) {
    try {
        const response = await fetch(`${API_BASE_URL}/signal/override`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ state: state })
        });
        
        const data = await response.json();
        console.log('Signal control result:', data);
        updateSignalStatus();
        showNotification(`Signal set to ${state.toUpperCase()}`, 'success');
    } catch (error) {
        console.error('Error controlling signal:', error);
        showNotification('Error controlling signal', 'danger');
    }
}

/**
 * Reset signal
 */
async function resetSignal() {
    try {
        const response = await fetch(`${API_BASE_URL}/signal/reset`, {
            method: 'POST'
        });
        
        const data = await response.json();
        console.log('Signal reset result:', data);
        updateSignalStatus();
        showNotification('Signal reset successfully', 'success');
    } catch (error) {
        console.error('Error resetting signal:', error);
        showNotification('Error resetting signal', 'danger');
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#27ae60' : type === 'danger' ? '#e74c3c' : '#3498db'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
