# 🗄️ Database Schema & Routes Reference

This document provides a technical reference for the SQLite database schema, parameterized SQL queries, Flask routes, input validation rules, and security protections.

---

## 🗄️ Database Schema (`notes.db`)

The application automatically creates and manages a single SQLite table named `notes`.

### SQL Table Schema: `notes`
```sql
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Data Dictionary

| Field Name | Type | Key | Nullable | Description | Example Value |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `id` | `INTEGER` | `PK` | No | Auto-incremented note primary key | `1` |
| `title` | `TEXT` | - | No | Title of the note | `"Study Flask Routing"` |
| `content` | `TEXT` | - | No | Detailed note body content | `"Learn GET and POST routes..."` |
| `created_at` | `TEXT` | - | No | Creation timestamp (`YYYY-MM-DD HH:MM:SS`) | `"2026-09-02 10:15:00"` |
| `updated_at` | `TEXT` | - | No | Last update timestamp (`YYYY-MM-DD HH:MM:SS`) | `"2026-09-02 10:20:00"` |

---

## 🔒 Parameterized SQL Queries

To prevent **SQL Injection**, all database interactions in `app.py` use parameterized placeholders (`?`).

```python
# 1. Fetch All Notes
SELECT * FROM notes ORDER BY updated_at DESC;

# 2. Fetch Note by ID
SELECT * FROM notes WHERE id = ?;

# 3. Insert New Note
INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?);

# 4. Update Existing Note
UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?;

# 5. Delete Note
DELETE FROM notes WHERE id = ?;

# 6. Search Notes by Title or Content
SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC;
```

---

## 🗺️ Application Routes Reference

| HTTP Method | Route URL | Controller Function | Input Parameters | Success Action / Response | Error Behavior |
| :---: | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | `index()` | None | Renders `templates/index.html` with note list | Catches DB error, flashes alert |
| `GET` | `/note/<id>` | `view_note(id)` | `id` (int) | Renders `templates/note.html` with note details | 404 page if note ID invalid |
| `POST` | `/add` | `add_note()` | `title`, `content` | Inserts note & redirects to `/` with success flash | Flashes error if inputs empty |
| `GET` | `/edit/<id>` | `edit_note(id)` | `id` (int) | Renders `templates/edit.html` pre-filled | 404 page if note ID invalid |
| `POST` | `/edit/<id>` | `edit_note(id)` | `id` (int), `title`, `content` | Updates note & redirects to `/` with success flash | Flashes error if inputs empty |
| `POST` | `/delete/<id>` | `delete_note(id)` | `id` (int) | Deletes note & redirects to `/` with success flash | 404 page if note ID invalid |
| `GET` | `/search` | `search()` | `q` (string) | Renders `index.html` with filtered notes | Redirects to `/` if search empty |

---

## 🛡️ Input Validation & Security Rules

1. **Title Validation**:
   - Must not be empty after trimming leading and trailing whitespace.
   - Client-side length restricted to maximum 100 characters.
2. **Content Validation**:
   - Must not be empty after trimming whitespace.
3. **Parameter Sanitization**:
   - Jinja2 automatically escapes HTML tags inside `{{ }}` expressions, neutralizing Cross-Site Scripting (XSS).
4. **Invalid Note ID Handling**:
   - Attempting to access or edit non-existent IDs returns a user-friendly 404 page rather than throwing server crashes.
