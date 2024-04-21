from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    open_date = request.form['openDate']

    conn = sqlite3.connect('timecrypt.db')
    c = conn.cursor()
    c.execute('INSERT INTO Users (Name, Email, Phone) VALUES (?, ?, ?)', (name, email, phone))
    user_id = c.lastrowid
    time_capsule_id = f"{user_id}-{open_date.replace('-', '')}"
    c.execute('INSERT INTO TimeCapsules (TimeCapsuleID, UserID, OpenDate) VALUES (?, ?, ?)', (time_capsule_id, user_id, open_date))
    upload_date = datetime.now().strftime("%Y%m%d%H%M%S")
    memory_id = f"{time_capsule_id}-{upload_date}"
    c.execute('INSERT INTO Memories (MemoryID, TimeCapsuleID, FilePath, UploadDate) VALUES (?, ?, ?, ?)', (memory_id, time_capsule_id, '', datetime.now()))
    conn.commit()
    conn.close()
    return 'Data submitted successfully!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
