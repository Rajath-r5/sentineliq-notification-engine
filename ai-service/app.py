from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Rate limiter — blocks any IP exceeding 30 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    storage_uri="memory://"
)

# Import routes (we will add these in Day 3+)
# from routes import describe, recommend, report

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "AI Service — Sentinel Notification Engine",
        "version": "1.0"
    }), 200

# Handle rate limit exceeded
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Maximum 30 requests per minute allowed",
        "status": 429
    }), 429

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)