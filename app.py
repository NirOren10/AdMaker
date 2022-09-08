import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# from django.utils import simplejson


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-reanswer_valueidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mental.db")
questions = db.execute("SELECT * FROM questions")

answers = []

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    global answers
    answers = []
    if request.method == "POST":
        return render_template("index.html")
    else:
        return render_template("index.html")




#----------------



@app.route("/questionnare", methods=["GET", "POST"])
@login_required
def questionnare():
    global answers
    answers = []
    if request.method == "POST":
        for q in questions:
            temp = []
            for i in range(q['answer_spaces']):
                answers = db.execute("SELECT * FROM answers WHERE user_id = ? AND question_id = ? AND answer_number=?", session['user_id'], q['id'],i)
                answer_value = request.form.get(str(q['question'])+str(i))
                temp.append(answer_value)
                if len(answers)==0:
                    print('01')
                    db.execute('INSERT INTO answers (user_id, question_id,answer, answer_number) VALUES(?,? , ?, ?)',
                    session["user_id"],
                    q['id'],
                    answer_value,
                    i) 
                else:
                    db.execute('UPDATE answers SET answer=? WHERE id = ?',
                    answer_value,
                    answers[0]['id'])
            
            answers.append(temp)
        return redirect("/")
    else:
        text_fillers = []
        for q in questions:
            temp = []
            for i in range(q['answer_spaces']):
                answers = db.execute("SELECT * FROM answers WHERE user_id = ? AND question_id = ? AND answer_number = ?", session['user_id'], q['id'],i)
                answer_value = answers[0]['answer']
                temp.append(answer_value)
            text_fillers.append(temp)

        return render_template("questionnare.html",questions = questions, text_fillers = text_fillers)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        ERROR = ' '
        # Ensure username was submitted
        if not request.form.get("email"):
            flash("must provide email")
            return render_template("login.html")
            #return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")
            #return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid email and/or password")
            return render_template("login.html")
            #return apology("inanswer_valueid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        ERROR=' '
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ERROR = ' '
        username = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('confirmation')
        email = request.form.get('email')

        if not request.form.get("email"):
            ERROR = "must provide email"
            return render_template("register.html", ERROR=ERROR)

            #return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            ERROR = "must provide password"
            flash('retype passwords')
            return render_template("register.html", ERROR=ERROR)
            #return apology("must provide password", 400)

        elif request.form.get("confirmation") is None:
            ERROR ="must retype password"
            flash('retype passwords')
            return render_template("register.html", ERROR=ERROR)
            #return apology("must retype password", 400)

        if password != repassword:
            ERROR ="passwords dont match"
            flash('passwords dont match')
            return render_template("register.html", ERROR=ERROR)
            #return apology("passwords dont match", 400)
        # Ensure username exists and password is correct

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(rows) != 0:
            ERROR ="email exists in system"
            flash('email exists')
            return render_template("register.html", ERROR=ERROR)
            #return apology("Username exists in system", 400)

        else:
            hashed_password = generate_password_hash(password)
            db.execute('INSERT INTO users (email, hash) VALUES(? , ?)',
            username,
            hashed_password)
            return redirect('/')

    else:
        return render_template("register.html")





@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    global txt
    if request.method == "POST":
        flash("Sold!")
        return redirect("/results")
    else:
        return render_template("testy.html", questions = questions)
 

txt = ''

@app.route("/paragraph", methods=["GET", "POST"])
@login_required
def paragraph():
    results = []
    global txt
    global answers
    if request.method == "POST":
        date = 'None'
        date = request.args.get('date', default=0, type=str)
        print('DATE:', date)
        txt = request.form.get("txt")

        db.execute('INSERT INTO posts (user_id, date,text) VALUES(? , ?,?)',
            session['user_id'],
            date,
            txt)
                
        return render_template('index.html')
    else:
        date = 0
        date = request.args.get('date', default=0, type=str)
        print('DATE:', date)
        txt = db.execute("SELECT * FROM posts WHERE user_id = ? AND date = ?", session['user_id'], date)
        answers = db.execute("SELECT * FROM answers WHERE user_id = ?", session['user_id'])
        
        if len(txt) == 0:
            txt = ''
        else:
            txt = txt[0]['text']

        questions_and_answers = {}
        lst = []
        string = ''
        for i in questions:
            specific_answers = db.execute("SELECT * FROM answers WHERE user_id = ? and question_id = ?", session['user_id'],i['id'])
            questions_and_answers[i['question']] = [i['answer'] for i in specific_answers if i['answer'] != 'None']
            lst.append(i['question'])
            string+=i["question"]+','

        return render_template("paragraph.html", questions_str = string, answers=answers,questions_and_answers=questions_and_answers,txt=txt)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)