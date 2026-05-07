Good morning, I am AI Developer 2 on the SentinelIQ team.
My responsibility was building the AI brain of this application.
Let me show you three things — what the AI does, how it works, and how we secured it.
I am now clicking the AI Recommend button on this notification.
Watch what happens — the AI reads the notification and returns three recommendations in under 2 seconds.
Each recommendation has an action type, a description, and a priority level.
This saves the team from manually deciding what to do next — the AI does it automatically.
Now I will click Generate Report.
This takes multiple notifications and combines them into a professional executive report.
The report has a title, summary, key findings with severity, and recommendations.
This is what a manager would read at end of day — generated in seconds.
Let me explain the technology behind this.
We use Groq's API to access LLaMA-3.3-70b — one of the fastest models available today.
We built three custom prompt templates — describe, recommend, and generate report.
Each prompt scored above 4.5 out of 5 in our quality review.
The AI service runs as a Docker container on port 5000.
Every input goes through our sanitiser before reaching the AI.
It strips HTML and blocks prompt injection using pattern matching.
We rate limit to 30 requests per minute to prevent API abuse.
OWASP ZAP scan — zero Critical, zero High findings.
Describe scored 4.5/5, Recommend 5/5, Report 4.4/5 — all above target.
That completes the AI demonstration — happy to answer questions.