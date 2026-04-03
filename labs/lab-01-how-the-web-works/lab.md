# Lab 1 — How the Web Works

**Phase:** 1 | **Estimated time:** 3–4 hours | **Type:** Conceptual

---

## Overview

Every web vulnerability — XSS, SQL injection, SSRF, IDOR — is ultimately an abuse of the
communication protocols covered in this lab. Before writing a single line of code or running a
single exploit, a clear mental model of what happens between a browser and a server is essential.

After this lab, you will be able to:
- Trace the full lifecycle of an HTTP request from DNS lookup through TCP handshake to response
- Read and interpret HTTP request/response headers in DevTools and Wireshark
- Explain how cookies and sessions establish identity across stateless HTTP connections
- Identify which layer of the stack (DNS, TCP, HTTP) a given network attack targets

---

## Prerequisites

- [ ] No prior labs required — this is Lab 1
- [ ] Tools installed:
  - Browser with DevTools (Chrome or Firefox)
  - `wireshark` — [install](https://www.wireshark.org/download.html)
  - `dig` — included on Linux/macOS; Windows: install BIND tools or use WSL
  - `curl` — included on Linux/macOS; [Windows install](https://curl.se/windows/)

---

## Concepts

### 2.1 DNS: How a Name Becomes an Address

When a browser is given `https://example.com`, the first thing it needs is an IP address.
It does not know this; it must ask. The Domain Name System (DNS) is the phone book that
translates human-readable names into IP addresses machines can route to.

The resolution process is recursive. The browser first checks its local cache. If the
record isn't there, it asks the operating system's configured resolver (typically your
router or ISP's server). If that resolver doesn't have the record cached, it climbs the
DNS hierarchy: root nameservers → TLD nameservers (`.com`, `.org`) → the authoritative
nameserver for the specific domain. The final answer travels back down the chain and is
cached at each layer according to the record's TTL (Time to Live), measured in seconds.

This caching is both a performance feature and a security surface. An attacker who can
poison a resolver's cache — substituting a malicious IP for a legitimate one — intercepts
traffic without touching either endpoint.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A DNS record has a TTL of 300. A user visits the site, their resolver
caches the answer, and then the site operator changes the IP address. What is the maximum
delay before all users see the new IP, and what determines that delay?

**Answer:** The maximum delay is the TTL value at the moment the record was last cached —
up to 300 seconds (5 minutes) in this case. Users whose resolvers already have the old
record cached will continue receiving the old IP until their cache entry expires. Users
who query after the change will get the new IP immediately. This is why operators lower
the TTL hours before a planned IP change, and why DNS propagation is not instantaneous.

</details>

---

### 2.2 TCP: The Reliable Pipe

HTTP runs on top of TCP (Transmission Control Protocol). Before any HTTP data is exchanged,
the browser and server must establish a TCP connection through a three-way handshake:

1. **SYN** — the client sends a synchronize packet, choosing a random initial sequence number
2. **SYN-ACK** — the server acknowledges and responds with its own sequence number
3. **ACK** — the client acknowledges the server's sequence number

After the handshake, both sides have agreed on sequence numbers and the connection is
"established." TCP then guarantees that data arrives in order and without corruption,
retransmitting any lost packets automatically. This reliability is what makes HTTP
workable over an unreliable network — but it also means every connection has setup
overhead before the first byte of application data is sent.

For HTTPS, a TLS handshake occurs after the TCP handshake, adding another round trip
(or half round trip with TLS 1.3) before the encrypted channel is ready.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** An attacker sends a flood of SYN packets to a server but never completes
the handshake (never sends the final ACK). What resource does this exhaust on the server,
and what is this attack called?

**Answer:** The server allocates memory for each half-open connection, waiting for the
final ACK that never arrives. A flood of these exhausts the server's connection table
(the SYN backlog), preventing legitimate clients from completing handshakes. This is a
SYN flood attack — a classic denial-of-service technique that exploits the stateful
nature of the TCP handshake.

</details>

---

### 2.3 HTTP: The Request-Response Cycle

HTTP (HyperText Transfer Protocol) is the application-layer protocol that browsers and
servers use to exchange data. Every interaction is a request-response pair:

**Request structure:**
```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 ...
Accept: text/html
Cookie: session_id=abc123
```

**Response structure:**
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session_id=abc123; HttpOnly; Secure
Content-Length: 1234

<!DOCTYPE html>...
```

The **method** (GET, POST, PUT, DELETE, PATCH) indicates the intended action. The
**path** identifies the resource. **Headers** are key-value metadata that both sides
use to negotiate content type, caching, authentication, and more.

**Status codes** are grouped by their first digit:
- `2xx` — success (200 OK, 201 Created, 204 No Content)
- `3xx` — redirection (301 Moved Permanently, 302 Found, 304 Not Modified)
- `4xx` — client error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
- `5xx` — server error (500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable)

HTTP is **stateless**: each request is independent. The server has no built-in memory of
prior requests. Cookies and sessions are the mechanisms layered on top to simulate state.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A login endpoint returns a `302 Found` with a `Location: /dashboard` header
after successful authentication. What does the browser do next, and using what method?

**Answer:** The browser automatically issues a new GET request to `/dashboard`. This is
the standard Post/Redirect/Get (PRG) pattern. The redirect ensures that if the user
refreshes `/dashboard`, the browser does not re-submit the login form — it only re-issues
the GET. This is why login forms typically respond with a redirect rather than directly
serving the post-login page.

</details>

---

### 2.4 Cookies and Sessions

HTTP's statelessness means a server cannot inherently tell request #47 apart from request
#1. Cookies solve this by having the server attach a small piece of data to a response
(`Set-Cookie`), which the browser stores and automatically includes in all future requests
to that domain (`Cookie` header).

A **session cookie** typically stores just a random session ID (e.g., `session_id=a3f9...`).
The actual session data (user ID, permissions, cart contents) lives on the server, keyed
by that ID. This is secure because the sensitive data never leaves the server — only the
random identifier crosses the network.

A **JWT (JSON Web Token)**, by contrast, stores the actual claims (user ID, roles) inside
a signed token that the client holds. The server verifies the signature rather than
looking up server-side state. This enables stateless authentication but introduces
different risks (covered in Lab 10 and Lab 19).

Critical cookie attributes for security:
- `HttpOnly` — prevents JavaScript from reading the cookie (blocks cookie theft via XSS)
- `Secure` — cookie is only sent over HTTPS connections
- `SameSite=Strict/Lax` — restricts cross-site cookie sending (mitigates CSRF)

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A session cookie lacks the `HttpOnly` flag. A page on the same site has a
stored XSS vulnerability. What can an attacker do, and what does `HttpOnly` prevent?

**Answer:** Without `HttpOnly`, JavaScript on the page can read `document.cookie` and
exfiltrate the session ID to an attacker-controlled server. The attacker can then use
that session ID to impersonate the victim — this is session hijacking. The `HttpOnly`
flag makes the cookie inaccessible to JavaScript entirely, so even if XSS is present,
the cookie cannot be stolen via script. It does not prevent the cookie from being sent
with requests — only from being read by JavaScript.

</details>

---

### 2.5 HTTP Headers Worth Knowing

Headers are where a large portion of web security lives. These are the ones that appear
constantly in bug bounty reports and security tooling:

**Request headers:**
- `Host` — which virtual host is being requested (required in HTTP/1.1)
- `Authorization` — credentials, often `Bearer <token>` for JWTs
- `Origin` — the origin of a cross-origin request (used in CORS)
- `Referer` — the URL that linked to this request (note: intentionally misspelled)
- `X-Forwarded-For` — client IP when behind a proxy; trivially spoofable

**Response headers:**
- `Content-Type` — what the response body is; if wrong, browsers may sniff and execute scripts
- `Content-Security-Policy` — restricts what sources scripts, styles, and media can load from
- `Strict-Transport-Security` — forces HTTPS for a specified duration
- `X-Content-Type-Options: nosniff` — prevents MIME-type sniffing
- `Access-Control-Allow-Origin` — controls which origins can read cross-origin responses (CORS)

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A server responds with `Content-Type: text/plain` but the body is actually
HTML containing a `<script>` tag. The `X-Content-Type-Options: nosniff` header is absent.
What might happen, and why does the `nosniff` directive prevent it?

**Answer:** Without `nosniff`, some browsers perform MIME-type sniffing — they inspect the
response body and may decide it "looks like" HTML regardless of the declared Content-Type,
then parse and execute it as HTML. This allows a script tag in a response declared as
`text/plain` to execute. `X-Content-Type-Options: nosniff` instructs the browser to
trust the declared Content-Type exactly and never sniff, preventing this escalation.

</details>

---

## Exercises

### Exercise 1 — [OBSERVE] Watch DNS Resolution

**Setup:** Terminal open, `dig` installed.

**Task:**
1. Run `dig example.com` and read the full output
2. Identify: the ANSWER SECTION, the TTL value, and the server line at the bottom
3. Run the same command again immediately — note whether the TTL has changed
4. Run `dig example.com +trace` to watch the full recursive resolution from root servers

**Success condition:** You can point to each section of `dig` output and explain what it contains. The TTL on the second run should be slightly lower than the first.

<details>
<summary>What you should see (expand after attempting)</summary>

The ANSWER SECTION contains one or more `A` records mapping the name to IPv4 addresses.
The TTL decreases between runs because your resolver is counting down the cache lifetime.
The `+trace` output shows the full delegation chain: root (`.`) → `.com` TLD → the
authoritative nameserver for `example.com`. Each line shows which server answered and
with what authority level.

</details>

**Why this matters:** Every web request starts with DNS. Understanding the delegation
chain — and how TTL-controlled caching works — is the foundation for understanding DNS
cache poisoning, subdomain takeover, and DNS-based reconnaissance in bug bounty work.

---

### Exercise 2 — [OBSERVE] Read a Raw HTTP Exchange in DevTools

**Setup:** Browser open to any site you own or a test site like `http://httpbin.org`.

**Task:**
1. Open DevTools (F12) → Network tab
2. Navigate to the site with "Preserve log" checked
3. Click on the first request in the log
4. In the Headers tab, locate and read:
   - The request method and path
   - The `Host`, `User-Agent`, and `Cookie` headers (if present)
   - The response status code and `Content-Type`
   - Any `Set-Cookie` headers in the response
5. Repeat for the second request and note how the `Cookie` header now carries what `Set-Cookie` set

**Success condition:** You can read aloud what the browser sent and what the server replied, line by line, for at least two requests.

**Why this matters:** Bug bounty hunters spend a large portion of their time in this view.
Every parameter, every header, and every cookie is a potential injection point or
authorization bypass. DevTools is the first tool in the chain — before Burp Suite, before
any scanner.

---

### Exercise 3 — [OBSERVE] Capture HTTP Traffic in Wireshark

**Setup:** Wireshark installed. Use a non-HTTPS site for this exercise (HTTPS traffic will be encrypted). `http://httpbin.org/get` works.

**Task:**
1. Start a Wireshark capture on your active network interface
2. In a browser, visit `http://httpbin.org/get`
3. Stop the capture
4. In the display filter bar, type `http` and press Enter
5. Find the GET request packet. Right-click → Follow → HTTP Stream
6. Read the raw request and response in the stream view

**Success condition:** You can see the full plaintext HTTP request and response, including headers, in the Wireshark stream view.

<details>
<summary>What you should see (expand after attempting)</summary>

The HTTP stream shows exactly what traversed the network — no browser formatting, no
abstractions. The request section (typically in red) shows the raw `GET /get HTTP/1.1`
line followed by headers. The response section (blue) shows the status line, headers,
and body. If anything in that stream looks unfamiliar, look it up in the HTTP spec.

</details>

**Why this matters:** HTTPS hides this content from network observers — which is why
HTTPS matters. But in contexts where traffic is unencrypted (internal networks, HTTP
downgrade attacks, misconfigured proxies), an attacker in a position to observe the
network sees everything in this view. Understanding what's visible motivates why
`Secure` cookies and HSTS exist.

---

### Exercise 4 — [OBSERVE] Inspect Cookie Attributes

**Setup:** Browser DevTools open.

**Task:**
1. Visit any site that uses cookies (most sites do)
2. In DevTools → Application tab → Cookies → select the domain
3. For each cookie listed, find and record:
   - Is `HttpOnly` checked?
   - Is `Secure` checked?
   - What is the `SameSite` value?
   - What is the expiration? (Session cookie vs. persistent?)
4. Find at least one cookie missing `HttpOnly` and note its name

**Success condition:** You have a table (mental or written in notes.md) of the cookies on one site and their security attributes.

**Why this matters:** Missing `HttpOnly` is a direct enabler of session hijacking via
XSS. Missing `Secure` allows the cookie to travel over HTTP where it can be observed.
Missing `SameSite` contributes to CSRF risk. Reading cookie attributes is one of the
first checks in a bug bounty recon pass.

---

### Exercise 5 — [DIAGRAM] Map the Full Request Lifecycle

**Setup:** notes.md open, nothing else needed.

**Task:**
Draw (or write out as a numbered sequence) the complete lifecycle of what happens when
a browser loads `https://example.com/page`. Do this **from memory first**. Cover:
- DNS resolution
- TCP handshake
- TLS handshake
- HTTP request
- Server processing
- HTTP response
- Browser rendering begins

Once your diagram is complete, verify it by reading through sections 2.1–2.3 and correcting any gaps.

**Success condition:** Your diagram includes all seven stages above, with at least one sentence describing what each stage accomplishes.

<details>
<summary>Reference sequence (expand after completing your own)</summary>

1. **DNS** — Browser checks local cache → OS cache → resolver → recursive lookup → A record returned with TTL
2. **TCP SYN** → **SYN-ACK** → **ACK** — Three-way handshake establishes connection to port 443
3. **TLS** — ClientHello → ServerHello + Certificate → key exchange → Finished; encrypted channel established
4. **HTTP GET** — Browser sends `GET /page HTTP/1.1` with headers including `Host: example.com`
5. **Server processing** — Server routes request, executes application logic, queries database if needed
6. **HTTP response** — Server sends status line, headers (`Content-Type`, `Set-Cookie`, etc.), and body
7. **Rendering** — Browser parses HTML, discovers linked resources (CSS, JS, images), fires additional requests for each

Gaps in a first attempt commonly include: forgetting TLS entirely, skipping DNS caching, or treating "server processing" as a black box without noting it may involve its own network calls (database, cache, third-party API).

</details>

**Why this matters:** This diagram is the mental model for the rest of the curriculum.
Every lab in Phases 2–6 is about one or more boxes in this diagram — backend logic, the
database layer, the auth layer, or exploiting the assumptions baked into this protocol
stack. Internalizing the full sequence makes it obvious where each class of attack sits.

---

## Reflection

*Write your answers in `notes.md` before moving to the next lab.*

**Tier 1 — Recall**

1. A browser sends an HTTP request. Walk through every network event that had to occur first, before the first byte of the HTTP request left the machine.

2. What is the difference between a `301 Moved Permanently` and a `302 Found` redirect? In what scenario would choosing the wrong one break something for a user who has visited before?

**Tier 2 — Application**

3. A site sets a session cookie with no `Secure` flag on an HTTPS login page. Describe the exact sequence of events by which an attacker on the same coffee shop WiFi could steal that session, assuming the user never visits the HTTP version of the site.

4. A company lowers its DNS TTL from 86400 (24 hours) to 300 (5 minutes) right before a major IP migration. What is the tradeoff they are making, and what would happen if they forgot to lower the TTL first?

**Tier 3 — Transfer**

5. CVE-2008-1447 (the Kaminsky DNS cache poisoning vulnerability) allowed an attacker to inject forged DNS responses into a resolver's cache without needing to be on the network path between the resolver and authoritative server. Which property of DNS at the time made this possible, and what was the fix? (Research this CVE — the answer is not in this lab.)

---

## Going Deeper

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): The authoritative spec for HTTP methods, status codes, and headers. Dense but worth having as a reference — when a header behaves unexpectedly, this is the ground truth.
- [RFC 1035 — Domain Names Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035): The original DNS spec from 1987. Reading sections 3–4 gives more intuition about the wire format than any tutorial.
- [OWASP Testing Guide — OTG-INFO-001 through OTG-INFO-005](https://owasp.org/www-project-web-security-testing-guide/): The reconnaissance section of the OWASP testing guide covers DNS, HTTP headers, and cookies from an attacker's enumeration perspective — the direct application of this lab's content.
- [The Illustrated TLS 1.3 Connection](https://tls13.xargs.org): A byte-by-byte visual walkthrough of the TLS handshake. Essential for understanding what HTTPS actually provides and where its limits are.
