import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)

# Secret key required for Flask flash messages
app.secret_key = 'teaching-notes-app-secret-key'

DATABASE_NAME = 'notes.db'


def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    row_factory allows column access by name (e.g., note['title']).
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Automatically creates the 'notes' table if it does not exist.
    Called when the Flask application starts up.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Ensure database and table exist upon app initialization
with app.app_context():
    init_db()


# ==========================================
# Database Helper Functions (Modular & Future AI Ready)
# ==========================================

def fetch_all_notes():
    """Retrieves all notes ordered by last updated date descending."""
    conn = get_db_connection()
    notes = conn.execute(
        'SELECT * FROM notes ORDER BY updated_at DESC'
    ).fetchall()
    conn.close()
    return notes


def fetch_note_by_id(note_id):
    """Retrieves a single note by its ID."""
    conn = get_db_connection()
    note = conn.execute(
        'SELECT * FROM notes WHERE id = ?', (note_id,)
    ).fetchone()
    conn.close()
    return note


def insert_note(title, content):
    """Creates a new note with timestamps."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)',
        (title, content, now, now)
    )
    conn.commit()
    conn.close()


def update_note_in_db(note_id, title, content):
    """Updates an existing note's title, content, and updated_at timestamp."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    conn.execute(
        'UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?',
        (title, content, now, note_id)
    )
    conn.commit()
    conn.close()


def delete_note_from_db(note_id):
    """Deletes a note by its ID."""
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM notes WHERE id = ?', (note_id,)
    )
    conn.commit()
    conn.close()


def search_notes_in_db(query):
    """Searches notes by matching query against title or content."""
    conn = get_db_connection()
    search_pattern = f'%{query}%'
    notes = conn.execute(
        'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY updated_at DESC',
        (search_pattern, search_pattern)
    ).fetchall()
    conn.close()
    return notes


# ==========================================
# Routes & Controllers
# ==========================================

@app.route('/')
def index():
    """GET / -> Display all notes."""
    try:
        notes = fetch_all_notes()
        return render_template('index.html', notes=notes)
    except sqlite3.Error as e:
        flash(f"Database error: {str(e)}", "error")
        return render_template('index.html', notes=[])


@app.route('/note/<int:id>')
def view_note(id):
    """GET /note/<id> -> Display a single note in detail."""
    try:
        note = fetch_note_by_id(id)
        if note is None:
            flash("Note not found.", "error")
            return render_template('404.html'), 404
        return render_template('note.html', note=note)
    except sqlite3.Error as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/add', methods=['POST'])
def add_note():
    """POST /add -> Create a new note."""
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    # Backend Validation
    if not title:
        flash("Title cannot be empty.", "error")
        return redirect(url_for('index'))
    if not content:
        flash("Content cannot be empty.", "error")
        return redirect(url_for('index'))

    try:
        insert_note(title, content)
        flash("Note created successfully!", "success")
    except sqlite3.Error as e:
        flash(f"Failed to create note: {str(e)}", "error")

    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    """
    GET /edit/<id>  -> Render edit form with existing note data.
    POST /edit/<id> -> Update note with new title/content.
    """
    note = fetch_note_by_id(id)
    if note is None:
        flash("Note not found.", "error")
        return render_template('404.html'), 404

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        # Backend Validation
        if not title:
            flash("Title cannot be empty.", "error")
            return render_template('edit.html', note=note)
        if not content:
            flash("Content cannot be empty.", "error")
            return render_template('edit.html', note=note)

        try:
            update_note_in_db(id, title, content)
            flash("Note updated successfully!", "success")
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            flash(f"Failed to update note: {str(e)}", "error")

    return render_template('edit.html', note=note)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    """POST /delete/<id> -> Delete a note by ID."""
    note = fetch_note_by_id(id)
    if note is None:
        flash("Note not found.", "error")
        return render_template('404.html'), 404

    try:
        delete_note_from_db(id)
        flash("Note deleted successfully!", "success")
    except sqlite3.Error as e:
        flash(f"Failed to delete note: {str(e)}", "error")

    return redirect(url_for('index'))


@app.route('/search')
def search():
    """GET /search -> Search notes by title or content."""
    query = request.args.get('q', '').strip()
    
    if not query:
        flash("Please enter a search term.", "info")
        return redirect(url_for('index'))

    try:
        notes = search_notes_in_db(query)
        return render_template('index.html', notes=notes, search_query=query)
    except sqlite3.Error as e:
        flash(f"Search error: {str(e)}", "error")
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Custom 500 error handler."""
    flash("An unexpected server error occurred.", "error")
    return render_template('index.html', notes=[]), 500


if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True, port=5000)
