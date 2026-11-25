import os
import time
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "notesdb"),
        user=os.environ.get("DB_USER", "notes"),
        password=os.environ.get("DB_PASSWORD", "notes"),
    )

def init_db():
    # Veritabani hazir olana kadar birkac kez dene
    for _ in range(10):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS notes ("
                "id SERIAL PRIMARY KEY, text TEXT NOT NULL)"
            )
            conn.commit()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(2)

init_db()

@app.route("/")
def home():
    return jsonify(message="Merhaba! Mini Platform calisiyor.")

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/load")
def load():
    start = time.time()
    while time.time() - start < 0.5:
        sum(i * i for i in range(10000))
    return jsonify(message="CPU yuklendi")

@app.route("/notes", methods=["GET"])
def list_notes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM notes ORDER BY id")
    rows = [{"id": r[0], "text": r[1]} for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/notes", methods=["POST"])
def add_note():
    text = (request.get_json(silent=True) or {}).get("text")
    if not text:
        return jsonify(error="text alani gerekli"), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (text) VALUES (%s) RETURNING id", (text,))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify(id=new_id, text=text), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
