# 🛠️ Technology Stack & Teaching Rationale

This document provides a detailed breakdown of the technologies used in the Notes Application and explains why each component was chosen for educational purposes.

---

## 🥞 Stack Overview

| Layer | Component | Package / Module |
| :--- | :--- | :--- |
| **Language** | Python 3 | Standard Library |
| **Backend Web Framework** | Flask | `Flask==3.0.3` |
| **Database Engine** | SQLite 3 | `sqlite3` (Python Standard Library) |
| **Templating Engine** | Jinja2 | Included with Flask |
| **Frontend Styling** | Vanilla CSS3 | Custom Properties & CSS Grid |
| **Frontend Logic** | Vanilla JavaScript | ES6+ Standard DOM APIs |
| **Virtual Environment** | Python `venv` | Built-in Python Tool |

---

## 🎯 Detailed Rationale for Teaching

### 1. Python + Flask
- **Why Flask?** Flask is a micro-framework that provides only the essential tools needed to build a web application (routing, request handling, and template rendering).
- **Teaching Benefit**: Unlike monolithic frameworks (like Django) that hide low-level details under complex magic and ORMs, Flask allows students to clearly see how an HTTP request hits a route function, interacts with Python logic, and returns an HTML response.

---

### 2. Built-in SQLite (`sqlite3`)
- **Why `sqlite3`?** SQLite is a lightweight, serverless, file-based SQL database built directly into Python's standard library.
- **Teaching Benefit**: 
  - Students do not need to install or configure external database servers (like PostgreSQL or MySQL).
  - Writing raw SQL queries using parameterized placeholders (`?`) teaches students standard SQL syntax and fundamental security concepts (preventing SQL Injection).

---

### 3. Jinja2 Templating
- **Why Jinja2?** Jinja2 is Flask's default template engine. It allows server-side rendering (SSR) of dynamic data inside standard HTML templates.
- **Teaching Benefit**: Students learn how dynamic web pages are rendered on the server before being sent to the client browser using expressions (`{{ note.title }}`), conditionals (`{% if notes %}`), and loops (`{% for note in notes %}`).

---

### 4. Vanilla CSS3 (Design System)
- **Why Vanilla CSS?** No Tailwind, Bootstrap, or heavy CSS frameworks were used.
- **Teaching Benefit**: 
  - Demonstrates modern CSS features like CSS Custom Properties (variables), Flexbox, CSS Grid, custom modals, and media queries.
  - Keeps students focused on core web design principles rather than learning proprietary framework class names.

---

### 5. Vanilla JavaScript (ES6+)
- **Why Vanilla JS?** No React, Vue, or frontend frameworks were used.
- **Teaching Benefit**:
  - Teaches fundamental DOM manipulation (`document.getElementById`), browser event listeners (`addEventListener`), dynamic character counting, input trimming, and modal dialog toggles.
  - Helps students understand what browser APIs do natively before introducing complex JavaScript frameworks.

---

### 6. Python Virtual Environment (`venv`)
- **Why `venv`?** `venv` creates an isolated directory for Python packages.
- **Teaching Benefit**: Teaches standard Python development workflows, dependency management (`requirements.txt`), and preventing version conflicts across different projects.
