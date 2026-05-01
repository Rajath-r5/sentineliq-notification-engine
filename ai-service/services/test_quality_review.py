import sys
import os
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from groq_client import call_groq, parse_json_response
    from datetime import datetime

    print("=" * 60)
    print("WEEK 2 AI QUALITY REVIEW — Day 10")
    print("Sentinel Notification Engine")
    print("Target: Average >= 4/5 per endpoint")
    print("=" * 60)

    def load_prompt(filename):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, '..', 'prompts', filename)
        with open(path, 'r') as f:
            return f.read()

    describe_prompt = load_prompt('describe_prompt.txt')
    recommend_prompt = load_prompt('recommend_prompt.txt')
    report_prompt = load_prompt('report_prompt.txt')

    # 10 fresh inputs — different from Day 6
    fresh_inputs = [
        "Critical alert — database connection pool exhausted on DB-02",
        "User password reset requests increased by 300% in last hour",
        "Scheduled backup job failed for third consecutive night",
        "New deployment to production environment failed at step 3",
        "Email notification service is returning 503 errors",
        "Unauthorized access attempt detected on admin panel",
        "System clock drift detected on server PROD-01 — 5 minutes ahead",
        "Storage quota exceeded for user uploads — 100GB limit reached",
        "Third party payment API returning intermittent 408 timeouts",
        "CPU temperature on server RACK-03 reached critical threshold 90C"
    ]

    def score_describe(parsed):
        if parsed is None:
            return 0
        score = 0
        required = ["summary", "category", "urgency", "suggested_action", "key_points"]
        for field in required:
            if field in parsed:
                score += 0.6
        if "key_points" in parsed and len(parsed["key_points"]) == 3:
            score += 0.5
        if "urgency" in parsed and parsed["urgency"] in ["Low", "Medium", "High", "Critical"]:
            score += 0.5
        if "category" in parsed and parsed["category"] in ["Alert", "Reminder", "Update", "Warning", "Info"]:
            score += 0.5
        return min(round(score * 10) / 10, 5)

    def score_recommend(parsed):
        if parsed is None:
            return 0
        score = 0
        if "recommendations" in parsed:
            recs = parsed["recommendations"]
            if len(recs) == 3:
                score += 2
            for rec in recs:
                if all(k in rec for k in ["action_type", "description", "priority"]):
                    score += 0.8
            priorities = [r.get("priority") for r in recs]
            if len(set(priorities)) > 1:
                score += 0.6
        return min(round(score * 10) / 10, 5)

    def score_report(parsed):
        if parsed is None:
            return 0
        score = 0
        required = ["title", "summary", "overview", "key_items", "recommendations"]
        for field in required:
            if field in parsed:
                score += 0.6
        if "key_items" in parsed and 3 <= len(parsed["key_items"]) <= 5:
            score += 0.8
        if "recommendations" in parsed and len(parsed["recommendations"]) == 3:
            score += 0.6
        return min(round(score * 10) / 10, 5)


    # ── TEST DESCRIBE ──────────────────────────────────────
    print("\n--- DESCRIBE ENDPOINT (10 fresh inputs) ---\n")
    describe_scores = []

    for i, input_text in enumerate(fresh_inputs):
        prompt = describe_prompt.replace("{content}", input_text)
        prompt = prompt.replace("{generated_at}", datetime.now().isoformat())
        messages = [{"role": "user", "content": prompt}]
        response = call_groq(messages, temperature=0.3)
        parsed = parse_json_response(response)
        score = score_describe(parsed)
        describe_scores.append(score)
        status = "✅" if score >= 4 else "❌"
        print(f"Input {i+1:2}: {status} Score {score}/5 — {input_text[:50]}")

    avg_describe = sum(describe_scores) / len(describe_scores)
    print(f"\nDescribe Average: {avg_describe:.1f}/5 {'✅' if avg_describe >= 4 else '❌'}")


    # ── TEST RECOMMEND ────────────────────────────────────
    print("\n--- RECOMMEND ENDPOINT (10 fresh inputs) ---\n")
    recommend_scores = []

    for i, input_text in enumerate(fresh_inputs):
        prompt = recommend_prompt.replace("{content}", input_text)
        messages = [{"role": "user", "content": prompt}]
        response = call_groq(messages, temperature=0.3)
        parsed = parse_json_response(response)
        score = score_recommend(parsed)
        recommend_scores.append(score)
        status = "✅" if score >= 4 else "❌"
        print(f"Input {i+1:2}: {status} Score {score}/5 — {input_text[:50]}")

    avg_recommend = sum(recommend_scores) / len(recommend_scores)
    print(f"\nRecommend Average: {avg_recommend:.1f}/5 {'✅' if avg_recommend >= 4 else '❌'}")


    # ── TEST REPORT ───────────────────────────────────────
    print("\n--- REPORT ENDPOINT (1 combined input) ---\n")
    report_scores = []

    report_inputs = [
        "Multiple critical alerts detected: DB connection pool exhausted, email service returning 503, CPU temperature critical on RACK-03",
        "Security incident summary: 3 unauthorized access attempts on admin panel, password reset spike of 300%, system clock drift detected",
        "Infrastructure report: Backup job failed 3 consecutive nights, deployment failed at step 3, storage quota exceeded"
    ]

    for i, input_text in enumerate(report_inputs):
        prompt = report_prompt.replace("{content}", input_text)
        prompt = prompt.replace("{generated_at}", datetime.now().isoformat())
        messages = [{"role": "user", "content": prompt}]
        response = call_groq(messages, temperature=0.3, max_tokens=1500)
        parsed = parse_json_response(response)
        score = score_report(parsed)
        report_scores.append(score)
        status = "✅" if score >= 4 else "❌"
        print(f"Input {i+1}: {status} Score {score}/5 — {input_text[:50]}")

    avg_report = sum(report_scores) / len(report_scores)
    print(f"\nReport Average: {avg_report:.1f}/5 {'✅' if avg_report >= 4 else '❌'}")


    # ── FINAL SUMMARY ─────────────────────────────────────
    print("\n" + "=" * 60)
    print("WEEK 2 AI QUALITY REVIEW SUMMARY")
    print("=" * 60)
    print(f"Describe  avg : {avg_describe:.1f}/5  {'✅ Passed' if avg_describe >= 4 else '❌ Needs fix'}")
    print(f"Recommend avg : {avg_recommend:.1f}/5  {'✅ Passed' if avg_recommend >= 4 else '❌ Needs fix'}")
    print(f"Report    avg : {avg_report:.1f}/5  {'✅ Passed' if avg_report >= 4 else '❌ Needs fix'}")

    all_passed = avg_describe >= 4 and avg_recommend >= 4 and avg_report >= 4
    if all_passed:
        print("\nAll endpoints passing quality review ✅")
        print("Week 2 AI Quality Review COMPLETE — Ready for Week 3")
    else:
        print("\nSome endpoints need fixing ❌")

except Exception as e:
    print("\nCRASH ERROR:")
    print(str(e))
    traceback.print_exc()