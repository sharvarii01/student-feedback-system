from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            name TEXT,
            message TEXT
        )
    ''')
    conn.close()

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
    conn.commit()
    conn.close()
    
    return "Feedback Submitted!"

@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    
    return render_template('view.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)