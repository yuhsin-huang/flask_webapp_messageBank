from flask import Flask, render_template, request, g, redirect, request, url_for
import sqlite3

app = Flask(__name__)

def get_message_db():
    # connect the database message_db
    if 'db' not in g:
        g.message_db = sqlite3.connect('messages.sqlite')
    
    # create a table if there isn't one in the database, colomns include message_id, handle, and message
    # after the column name, specify the data type and constraints
    # not null means that the column does not accept NULL value, and primary key means that the value must be unique
    cmd = \
    "CREATE TABLE IF NOT EXISTS messages(message_id INTEGER PRIMARY KEY, handle TEXT NOT NULL, message TEXT NOT NULL)"
    g.message_db.execute(cmd)
    
    return g.message_db

def insert_message(request):
    # values of handle and message come from the user's input (request)
    handle = request.form['handle']
    message = request.form['message']

    # get the database connection and cursor
    db = get_message_db()
    cur = db.cursor()
    error = None

    if error is None:
        # message_id is the row length of the table in the database + 1
        cur.execute("SELECT * FROM messages")
        message_id = len(cur.fetchall())+1

        # insert new message_id, handle, and message values into the database table
        db.execute(
            'INSERT INTO messages (message_id, handle, message) VALUES (?, ?, ?)',
            (message_id, handle, message)
            )
        
        # it is necessary to run db.commit() to ensure that the row insertion has been saved
        db.commit()

        return redirect(url_for('main'))

    # close the connection
    db = g.pop('message_db', None)
    if db is not None:
        db.close()

    return render_template('base.html')


def random_messages(n):
    # get the database connection and cursor
    db = get_message_db()
    cur = db.cursor()

    # randomly select n rows from the database
    cmd = "SELECT * from messages order by RANDOM() LIMIT ?"
    result = cur.execute(cmd, (n,))
    result = cur.fetchall()

    # close the connection
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




        