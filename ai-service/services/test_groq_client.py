from groq_client import call_groq, parse_json_response

# Test 1 — Basic API call
print("=== Test 1: Basic Call ===")
messages = [
    {"role": "user", "content": "Reply with this exact JSON: {\"status\": \"working\", \"message\": \"GroqClient is operational\"}"}
]
response = call_groq(messages)
print("Raw response:", response)

# Test 2 — JSON parsing
print("\n=== Test 2: JSON Parsing ===")
parsed = parse_json_response(response)
if parsed:
    print("Parsed successfully:", parsed)
else:
    print("Parsing failed")

# Test 3 — Empty input handling
print("\n=== Test 3: Empty Input ===")
empty_response = call_groq([])
if empty_response is None:
    print("Empty input handled correctly — returned None")