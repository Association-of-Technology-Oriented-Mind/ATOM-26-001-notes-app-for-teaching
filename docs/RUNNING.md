# 🚀 Setup & Execution Guide

This document provides step-by-step instructions on how to set up, activate, run, and test the Notes Application across different operating systems (**macOS / Linux** and **Windows**).

---

## 📋 Prerequisites

Ensure you have Python 3 installed on your system:
- **macOS / Linux**: Python 3 is typically pre-installed (`python3 --version`).
- **Windows**: Download Python 3 from [python.org](https://www.python.org/downloads/). Ensure you check **"Add Python to PATH"** during installation.

---

## 🛠️ Step-by-Step Setup Guide

### 1. Open Terminal or Command Prompt
Open your command line interface and navigate to the project root directory:

```bash
cd ATOM-26-001-notes-app-for-teaching
```

---

### 2. Create a Virtual Environment (`venv`)

Creating a virtual environment isolates project dependencies from your system's global Python installation.

- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```

- **Windows (Command Prompt / PowerShell):**
  ```cmd
  python -m venv venv
  ```

---

### 3. Activate the Virtual Environment

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

- **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate
  ```

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

*(Once activated, your terminal prompt will display a `(venv)` prefix).*

---

### 4. Install Project Dependencies

Install the required Python packages specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Note:** SQLite is included in Python's standard library (`sqlite3`), so no external database driver needs to be installed!

---

### 5. Start the Flask Application Server

Run the Flask server script:

```bash
python app.py
```

**Expected Startup Output:**
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

> **Automatic DB Initialization**: On launch, Flask automatically checks if `notes.db` exists. If not, it creates the database and initializes the `notes` table automatically.

---

### 6. Open Application in Web Browser

Open your web browser and navigate to:

```text
http://127.0.0.1:5000/
```

---

## 🧪 Testing Application Functionality

You can verify that the application and database functions are working properly by running the Python test suite:

```bash
python -c "
from app import app, fetch_all_notes, insert_note

with app.app_context():
    notes = fetch_all_notes()
    print(f'Current total notes in database: {len(notes)}')
"
```

---

## 🔧 Troubleshooting & Common Issues

### Issue 1: `Address already in use` (Port 5000 Conflict)
If port 5000 is occupied by another process:
- **Workaround**: Modify the last line in `app.py` to use another port, e.g., `port=5001`:
  ```python
  if __name__ == '__main__':
      app.run(debug=True, port=5001)
  ```

### Issue 2: `script execution is disabled on this system` (Windows PowerShell)
PowerShell may block running activate scripts due to execution policy:
- **Solution**: Run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy Unrestricted -Scope Process
  ```
  Then run `.\venv\Scripts\Activate.ps1` again.

### Issue 3: Resetting the Database
If you wish to clear all notes and start with a fresh database:
1. Stop the Flask server (`Ctrl + C`).
2. Delete the `notes.db` file:
   - **Linux / macOS**: `rm notes.db`
   - **Windows**: `del notes.db`
3. Restart the server with `python app.py`. `notes.db` will be recreated automatically.
