import json

from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({
            "error": "Content is required"
        }), 400

    content = data["content"]

    messages = [
        {
            "role": "user",
            "content": f"""
            Based on this notification:

            {content}

            Generate 3 recommendations in JSON format.

            Example:
            [
                {{
                    "action_type": "EMAIL",
                    "description": "Send email alert",
                    "priority": "HIGH"
                }}
            ]
            """
        }
    ]

    response = call_groq(messages)

    if response is None:
        return jsonify({
            "error": "AI service unavailable",
            "is_fallback": True
        }), 500

    try:
        parsed_response = json.loads(response)

        return jsonify({
            "recommendations": parsed_response
        }), 200

    except Exception:
        return jsonify({
            "recommendations": response
        }), 200