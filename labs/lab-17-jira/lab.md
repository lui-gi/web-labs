# Lab 17 — Jira Service Management Fundamentals

**Phase:** 5 | **Estimated time:** ~60 min | **Type:** Hands-on

**Tools required:** Web browser (no install needed) — open `starter/index.html` directly

---

## Overview

You are 30 minutes from your first day on the IT service desk. Every ticket that comes
in will land in Jira Service Management (JSM), and your team will expect you to triage,
assign, and update tickets from the moment you sit down. This lab gives you enough
hands-on JSM experience to participate in your first standup and work your first ticket
without hesitation — using a pre-built simulation that runs entirely in your browser.

JSM is the tool that makes IT operations visible and accountable. Without it, work lives
in email threads, Slack DMs, and people's heads — impossible to prioritize, track, or
report on. Understanding it from day one is not optional for an IT ops role.

After this lab, you will be able to:
- Identify the four JSM ticket types (Incident, Service Request, Problem, Change) and
  classify a real user report into the correct type
- Read a JSM queue and explain what each column means, including SLA breach indicators
- Assign, triage, and update a ticket through its lifecycle
- Create a well-formed ticket from a raw user report

---

## Prerequisites

- [ ] Lab 16 complete (or general familiarity with web browser operation)
- [ ] Tools installed:
  - Any modern web browser (Chrome, Firefox, Edge, Safari)
- [ ] No accounts, no install, no server — open `starter/index.html` directly in your browser

---

## Concepts

### 2.1 Ticket Types in JSM

JSM uses four ticket types, each inherited from the **ITIL framework** — the industry
standard for IT service management that most enterprise IT orgs follow.

**Incident** — an unplanned disruption to a service or a degradation in quality.
Something broke. The laptop won't turn on. The VPN is rejecting logins. The app is
returning 500 errors. The defining characteristic: nobody planned this, and a user
is affected right now.

**Service Request** — a planned fulfillment of a standard need. Someone needs something,
not because something is broken, but because they want or need a new resource. New
software license, access to a shared drive, a password reset for a locked account. The
defining characteristic: it is a predictable, repeatable ask with a known fulfillment
process.

**Problem** — the underlying root cause behind one or more incidents. If the same
printer breaks three times in a month, each break is an Incident, but the fact that
the printer keeps breaking is a Problem. Problem tickets trigger root-cause investigation
to prevent future incidents — not just to fix this one.

**Change** — a planned modification to infrastructure, configuration, or services. OS
upgrades, firewall rule changes, server migrations. Changes go through an approval
process and usually have a maintenance window. The goal is to prevent changes from
creating new incidents.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A user calls to report their laptop won't turn on. Is that an Incident or
a Service Request? Why?

**Answer:** Incident. The laptop is broken — an unplanned disruption that a user is
experiencing right now. A Service Request would be something like "I need a new laptop
for a new hire starting Monday" — a planned, predictable ask with no failure involved.
The key test: did something break unexpectedly, or is someone asking for something they
don't yet have?

</details>

---

### 2.2 The Ticket Lifecycle and SLAs

A ticket moves through statuses that represent where it is in the resolution process.
In the simulation you will see these states:

- **WAITING FOR SUPPORT** — ticket is open and unassigned (or assigned but not yet
  acknowledged). The clock is ticking.
- **IN PROGRESS** — an agent has acknowledged the ticket and is actively working it.
- **WORK IN PROGRESS** — extended active work, often used to signal ongoing investigation
  or implementation.
- **UNDER REVIEW** — a solution has been proposed and is being verified.
- **WAITING FOR APPROVAL** — the resolution requires sign-off (common for Changes).
- **Resolved / Closed** — the issue is fixed and the user has confirmed it (or a timeout
  has passed). (Note: the simulation does not include a Resolved or Closed state — those
  appear in a real JSM instance after the customer confirms the issue is fixed.)

**SLA (Service Level Agreement)** is a time-bound commitment between the IT team and
the business. A common SLA: "P2 Incidents will receive a first response within 4 hours
and be resolved within 8 hours." JSM tracks these automatically with countdown timers.

When the timer reaches zero, the SLA is **breached**. The timer turns red and displays
negative time (e.g., `-15m`). A breached SLA means the team failed to meet its
commitment — which has contractual, operational, and trust implications. Teams are
measured on SLA compliance in weekly and monthly reports.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** The SLA on ITSM-1324 shows `-15m` in red. What does that mean for the
IT team and why does it matter?

**Answer:** The IT team committed to responding to (or resolving) this ticket within
a specific time window, and that window expired 15 minutes ago. This is a breach. It
matters because SLA compliance is tracked and reported — managers, customers, and
leadership review it. Repeated breaches indicate understaffing, poor triage, or process
problems. On a personal level, unacknowledged breached tickets are the first thing a
team lead will ask about in standup.

</details>

---

### 2.3 Queues and Triage

A **queue** in JSM is a filtered, sorted list of tickets for a specific team or role.
Instead of every agent seeing every ticket in the system, queues surface only the work
that is relevant — "all open P1s", "all tickets assigned to my team", "all breached
SLAs". Queues are configured by admins but used by every agent, every day.

**Triage** is the process of deciding what to work in what order. IT ops triage is
driven by two factors in combination:

1. **Priority (P1–P4):** P1 = critical, service-down, revenue-impacting. P2 = high,
   major impact to one user or minor impact to many. P3 = medium, workaround exists.
   P4 = low, convenience or cosmetic issue.

2. **SLA time remaining:** A P2 with 10 minutes left on SLA is more urgent than a P1
   with 6 hours left. Breached SLAs always get acknowledged first — even if the
   underlying issue is lower priority — because the breach itself must be logged and
   communicated.

A simple rule of thumb: **breached first, then P1, then P2, then sort by time remaining
within each priority band.**

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** You have 6 open tickets — one P1 with 45 minutes left on SLA, one P2
with 3 hours left, and four P3s. In what order do you work them?

**Answer:** P1 first (45 min left — act now or it breaches), then the P2 (3 hours is
comfortable but P2 still outranks P3), then the four P3s sorted by SLA time remaining.
The P3s do not get ignored — they will eventually breach too — but they wait until the
higher-priority work is acknowledged or handed off. If you are the only agent, note the
P3 SLA times in standup so a teammate can pick them up.

</details>

---

## Exercises

### Exercise 1 — [OBSERVE] Orient Yourself

**Setup:** Open `starter/index.html` in your browser. Do not click anything yet.

**Task:**
Without interacting with the simulation, answer the following in writing (in `notes.md`
or on paper):
1. What are the three labeled section headers that appear in the sidebar below the queue filters?
2. Name and describe what each of the column headers in the ticket table represents.
3. What does the red `-15m` badge on ticket ITSM-1324 mean?

**Success condition:** Your written answers match all items in the hints below.

<details>
<summary>What you should see (expand after attempting)</summary>

1. **Left sidebar section headers:** OPERATIONS, KNOWLEDGE & INSIGHTS, CHANNELS & PEOPLE.

2. **Table columns:**
   - Checkbox — for bulk-selecting tickets
   - Request Type — the ticket category shown with an icon (e.g., Incident, Service Request)
   - Key — the unique ticket ID (e.g., ITSM-1324)
   - Summary — the ticket title; should be a concise description of the issue
   - Reporter — the person who opened the ticket (the user with the problem)
   - Assignee — the IT staff member responsible for resolving it
   - Status — the current state in the lifecycle (e.g., WAITING FOR SUPPORT, IN PROGRESS)
   - Created — the date and time the ticket was opened
   - Time to Resolution — the SLA countdown timer; red = breached
   - P — priority (P1 through P4)

3. The SLA has been **breached** — the team committed to responding within a specific
   time window, and that window expired 15 minutes ago.

</details>

**Why this matters:** Real IT ops teams start standups by scanning the queue. Knowing
the layout cold — which column means what, what a red timer signals — prevents fumbling
in front of your team. The queue is your dashboard; you should be able to read it in
under 10 seconds.

---

### Exercise 2 — [OBSERVE] Dissect a Ticket

**Setup:** From the ticket table, click on ticket ITSM-1342 ("Banc.ly Inc is slow") to
open its detail panel.

**Task:**
Answer the following in writing:
1. What is this ticket's type?
2. What is its priority?
3. What is the difference between the Reporter and the Assignee?
4. Scroll to the Activity section. You will see an existing internal note. How can you
   tell it is an internal note and not a public reply to the customer?

**Success condition:** All four answers correct per the hints.

<details>
<summary>What you should see (expand after attempting)</summary>

1. **Incident** — an unplanned disruption (the Banc.ly app is slow, which is an
   unexpected degradation in service quality).
2. **P2 / High** — major impact but not a full service-down.
3. **Reporter** = the person who opened the ticket, usually the user experiencing the
   problem. **Assignee** = the IT staff member who owns and is responsible for resolving
   it. These are different people. Confusing them (e.g., emailing the reporter when you
   mean to update the assignee) is a common new-agent mistake.
4. **Internal notes** have a yellow background and an orange "Internal note" badge — they
   are only visible to the IT team, not the customer. Public comments have a plain white
   background. If you accidentally post an internal note as a public comment, the customer
   sees your internal troubleshooting discussion.

</details>

**Why this matters:** Confusing Reporter with Assignee, or leaking an internal note to
a customer, are among the most common new-agent mistakes. Both can damage trust — one
sends work to the wrong person, the other exposes internal discussions to someone who
shouldn't see them.

---

### Exercise 3 — [BUILD] Triage an Incoming Ticket

**Setup:** Close the detail panel. Find ticket ITSM-1324 ("Admin access to Jira") in
the queue — it is currently WAITING FOR SUPPORT with a breached SLA (red `-15m`).

**Task:**
1. Click ITSM-1324 to open its detail panel.
2. In the **Assignee** dropdown, assign the ticket to "Sammy ServiceDeskAgent".
3. Change the **Status** to "In Progress".
4. Click the **Add a comment** tab to open the comment form. Then click **Add internal note** and type:
   `Investigating — contacted user to confirm access scope.`
   Then submit the note.

**Success condition:** The ticket shows status "IN PROGRESS" in both the detail panel
and the ticket table row. The internal note appears in the Activity log with a yellow
background. The Assignee field shows "Sammy ServiceDeskAgent" (it started as Unassigned).

**Why this matters:** This is the exact sequence you will run every morning at standup:
scan the queue for breached SLAs, assign to the right agent, move to In Progress, log
first contact. Doing this within minutes of a ticket appearing is what prevents a `-15m`
from becoming a `-2h`. The internal note creates an audit trail — every status change
and note is timestamped and logged permanently.

---

### Exercise 4 — [BUILD] Create a Ticket from a User Report

**Setup:** A colleague forwards you this email:

> Hi IT, I can't connect to the VPN from home — getting "authentication failed". I'm
> on Windows 11. This started after I reset my password this morning. — Dante

**Task:**
1. Click **+ Create** to open the new ticket form.
2. Choose the correct **Issue Type**.
3. Fill in **Summary** with a clear, searchable title (not just "VPN problem").
4. Fill in **Description** with the relevant details from Dante's email.
5. Set **Priority** appropriately.
6. **Assign** it to an agent.
7. Click **Create**.

**Success condition:** A new ticket appears in the queue with status "WAITING FOR
SUPPORT", the correct issue type, and a descriptive summary that gives the next agent
enough context to start working without hunting down Dante.

<details>
<summary>Hint / What you should see (expand after attempting)</summary>

- **Issue Type:** Incident — the VPN is broken for Dante after a password reset. This
  is an unplanned disruption, not a planned request. Even though the cause (password
  reset) was intentional, the VPN failure was not.
- **Good summary:** "VPN authentication failure after password reset — Windows 11"
- **Priority:** P2 — Dante cannot work remotely, which is a major impact to one user.
  Not P1 (no revenue-critical service is down for everyone), not P3 (there is no
  workaround if they need to VPN in).
- **Description should include:** what's happening ("authentication failed" error),
  the exact error message, the OS (Windows 11), when it started (after this morning's
  password reset), and what changed (the password reset).

</details>

**Why this matters:** Vague tickets ("VPN broken") get lost, get misrouted, or require
a follow-up call with the reporter to gather basic information. A well-formed ticket is
findable in search, filterable by type and priority, and gives the next agent enough
context to start working immediately — even if the original agent is out sick. Good
ticket hygiene is what separates a functional IT org from a chaotic one.

---

### Exercise 5 — [REFLECT-IN-PLACE] Classify These Scenarios

**Setup:** No browser interaction needed. Work from your notes.

**Task:**
For each scenario below, write (a) the correct JSM ticket type and (b) one sentence
explaining why.

- **Scenario A:** "The office Wi-Fi has been dropping for 30 seconds every day at
  exactly 2pm for the past week. Multiple users are affected. Nobody knows the cause."
- **Scenario B:** "The finance team needs a new license for Adobe Acrobat Pro for a
  new hire starting Monday."
- **Scenario C:** "We're upgrading the email server from Exchange 2016 to 2019 next
  Saturday at midnight with a 4-hour maintenance window."

**Success condition:**
- **A = Problem** — a recurring pattern of disruption with an unknown root cause. Each
  individual drop was an Incident, but the pattern points to an underlying cause that
  needs investigation to prevent recurrence.
- **B = Service Request** — a planned fulfillment of a standard need. Nothing is broken;
  a new hire needs a resource that follows a predictable procurement process.
- **C = Change** — a planned modification to infrastructure with a maintenance window
  and an approval process. The team is deliberately modifying a production system.

**Why this matters:** The ticket type determines which queue the ticket lands in, which
SLA applies, which team handles it, and how it shows up in monthly reports. A Change
that gets filed as an Incident bypasses the change approval process — which exists to
prevent outages. A Problem filed as a series of Incidents never gets root-cause
investigation and keeps recurring. Getting classification right is not bureaucracy; it
is how the right work reaches the right people with the right urgency.

---

## Reflection

*Write your answers in `notes.md` before moving to the next lab.*

**Tier 1 — Recall**

1. What does SLA stand for, and what happens operationally when an SLA timer turns red
   in JSM?

2. What is the difference between the Reporter and Assignee fields on a JSM ticket?

**Tier 2 — Application**

3. Your queue opens with 8 tickets: one P1 with 45 minutes left on SLA (currently
   unacknowledged), one P2 with 30 minutes left on SLA (also unacknowledged), and six
   P3s with 2–6 hours remaining. Describe your triage decision process in 3–4 sentences.

4. A user is angry about the slow response on their ticket and calls you directly.
   You are still investigating — you don't have a fix yet. Do you leave them a public
   comment or an internal note first, and what do you write in each?

**Tier 3 — Transfer**

5. JSM's ticket types (Incident, Problem, Change, Service Request) map directly to ITIL
   4 framework concepts. Search for "ITIL 4 incident vs problem management". How does
   the Incident → Problem → Known Error chain relate to what you practiced in Exercise
   5, Scenario A? What would the Known Error record contain in that scenario, and what
   would "workaround" mean for the daily Wi-Fi drop?

---

## Going Deeper

- [Atlassian: What is Jira Service Management?](https://www.atlassian.com/software/jira/service-management): Official overview including how JSM differs from Jira Software (for dev teams) — worth reading to understand why IT ops and engineering use different Jira products.
- [ITIL 4 Foundation overview (AXELOS)](https://www.axelos.com/certifications/itil-service-management/itil-4-foundation): The framework that defines Incident, Problem, Change, and Service Request at a process level — understanding ITIL makes JSM's structure make sense rather than feel arbitrary; the Foundation certification is the standard entry-level IT ops credential.
- [Atlassian: SLA in Jira Service Management](https://support.atlassian.com/jira-service-management-cloud/docs/): Atlassian JSM Cloud documentation — browse to 'SLAs' for configuration guides; the root index lists all available help articles. Covers how SLA timers are configured, what "breached" means in a real org, and how to read SLA compliance reports — essential reading before your first monthly IT ops review.
