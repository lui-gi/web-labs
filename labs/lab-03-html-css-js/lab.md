# Lab 3 — Intro to HTML/CSS/JS (No Frameworks)

**Phase:** 1 | **Estimated time:** 3–4 hours | **Type:** Hands-on

---

## Overview

Every frontend framework — React, Vue, Angular — is an abstraction over three things:
HTML (structure), CSS (presentation), and JavaScript (behavior). Developers who learn
frameworks first often have a fragile mental model: they know how to use the abstraction
but cannot reason about what it produces. This lab removes the abstraction entirely.

The product is a single HTML file: a form that takes two numbers and displays their sum,
built using only the browser's native APIs. Nothing is installed. No build step. The
browser is the runtime.

After this lab, you will be able to:
- Explain what the DOM is and how JavaScript uses it to read and modify a page
- Write a form that captures user input and responds to submission without a page reload
- Read a form input's value from JavaScript and write a result back to the page
- Distinguish between HTML structure, CSS presentation, and JS behavior as separate concerns

---

## Prerequisites

- [ ] Lab 1 complete (HTTP request/response mental model)
- [ ] Lab 2 complete (frontend/backend relationship)
- [ ] Tools installed:
  - Any text editor (VS Code recommended)
  - Any modern browser
- [ ] No server, no Node.js, no Python — just a browser and a text editor

---

## Concepts

### 2.1 HTML: Structure as a Tree

HTML is not just text — when a browser parses an HTML file it builds a tree called the
**Document Object Model (DOM)**. Each HTML tag becomes a node in the tree. The `<html>`
element is the root; `<head>` and `<body>` are its children; everything else descends
from there.

This tree representation is what JavaScript operates on. When code calls
`document.getElementById('result')`, it is traversing the DOM tree and returning a
reference to a node. When it sets `element.textContent = 'hello'`, it is mutating
a node in that tree, and the browser immediately re-renders that part of the page.

Key structural elements for this lab:
- `<form>` — a container for user input elements; has a `submit` event
- `<input type="number">` — a field that accepts numeric input
- `<button type="submit">` — triggers form submission
- `<p>` or `<div>` — a block element used to display the result

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** `document.getElementById('result')` returns `null`. What does that tell
you, and what is the most common cause?

**Answer:** `null` means no element with `id="result"` exists in the DOM at the moment
the JavaScript ran. The most common cause is script placement: if the `<script>` tag
is in `<head>` (or anywhere before the element it references), the DOM is not fully
built when the script executes. Moving the `<script>` to just before `</body>`, or
wrapping the code in a `DOMContentLoaded` listener, fixes this. A second common cause
is a typo — `id="results"` vs `getElementById('result')`.

</details>

---

### 2.2 JavaScript Events and the DOM

JavaScript in a browser is **event-driven**. Code does not run top-to-bottom on a timer;
it runs in response to events. A user clicking a button, submitting a form, or moving
a mouse all generate events. JavaScript registers handlers — functions — that execute
when specific events occur.

The pattern is always the same:
1. Get a reference to a DOM element
2. Call `.addEventListener(eventType, handlerFunction)` on it
3. Inside the handler, read inputs, compute, write outputs

For a form, the relevant event is `submit`. By default, submitting a form triggers a
full page reload (an HTTP GET or POST request to the current URL or the `action`
attribute's URL). To prevent this — which is almost always what a single-page form
needs — call `event.preventDefault()` at the start of the submit handler.

```javascript
const form = document.getElementById('my-form');

form.addEventListener('submit', function(event) {
  event.preventDefault(); // stop the page from reloading
  // ... do work here
});
```

Reading an input's value:
```javascript
const value = document.getElementById('num1').value; // returns a string
const number = parseFloat(value);                     // convert to a number
```

Writing to an output element:
```javascript
document.getElementById('result').textContent = 'The sum is: ' + sum;
```

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** A form submit handler runs, computes the correct sum, and calls
`resultElement.textContent = sum`. The page displays "NaN". What went wrong?

**Answer:** `input.value` always returns a **string**, even when `type="number"`.
Adding two strings with `+` concatenates them: `"3" + "4"` is `"34"`, not `7`. Then
some operation (subtraction, multiplication, or attempting `parseInt` on a non-numeric
string) produced `NaN`. The fix is to explicitly convert with `Number()`, `parseInt()`,
or `parseFloat()` before arithmetic. A secondary cause: if either input is empty,
`Number("")` is `0` but `parseFloat("")` is `NaN` — choose the conversion function
deliberately based on what empty input should mean.

</details>

---

### 2.3 CSS: Presentation as Rules

CSS (Cascading Style Sheets) controls the visual presentation of HTML elements. It is
separate from HTML deliberately — structure and presentation are different concerns.

CSS rules are selector-property pairs:
```css
h1 {
  font-size: 2rem;
  color: #333;
}

#result {
  font-weight: bold;
  margin-top: 1rem;
}
```

For this lab, CSS is not the focus. Two properties to know:
- `display: none` — hides an element completely (useful for hiding the result container until a sum is computed)
- `color`, `font-size`, `margin`, `padding` — basic visual adjustments

The cascade: when multiple rules match the same element, the most **specific** selector
wins. `#result` (ID selector) beats `.output` (class selector) beats `p` (tag selector).
Inline styles (`style="..."`) beat all three.

<details>
<summary>Mental model check — answer before expanding</summary>

**Question:** An element has `display: none` set in a stylesheet. JavaScript sets
`element.style.display = 'block'`. Which rule wins, and why?

**Answer:** The JavaScript inline style wins. Inline styles (set via `element.style.property`)
are equivalent to a `style` attribute directly on the element, which has the highest
specificity in the cascade — above any stylesheet rule regardless of selector. This is
the standard pattern for showing/hiding elements dynamically: hide via CSS by default,
reveal via JavaScript when needed.

</details>

---

## Exercises

### Exercise 1 — [OBSERVE] Open a Bare HTML File in a Browser

**Setup:** Text editor and browser ready. No server needed.

**Task:**
1. Create a new file called `scratch.html` anywhere on your machine (outside the lab directory)
2. Paste this exact content and save:
   ```html
   <!DOCTYPE html>
   <html>
     <body>
       <p id="hello">Original text</p>
       <script>
         document.getElementById('hello').textContent = 'Changed by JavaScript';
       </script>
     </body>
   </html>
   ```
3. Open it directly in your browser using File → Open (or drag it onto the browser)
4. Open DevTools → Console tab and type: `document.getElementById('hello')`

**Success condition:** The page displays "Changed by JavaScript" (not "Original text"), and the console returns the `<p>` element object.

**Why this matters:** This is the entire foundation of browser JavaScript — the DOM is
mutable, scripts modify it, and the browser re-renders. Every React component, every
jQuery plugin, every vanilla JS form reduces to this. The fact that you opened a local
file with no server demonstrates that the browser itself is the runtime; HTTP is just
the delivery mechanism.

---

### Exercise 2 — [OBSERVE] Inspect the DOM vs. the Source

**Setup:** `scratch.html` from Exercise 1 open in browser.

**Task:**
1. Right-click the page → View Page Source. Read the HTML.
2. Right-click the page → Inspect (or F12). Look at the Elements tab.
3. Find the difference between the two views.

**Success condition:** You can explain in one sentence why the source and the Elements panel show different text.

<details>
<summary>What you should see (expand after attempting)</summary>

View Source shows the original HTML file exactly as written — "Original text". The
Elements panel shows the live DOM after JavaScript has run — "Changed by JavaScript".
Source is the file. Elements is the current state of the tree in memory. Frameworks like
React produce minimal source HTML and build the entire DOM via JavaScript — which is why
"View Source" on a React app looks nearly empty but the Elements panel shows the full page.

</details>

**Why this matters:** Security scanners that only read the page source miss content that
JavaScript injects. Understanding this gap matters for recon — tools like `curl` see the
source; a headless browser sees the rendered DOM.

---

### Exercise 3 — [BUILD] Write the Form Structure

**Setup:** Open `starter/index.html` from this lab directory in your text editor.

**Task:**
Inside `<body>`, add:
1. An `<h1>` with the text "Number Adder"
2. A `<form>` element with `id="adder-form"`
3. Inside the form: two `<input type="number">` elements with `id="num1"` and `id="num2"`,
   each with a visible `<label>`
4. A `<button type="submit">` with the text "Add"
5. A `<p>` element with `id="result"` below the form (outside it), initially empty

Open the file in your browser. The form should appear and be interactive, though
submitting it will reload the page for now.

**Success condition:** The page shows a labeled form with two number inputs and a button. The Elements panel confirms IDs are correct.

**Why this matters:** HTML form structure is what servers receive as POST bodies, what
scanners enumerate as attack surface, and what accessibility tools read. Getting the
structure right — correct element types, correct IDs, labels associated to inputs —
is not cosmetic.

---

### Exercise 4 — [BUILD] Intercept Submission and Read Inputs

**Setup:** `starter/index.html` with form from Exercise 3.

**Task:**
Inside the `<script>` tag at the bottom of `<body>`:
1. Get a reference to the form by ID
2. Add a `submit` event listener
3. Inside the listener, call `event.preventDefault()`
4. Read the values of both inputs
5. Use `console.log()` to print both values and their types (`typeof`)

Open DevTools Console before submitting. Fill in the inputs and click Add.

**Success condition:** The page does not reload. The console shows both input values logged, and their `typeof` is `"string"`.

<details>
<summary>What you should see (expand after attempting)</summary>

```
3          (string)
4          (string)
```

Even though `type="number"` restricts what the user can type, `.value` still returns a
string. This is consistent — `.value` is always a string for all input types. The
`type="number"` only affects browser UI (numeric keyboard on mobile, up/down arrows)
and basic browser-level validation; it does not change the JavaScript API.

</details>

**Why this matters:** The type mismatch between `input.value` (always string) and
JavaScript arithmetic (needs numbers) is where most first-time bugs come from. It is
also a reminder: never trust input types to enforce server-side constraints. A `type="number"`
field is trivially bypassed with DevTools or curl. Validation must happen at the server.

---

### Exercise 5 — [BUILD] Compute and Display the Sum

**Setup:** `starter/index.html` with the submit listener from Exercise 4.

**Task:**
Inside the submit listener, after reading the inputs:
1. Convert both values to numbers using `parseFloat()`
2. Compute their sum
3. Write the result to the `#result` element's `textContent` in the format:
   `"3 + 4 = 7"`
4. Handle the case where either input is empty or non-numeric — display
   `"Please enter two valid numbers"` instead

Test with: integers, decimals, negative numbers, empty inputs, and non-numeric text
(try bypassing the `type="number"` restriction by temporarily changing it in DevTools).

**Success condition:** The page displays the correct sum for valid inputs and the error message for invalid ones, with no page reload.

**Why this matters:** This exercise contains the complete input → validate → compute →
display cycle that every form on the web follows. The important lesson is what happens
with edge cases: `parseFloat("")` returns `NaN`, `NaN + 5` is `NaN`, `isNaN()` catches
it. Real forms have the same edge cases — and a server that trusts the browser's
`type="number"` to enforce valid input will receive garbage from anyone using curl.

---

### Exercise 6 — [BUILD] Style the Result

**Setup:** `starter/index.html` with working sum from Exercise 5.

**Task:**
In the `<style>` block in `<head>`:
1. Give the page a maximum width of `600px`, centered with `margin: 0 auto`
2. Give inputs and the button some `padding` so they're comfortable to click
3. Style `#result` so it appears visually distinct — use `font-weight: bold` and a
   color of your choice
4. Initially hide `#result` with `display: none` in CSS
5. In JavaScript, set `resultElement.style.display = 'block'` before writing the result

**Success condition:** The result element is invisible on load and appears when the form is submitted.

**Why this matters:** The `display: none` → `display: block` toggle via JavaScript is
the pattern behind every modal, dropdown, and dynamic element on the web. It also
demonstrates the separation of concerns: CSS owns the default state, JavaScript modifies
it in response to events.

---

### Exercise 7 — [DIAGRAM] Map Structure to DOM Tree

**Setup:** Completed `starter/index.html`, DevTools Elements panel open.

**Task:**
In `notes.md`, draw the DOM tree for your completed page. Use indentation to show
parent-child relationships. For each element, note its `id` if it has one.

Then open DevTools → Elements and verify your diagram against the live tree. Mark any
discrepancies.

**Success condition:** Your diagram matches the Elements panel, including the nesting of `<form>` inside `<body>`, inputs inside the form, and `#result` as a sibling of the form.

**Why this matters:** XSS (Lab 15) works by injecting new nodes into this tree.
Understanding the tree structure is prerequisite to understanding where injected content
lands and what access it has. Frameworks that use a "virtual DOM" diff their in-memory
tree against this one — knowing the real tree makes framework output predictable.

---

## Reflection

*Write your answers in `notes.md` before moving to the next lab.*

**Tier 1 — Recall**

1. What does `event.preventDefault()` do in a form's submit handler, and what happens if you omit it?

2. `document.getElementById('num1').value` returns `"42"` even though the input has `type="number"`. Why, and how do you convert it for arithmetic?

**Tier 2 — Application**

3. A form has `<input type="number" min="1" max="100">`. A user bypasses the HTML constraints by editing the request in DevTools and submits `9999`. The server processes it without additional validation. What category of vulnerability is this, and where should validation actually live?

4. A single-page app built entirely with JavaScript has no meaningful HTML in the source — just `<div id="root"></div>`. A bug bounty hunter uses `curl` to fetch the page. What do they see, and what does that mean for their recon?

**Tier 3 — Transfer**

5. DOM-based XSS (a category you will exploit in Lab 15) occurs when JavaScript reads from an attacker-controlled source (like `location.hash` or a URL parameter) and writes it to the DOM without sanitization. Given what you built in this lab — specifically the line where you write to `#result` — what change to Exercise 5 would create a DOM XSS vulnerability, and what would an attacker be able to do with it?

---

## Going Deeper

- [MDN — Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction): The authoritative reference for DOM APIs. When a method behaves unexpectedly, this is the first place to check — not Stack Overflow.
- [MDN — HTMLFormElement: submit event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/submit_event): Documents the exact behavior of form submission including the default action this lab's `preventDefault()` blocks.
- [OWASP — Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html): The authoritative guide on where and how to validate input. Exercise 5's note about server-side validation is expanded here into a full decision framework.
