import sys
import os
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

try:
    from groq_client import call_groq, parse_json_response
    from datetime import datetime

    print("=" * 60)
    print("PROMPT TUNING REPORT — Day 6")
    print("Sentinel Notification Engine")
    print("=" * 60)

    def load_prompt(filename):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, '..', 'prompts', filename)
        print(f"Loading: {path}")
        with open(path, 'r') as f:
            return f.read()

    print("Loading prompts...")
    describe_prompt = load_prompt('describe_prompt.txt')
    print("describe loaded OK")
    recommend_prompt = load_prompt('recommend_prompt.txt')
    print("recommend loaded OK")

    test_inputs = [
        "Server CPU usage has reached 95% on production server DB-01",
        "Scheduled maintenance window tonight from 11pm to 2am",
        "New user registration spike 500 signups in the last hour",
        "Payment gateway timeout errors increased by 40% in last 30 minutes",
        "SSL certificate for api.sentinel.com expires in 7 days",
        "Database backup failed last successful backup was 48 hours ago",
        "Security scan detected 3 failed login attempts from IP 192.168.1.105",
        "Memory usage on web server WEB-02 is at 87% capacity",
        "API response time degraded average latency increased from 200ms to 800ms",
        "Disk space on storage server is at 92% only 8GB remaining"
    ]

    def score_response(parsed, prompt_type):
        score = 0
        reasons = []

        if parsed is None:
            return 0, ["Failed to parse JSON"]

        if prompt_type == "describe":
            required = ["summary", "category", "urgency", "suggested_action", "key_points"]
            for field in required:
                if field in parsed:
                    score += 1.5
                else:
                    reasons.append(f"Missing field: {field}")
            if "key_points" in parsed and len(parsed["key_points"]) == 3:
                score += 1
            if "category" in parsed and parsed["category"] in ["Alert", "Reminder", "Update", "Warning", "Info"]:
                score += 0.5
            if "urgency" in parsed and parsed["urgency"] in ["Low", "Medium", "High", "Critical"]:
                score += 0.5

        elif prompt_type == "recommend":
            if "recommendations" in parsed:
                recs = parsed["recommendations"]
                if len(recs) == 3:
                    score += 3
                all_fields_count = 0
                for rec in recs:
                    if all(k in rec for k in ["action_type", "description", "priority"]):
                        all_fields_count += 1
                score += all_fields_count * 2
                priorities = [r.get("priority") for r in recs]
                if len(set(priorities)) > 1:
                    score += 1
            else:
                reasons.append("Missing recommendations array")

        return min(round(score), 10), reasons

    # ── TEST DESCRIBE PROMPT ───────────────────────────────
    print("\n--- DESCRIBE PROMPT TUNING (10 inputs) ---\n")
    describe_scores = []

    for i, input_text in enumerate(test_inputs):
        print(f"Testing input {i+1}...")
        prompt = describe_prompt.replace("{content}", input_text)
        prompt = prompt.replace("{generated_at}", datetime.now().isoformat())
        messages = [{"role": "user", "content": prompt}]
        response = call_groq(messages, temperature=0.3)
        parsed = parse_json_response(response)
        score, reasons = score_response(parsed, "describe")
        describe_scores.append(score)
        status = "✅" if score >= 7 else "❌"
        print(f"Input {i+1:2}: {status} Score {score}/10 — {input_text[:50]}")
        if reasons:
            for r in reasons:
                print(f"          ⚠ {r}")

    avg_describe = sum(describe_scores) / len(describe_scores)
    print(f"\nDescribe Average: {avg_describe:.1f}/10")

    # ── TEST RECOMMEND PROMPT ──────────────────────────────
    print("\n--- RECOMMEND PROMPT TUNING (10 inputs) ---\n")
    recommend_scores = []

    for i, input_text in enumerate(test_inputs):
        print(f"Testing input {i+1}...")
        prompt = recommend_prompt.replace("{content}", input_text)
        messages = [{"role": "user", "content": prompt}]
        response = call_groq(messages, temperature=0.3)
        parsed = parse_json_response(response)
        score, reasons = score_response(parsed, "recommend")
        recommend_scores.append(score)
        status = "✅" if score >= 7 else "❌"
        print(f"Input {i+1:2}: {status} Score {score}/10 — {input_text[:50]}")
        if reasons:
            for r in reasons:
                print(f"          ⚠ {r}")

    avg_recommend = sum(recommend_scores) / len(recommend_scores)
    print(f"\nRecommend Average: {avg_recommend:.1f}/10")

    # ── FINAL SUMMARY ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("TUNING SUMMARY")
    print("=" * 60)
    print(f"Describe  prompt avg : {avg_describe:.1f}/10  {'✅ Good' if avg_describe >= 7 else '❌ Needs rewrite'}")
    print(f"Recommend prompt avg : {avg_recommend:.1f}/10  {'✅ Good' if avg_recommend >= 7 else '❌ Needs rewrite'}")

    if avg_describe >= 7 and avg_recommend >= 7:
        print("\nAll prompts scoring above 7/10 ✅ Ready for Day 7")
    else:
        print("\nSome prompts need rewriting ❌ Review scores above")

except Exception as e:
    print("\nCRASH ERROR:")
    print(str(e))
    traceback.print_exc()