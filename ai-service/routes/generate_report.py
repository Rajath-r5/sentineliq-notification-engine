from flask import Blueprint, request, jsonify
from services.groq_client import call_groq

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

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
            Generate a professional notification report for:

            {content}

            Include:
            - title
            - summary
            - overview
            - key findings
            - recommendations

            Return clean readable text.
            """
        }
    ]

    response = call_groq(messages)

    if response is None:
        return jsonify({
            "error": "AI service unavailable",
            "is_fallback": True
        }), 500

    return jsonify({
        "report": response
    }), 200