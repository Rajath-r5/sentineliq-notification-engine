from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Import route blueprints
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import report_bp

# Create Flask app
app = Flask(__name__)

# Register all routes
app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(report_bp)

# Rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

# Security headers
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

# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "AI Service — Sentinel Notification Engine",
        "version": "1.0"
    }), 200

# 429 Rate limit handler
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Maximum 30 requests per minute allowed",
        "status": 429
    }), 429

# 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "status": 404
    }), 404

# 500 handler
@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)