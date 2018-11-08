"""
Log Processing REST API
Provides endpoints for log analysis and metrics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Log Processing API',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/v1/logs/search', methods=['POST'])
def search_logs():
    """
    Search logs with filters
    
    Request body:
    {
        "query": "error",
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-31T23:59:59",
        "log_level": "ERROR",
        "limit": 100
    }
    """
    try:
        data = request.get_json()
        
        # In production, query from Elasticsearch
        results = {
            'total': 1234,
            'logs': [
                {
                    'timestamp': '2024-01-15T10:30:45',
                    'level': 'ERROR',
                    'message': 'Connection timeout',
                    'logger': 'com.app.service'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error searching logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/v1/metrics/summary', methods=['GET'])
def get_metrics_summary():
    """Get log metrics summary"""
    try:
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        # In production, query from processed metrics
        summary = {
            'total_logs': 1500000,
            'error_count': 2500,
            'error_rate': 0.17,
            'avg_response_time': 245.5,
            'top_errors': [
                {'type': 'ConnectionError', 'count': 850},
                {'type': 'NullPointerException', 'count': 620}
            ]
        }
        
        return jsonify({
            'success': True,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/v1/security/events', methods=['GET'])
def get_security_events():
    """Get security events"""
    try:
        severity = request.args.get('severity', 'all')
        
        events = {
            'total': 45,
            'events': [
                {
                    'timestamp': '2024-01-15T14:22:10',
                    'type': 'failed_login',
                    'severity': 'high',
                    'ip': '192.168.1.100',
                    'details': 'Multiple failed login attempts'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'events': events,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error getting security events: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
