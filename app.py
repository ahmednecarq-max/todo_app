from flask import Flask, render_template_string, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Veritabanı dosyası konteyner içinde /app klasöründe
DB = "todo.db"

HTML = """
<!doctype html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body { font-family: Arial; max-width: 500px;
               margin: 60px auto; background: #f9f9f9; }
        h1   { color: #333; }
        input[type=text] { width: 70%; padding: 10px;
                           font-size: 15px; border: 1px solid #ddd;
                           border-radius: 6px; }
        button { padding: 10px 16px; background: #4CAF50;
                 color: white; border: none;
                 border-radius: 6px; cursor: pointer; }
        ul { list-style: none; padding: 0; margin-top: 20px; }
        li { background: white; padding: 12px 16px;
             margin: 6px 0; border-radius: 8px;
             display: flex; justify-content: space-between;
             align-items: center;
             box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        li.bitti { text-decoration: line-through; color: #aaa; }
        .sil { background: #e74c3c; color: white;
               border: none; padding: 5px 10px;
               border-radius: 4px; cursor: pointer; }
        .bitti-btn { background: #3498db; color: white;
                     border: none; padding: 5px 10px;
                     border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>📝 Yapılacaklar</h1>

    <form method="POST" action="/ekle">
        <input type="text" name="gorev" placeholder="Yeni görev ekle..." required>
        <button type="submit">Ekle</button>
    </form>

    <ul>
        {% for id, gorev, bitti in gorevler %}
        <li class="{{ 'bitti' if bitti else '' }}">
            {{ gorev }}
            <div>
                <form method="POST" action="/tamamla/{{ id }}" style="display:inline">
                    <button class="bitti-btn">✓</button>
                </form>
                <form method="POST" action="/sil/{{ id }}" style="display:inline">
                    <button class="sil">✕</button>
                </form>
            </div>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

def baglan():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gorevler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gorev TEXT,
            bitti INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn

@app.route("/")
def index():
    conn = baglan()
    gorevler = conn.execute(
        "SELECT id, gorev, bitti FROM gorevler ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template_string(HTML, gorevler=gorevler)

@app.route("/ekle", methods=["POST"])
def ekle():
    gorev = request.form.get("gorev")
    if gorev:
        conn = baglan()
        conn.execute("INSERT INTO gorevler (gorev) VALUES (?)", (gorev,))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/tamamla/<int:id>", methods=["POST"])
def tamamla(id):
    conn = baglan()
    conn.execute("UPDATE gorevler SET bitti=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/sil/<int:id>", methods=["POST"])
def sil(id):
    conn = baglan()
    conn.execute("DELETE FROM gorevler WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
