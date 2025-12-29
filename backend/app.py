from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT,
            author_name TEXT,
            author_initials TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            email TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()

app = Flask(__name__)
CORS(app)

@app.get('/api/health')
def health():
    return jsonify({"status": "ok"})

@app.get('/api/news')
def list_news():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, date, author_name, author_initials, created_at FROM news ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.post('/api/news')
def create_news():
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    content = data.get('content')
    date = data.get('date')
    author_name = data.get('author_name')
    author_initials = data.get('author_initials')
    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO news (title, content, date, author_name, author_initials) VALUES (?,?,?,?,?)",
        (title, content, date, author_name, author_initials)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({"id": new_id}), 201

@app.put('/api/news/<int:item_id>')
def update_news(item_id):
    data = request.get_json(silent=True) or {}
    fields = ['title', 'content', 'date', 'author_name', 'author_initials']
    sets = []
    values = []
    for f in fields:
        if f in data:
            sets.append(f"{f} = ?")
            values.append(data[f])
    if not sets:
        return jsonify({"error": "no fields to update"}), 400
    values.append(item_id)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"UPDATE news SET {', '.join(sets)} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return jsonify({"updated": True})

@app.delete('/api/news/<int:item_id>')
def delete_news(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"deleted": True})

@app.post('/api/auth/login')
def login():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    role = data.get('role', 'user')
    email = data.get('email')
    if not name:
        return jsonify({"error": "name is required"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, role, email) VALUES (?,?,?)", (name, role, email))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return jsonify({"id": user_id, "name": name, "role": role, "email": email})

if __name__ == '__main__':
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_db()
    # Use PORT env for Cloud Run, default 8080; bind to all interfaces
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)