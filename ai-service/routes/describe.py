from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():

    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({
            "error": "Content is required"
        }), 400

    content = data["content"]

    messages = [
        {
            "role": "user",
            "content": f"Generate a short notification description for: {content}"
        }
    ]

    response = call_groq(messages)
    


    response = response.strip('"')

    if response is None:
        return jsonify({
            "error": "AI service unavailable",
            "is_fallback": True
        }), 500

    return jsonify({
        "description": response
    }), 200