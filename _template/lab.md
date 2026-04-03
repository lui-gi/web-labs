# Lab N — Title
<!-- Replace N with the lab number and Title with the lab name -->

**Phase:** N | **Estimated time:** X hours | **Type:** Conceptual / Hands-on / Attack-Defense
<!-- Type: use one of the three above. Delete the others. -->

---

## Overview

<!-- 3–5 sentences answering:
  - What is this lab about?
  - Why does it matter for the curriculum / bug bounty track?
  - What will the learner be able to do after completing it?
     → Write these as "After this lab, [learner] will be able to..." statements.
     → Use "explain", "build", "attack", "identify" — not "understand" or "learn about".
-->

---

## Prerequisites

<!-- List everything needed before starting this lab. Be specific. -->

- [ ] Lab N-1 complete
- [ ] Tools installed:
  - `tool-name` — [install instructions or link]
- [ ] Concepts assumed known: [link to relevant section of a prior lab if applicable]

---

## Concepts

<!-- This section is for READING. No instructions here — pure explanation.
     Break into H3 subsections. Each subsection:
       1. Explains a concept with enough depth to reason about it
       2. Ends with a <details> Mental model check

     The Mental model check is the core mechanism for deep understanding:
     the learner must form an answer BEFORE expanding the disclosure.
     Write the question so it cannot be answered by restating what was
     just written — it should require applying or compressing the concept.

     Ratio guide:
       Conceptual labs (1, 6, 14):  6–8 subsections, 3–4 exercises
       Hands-on labs (3, 5, 9, 11): 2–3 subsections, 6–8 exercises
       Attack-defense labs (15–20): 3–4 subsections, 6–8 exercises
-->

### 2.1 [Subsection Title]

[Explanation prose. Write for someone who has completed the prior labs.
 Do not assume knowledge beyond the prerequisites listed above.
 Concrete examples beat abstract definitions every time.]

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** [A question that requires compressing or applying the concept above.
 It should not be answerable by copy-pasting a sentence from the prose.
 Example pattern: "In your own words, why does X happen?" or
 "If Y changed, what would break and why?"]

**Answer:** [The authoritative answer. Write this to correct misconceptions,
 not just to confirm correct answers. Include the "why" even if the question
 only asked "what".]

</details>

### 2.2 [Subsection Title]

[Continue as above...]

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** [...]

**Answer:** [...]

</details>

---

## Exercises

<!-- This section is for DOING.
     Each exercise uses a type tag on the heading:
       [OBSERVE]  — run or inspect something without changing it
       [BUILD]    — write or modify code
       [ATTACK]   — exploit a vulnerability (your own setup or a provided one)
       [PATCH]    — fix something that was just broken
       [DIAGRAM]  — draw or describe an architecture/flow BEFORE verifying it
       [REFLECT-IN-PLACE] — a focused thinking exercise embedded mid-sequence

     For attack-defense labs (Phase 5), exercises MUST follow this sequence:
       [OBSERVE] → [ATTACK] → [PATCH]
     Never put [PATCH] before [ATTACK].

     Each exercise block has four fields:
       Setup            — environment state expected before starting (skip if obvious)
       Task             — the instruction
       Success condition — the specific observable that confirms it worked;
                          not just "it runs" — name exactly what should appear/change
       Why this matters — always visible, never inside <details>; explains the
                          underlying mechanism this exercise is demonstrating

     Use <details> inside exercises ONLY for:
       - "What you should see" hints (expand after attempting)
       - For [PATCH] exercises: the reference patch implementation
         (forces learners to attempt their own fix before seeing the answer)
-->

### Exercise 1 — [OBSERVE / BUILD / ATTACK / PATCH / DIAGRAM] [Short Title]

**Setup:** [What state the environment needs to be in. E.g., "server running on port 8000", "Lab 3 starter code open". Skip this field if it's obvious from context.]

**Task:**
[Clear instruction. If there are multiple steps, use a numbered list.
 For [DIAGRAM] exercises, always say "from memory first, then verify".]

**Success condition:** [Exactly what the learner should see, receive, or be able to show when done.]

<details>
<summary>Hint / What you should see (expand after attempting)</summary>

[Guidance for when the learner is stuck, or confirmation of what correct output looks like.
 For [PATCH] exercises, replace this summary with "Reference patch (expand after attempting your own)"
 and put the reference implementation here.]

</details>

**Why this matters:** [One paragraph. Always visible. Explains the mechanism this exercise
demonstrates and why it's relevant to the broader curriculum goal (bug bounty / security).]

---

### Exercise 2 — [TYPE] [Short Title]

**Setup:** [...]

**Task:**
[...]

**Success condition:** [...]

**Why this matters:** [...]

---

<!-- Add more exercises following the same pattern. -->

---

## Reflection

<!-- Five questions, NO answers provided anywhere in this file.
     The learner writes answers in notes.md.
     Never use <details> here — these questions have no "correct" answer to reveal.

     Three tiers:
       Tier 1 (Recall, 2 questions):     Can the learner restate the mechanism?
       Tier 2 (Application, 2 questions): What happens when context changes?
       Tier 3 (Transfer, 1 question):     Connect to a real CVE, OWASP category,
                                          or bug bounty report — cannot be answered
                                          by restating the lab.

     Write Tier 3 so it requires external knowledge. Reference a specific CVE,
     OWASP Top 10 entry, or published bug bounty report by name.
-->

*Write your answers in `notes.md` before moving to the next lab.*

**Tier 1 — Recall**

1. [Restate-the-mechanism question. Example: "In your own words, explain what happens between typing a URL and seeing the first byte of a response."]

2. [Second recall question.]

**Tier 2 — Application**

3. [What-if question. Example: "If a server returned no Cache-Control header, how would a browser decide how long to cache the response?"]

4. [Second application question.]

**Tier 3 — Transfer**

5. [Real-world connection. Example: "CVE-2008-1447 (the Kaminsky DNS cache poisoning bug) exploited a property of DNS you saw in this lab. What was that property, and why did it take so long to patch?"]

---

## Going Deeper

<!-- 2–4 optional pointers. Always annotated — one sentence on why each is worth reading.
     Prioritize: RFCs, CVEs, OWASP entries, published bug bounty reports, research papers.
     Do not link to tutorial blog posts unless they are unusually authoritative. -->

- [Resource title](URL): [One sentence on why this is worth reading and what it adds beyond the lab.]
- [Resource title](URL): [...]
