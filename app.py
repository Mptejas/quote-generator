from flask import Flask, jsonify
import requests
import sqlite3

app = Flask(__name__)

# Create DB
conn = sqlite3.connect('quotes.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS history
                  (id INTEGER PRIMARY KEY, quote TEXT, author TEXT)''')

@app.route('/quote')
def get_quote():
    res = requests.get("https://api.quotable.io/random")
    data = res.json()

    quote = data['content']
    author = data['author']

    cursor.execute("INSERT INTO history (quote, author) VALUES (?, ?)", (quote, author))
    conn.commit()

    return jsonify({"quote": quote, "author": author})

@app.route('/history')
def history():
    cursor.execute("SELECT quote, author FROM history")
    rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
