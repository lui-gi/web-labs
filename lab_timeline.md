Full Web Programming Lab Timeline
For: Cybersecurity & Bug Bounty Track

🧱 Phase 1 — How the Web Actually Works
Before writing a single line of code, you need to understand what's happening under the hood. This phase is what separates bug bounty hunters from script kiddies.
Lab 1 — How the Web Works
HTTP request/response cycle, DNS resolution, TCP/IP basics, status codes (200, 301, 404, 500), headers, cookies, and sessions. You'll use browser DevTools and Wireshark to watch real traffic as you browse.
Lab 2 — Frontend + Backend Relationship
Trace a single button click in your C compiler app all the way from index.html → fetch() → FastAPI → Lambda → back to the browser. Draw the architecture diagram yourself before verifying it.
Lab 3 — Intro to HTML/CSS/JS (No Frameworks)
Build a static webpage from scratch: a simple form that collects two numbers and displays their sum. No React, no Tailwind. Raw DOM manipulation with document.getElementById. This is what every framework abstracts — you need to see underneath it.

⚙️ Phase 2 — Backend Fundamentals
Your weakest area. This phase gets you writing and owning backend code without assistance.
Lab 4 — Intro to APIs & REST
What an API is, what REST means (stateless, resource-based URLs, HTTP verbs). Build a tiny FastAPI server with GET /hello and POST /echo from scratch. Test it with curl and Postman.
Lab 5 — FastAPI Deep Dive
Go line by line through api/main.py and api/sandbox.py. Topics: Pydantic models, field validators, routing, error handling, subprocess calls. Then rebuild a simplified version — a /compile endpoint that just runs gcc — without looking at the original.
Lab 6 — REST vs. GraphQL vs. WebSockets
REST is what you've been building. GraphQL lets clients ask for exactly the data they need (important for bug bounty recon — GraphQL introspection is a goldmine). WebSockets enable real-time two-way communication (relevant for CounterStack live threat feeds). Build a tiny example of each.
Lab 7 — Backend & API Separation
Why is sandbox.py separate from main.py in your compiler? Covers separation of concerns, layered architecture, and why business logic shouldn't live in your route handlers. You refactor a messy single-file FastAPI app into a clean layered structure.

🗄️ Phase 3 — Databases
You've used PostgreSQL before with Shelnet. This phase makes it deliberate.
Lab 8 — SQL Fundamentals
CREATE TABLE, INSERT, SELECT, WHERE, JOIN, INDEX. You design the schema for storing compiler submission history: who submitted, what code, what output, when. Run queries against it manually in psql.
Lab 9 — PostgreSQL + FastAPI Integration
Connect your FastAPI app to PostgreSQL using asyncpg or SQLAlchemy. Add a POST /submit route that saves to the DB and a GET /history route that retrieves it. No ORM magic until you've done it raw first.
Lab 10 — Auth: Sessions, JWTs, and Cookies
How do websites know who you are? Build a simple login system: register a user, hash their password with bcrypt, issue a JWT on login, protect a route with it. This is foundational for bug bounty — broken auth is OWASP #2.

🐳 Phase 4 — Containers & Infrastructure
Now that you understand what the code does, you'll understand what Docker and AWS are actually abstracting.
Lab 11 — Docker
Read your compiler's Dockerfile and docker-compose.yml line by line. Then write one from scratch for your FastAPI app. Topics: images vs. containers, layers, volumes, networking between containers, environment variables.
Lab 12 — AWS Lambda
Go line by line through lambda/handler.py. Understand cold starts, execution environments, the event object, and timeout behavior. Deploy a hello-world Lambda manually through the AWS console — no CDK, no Terraform, just you and the UI first.
Lab 13 — AWS Ecosystem
S3 (file storage), IAM (permissions — critical for cloud pentesting), API Gateway (how Lambda gets an HTTP interface), CloudWatch (logs). Set up a simple architecture: API Gateway → Lambda → S3.

🔐 Phase 5 — Web Security (Where It All Connects)
This is why you learned everything above. Each lab here maps directly to OWASP Top 10 and bug bounty targets.
Lab 14 — OWASP Top 10 Overview
Map every vulnerability in the Top 10 to what you've built: where would SQL injection hit your DB schema? Where would broken auth hit your JWT lab? Where would SSRF hit your Lambda sandbox? This lab is a threat model of your own projects.
Lab 15 — XSS (Cross-Site Scripting)
Stored, reflected, and DOM-based XSS. Build a vulnerable comment box, exploit it, then patch it. Understand Content Security Policy headers and why output encoding matters.
Lab 16 — SQL Injection
Build a vulnerable login form, exploit it manually (no sqlmap yet), then patch it with parameterized queries. Then use sqlmap to automate what you just did by hand.
Lab 17 — IDOR & Broken Access Control
Build an API with user-specific resources (/api/submissions/1), then demonstrate how incrementing that ID gives you another user's data. IDOR is the #1 bug bounty finding. Patch it with proper authorization checks.
Lab 18 — SSRF (Server-Side Request Forgery)
Especially relevant since your Lambda sandbox executes code and makes outbound calls. Demonstrate how a malicious payload could make your server fetch internal AWS metadata endpoints. This is a critical cloud vulnerability.
Lab 19 — JWT Attacks
Since you implemented JWTs in Lab 10, now attack them. Algorithm confusion (alg: none), weak secrets, and signature stripping. Use jwt_tool to test your own implementation.
Lab 20 — API Security & Recon
GraphQL introspection queries, finding hidden endpoints with ffuf/feroxbuster, reading API docs to find undocumented parameters, testing for mass assignment vulnerabilities. This is your bug bounty workflow lab.

🚀 Phase 6 — Capstone
Build something real that ties every phase together.
Lab 21 — Capstone: Build & Break a Fullstack App
Build a small fullstack app (a note-taking API with auth and a simple frontend) entirely without Claude Code. Then switch hats — pentest it using everything from Phase 5. Write a vulnerability report in the format bug bounty platforms expect (HackerOne style). This goes directly on your resume and Shelnet.
