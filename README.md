# AI Service — SentinelIQ Notification Engine
## Tool-80 | AI Developer 2 | Sprint: 14 April – 9 May 2026

---

## Overview

The AI service is a Flask microservice that provides three AI-powered endpoints for the SentinelIQ Notification Engine. It uses Groq's LLaMA-3.3-70b model to describe notifications, recommend actions, and generate executive reports.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Language |
| Flask 3.x | Web framework |
| Groq API | AI model — LLaMA-3.3-70b |
| flask-limiter | Rate limiting — 30 req/min |
| bleach | HTML sanitisation |
| Docker | Containerisation |

---

## Prerequisites

- Python 3.11+
- Docker Desktop
- Groq API key — get free at console.groq.com

---

## Setup Instructions

### Option 1 — Run with Docker (Recommended)

Step 1 — Clone the repo:

    git clone https://github.com/Rajath-r5/sentineliq-notification-engine.git
    cd sentineliq-notification-engine

Step 2 — Create .env file in ai-service folder:

    cd ai-service

Create a file called .env and add:

    GROQ_API_KEY=your_groq_api_key_here

Step 3 — Build and run:

    cd ..
    docker-compose up --build

Step 4 — Verify running:

    curl http://localhost:5000/health

---

### Option 2 — Run locally

Step 1 — Install dependencies:

    cd ai-service
    pip install -r requirements.txt

Step 2 — Create .env file:

    GROQ_API_KEY=your_groq_api_key_here

Step 3 — Run:

    python app.py

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| GROQ_API_KEY | Groq API key from console.groq.com | Yes |

---

## API Reference

### GET /health
Check if the AI service is running.

Response:
    {
        "status": "ok",
        "service": "AI Service — Sentinel Notification Engine",
        "version": "1.0"
    }

---

### POST /describe
Analyse a notification and return structured description.

Request:
    {
        "content": "Server CPU usage has reached 95% on DB-01"
    }

Response:
    {
        "summary": "Critical CPU spike on DB-01",
        "category": "Alert",
        "urgency": "Critical",
        "suggested_action": "Scale up server resources immediately",
        "key_points": [
            "CPU at 95% on production server DB-01",
            "Risk of outage if not addressed",
            "Immediate action required"
        ],
        "generated_at": "2026-05-03T10:00:00"
    }

---

### POST /recommend
Get 3 AI recommendations for a notification.

Request:
    {
        "content": "SSL certificate expires in 7 days"
    }

Response:
    {
        "recommendations": [
            {
                "action_type": "Resolve",
                "description": "Renew SSL certificate immediately",
                "priority": "High"
            },
            {
                "action_type": "Schedule",
                "description": "Set up auto-renewal",
                "priority": "Medium"
            },
            {
                "action_type": "Monitor",
                "description": "Add 30-day expiry alert",
                "priority": "Low"
            }
        ]
    }

---

### POST /generate-report
Generate executive report from notifications.

Request:
    {
        "content": "Multiple issues: CPU critical, SSL expiring, payment timeouts"
    }

Response:
    {
        "title": "Weekly Infrastructure Report",
        "summary": "Three critical issues detected this week",
        "overview": "Detailed overview of all incidents...",
        "key_items": [
            {"item": "CPU critical on DB-01", "severity": "Critical"},
            {"item": "SSL expiring in 7 days", "severity": "High"},
            {"item": "Payment timeouts up 40%", "severity": "High"}
        ],
        "recommendations": [
            {"action": "Scale DB-01 immediately", "priority": "High"},
            {"action": "Renew SSL today", "priority": "High"},
            {"action": "Investigate payment gateway", "priority": "Medium"}
        ],
        "generated_at": "2026-05-03T10:00:00"
    }

---

## Security Features

| Feature | Implementation |
|---|---|
| Input sanitisation | bleach strips HTML |
| Prompt injection detection | 10+ patterns blocked |
| Rate limiting | 30 req/min per IP |
| Security headers | 7 headers on all responses |
| Server version hidden | Server: SentinelIQ |
| Debug mode | Disabled in production |

---

## Running Tests

    cd ai-service/services
    python test_security.py
    python test_prompt_tuning.py
    python test_quality_review.py
    python test_week2_signoff.py

    cd ../..
    pytest test_ai_service.py -v

---

## Test Results

| Test Suite | Result |
|---|---|
| Security tests | 15/15 passing |
| Pytest unit tests | 8/8 passing |
| Week 2 sign-off | 13/13 passing |
| Prompt tuning | 10/10 both prompts |
| AI quality review | 4.4 to 5.0 out of 5 all endpoints |

---

## Folder Structure

    ai-service/
    ├── prompts/
    │   ├── describe_prompt.txt
    │   ├── recommend_prompt.txt
    │   └── report_prompt.txt
    ├── routes/
    ├── services/
    │   ├── groq_client.py
    │   ├── sanitiser.py
    │   ├── test_groq_client.py
    │   ├── test_prompt_tuning.py
    │   ├── test_quality_review.py
    │   ├── test_security.py
    │   └── test_week2_signoff.py
    ├── .env
    ├── app.py
    ├── Dockerfile
    ├── README.md
    └── requirements.txt

---

## AI Quality Scores

| Endpoint | Score | Target |
|---|---|---|
| /describe | 4.5/5 | 4/5 |
| /recommend | 5.0/5 | 4/5 |
| /generate-report | 4.4/5 | 4/5 |

---

AI Developer 2 — SentinelIQ Notification Engine
Sprint: 14 April – 9 May 2026