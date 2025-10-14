from flask import request, jsonify
from functools import wraps
import yaml

# Load token from config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
AUTH_TOKEN = config['app'].get('auth_token', 'mysecrettoken')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f'Bearer {AUTH_TOKEN}':
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated
