from flask import Flask, render_template, request, g, redirect, request, flash, url_for, session


import sqlite3
import random
import string

app = Flask(__name__)

def get_message_db():
    if 'db' not in g:
        g.message_db = sqlite3.connect('messages.sqlite')
    
    cmd = \
    "CREATE TABLE IF NOT EXISTS messages(message_id INTEGER PRIMARY KEY, handle TEXT NOT NULL, message TEXT NOT NULL)"
    g.message_db.execute(cmd)
    g.message_db.commit()

    return g.message_db

def insert_message(request):
    handle = request.form['handle']
    message = request.form['message']
    db = get_message_db()
    cur = db.cursor()
    error = None

    if error is None:
        cur.execute("SELECT * FROM messages")
        message_id = len(cur.fetchall())+1

        db.execute(
            'INSERT INTO messages (message_id, handle, message) VALUES (?, ?, ?)',
            (message_id, handle, message)
            )
        db.commit()
        # flash('Congrats! You have successfully submitted your message.')
        return redirect(url_for('main'))


    db = g.pop('message_db', None)
    if db is not None:
        db.close()

    return render_template('base.html')

def random_messages(n):
    db = get_message_db()
    cur = db.cursor()
    cmd = "SELECT * from messages order by RANDOM() LIMIT ?"
    result = cur.execute(cmd, (n,))
    result = cur.fetchall()

    db = g.pop('message_db', None)
    if db is not None:
        db.close()

    return result


@app.route("/")
def main():
    return render_template("base.html")

@app.route("/submit/", methods = ["POST", "GET"])
def submit():
    if request.method == "GET":
        return render_template("submit.html")
    else:
        handle = request.form["handle"],
        message = request.form["message"]
        insert_message(request)
        return render_template("submit.html")




@app.route("/view/")
def view():
    messages = random_messages(3)
    return render_template('view.html', db = messages)




        