from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Server'] = 'SentinelIQ'
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "AI Service — Sentinel Notification Engine",
        "version": "1.0"
    }), 200

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Maximum 30 requests per minute allowed",
        "status": 429
    }), 429

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)