import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


questions = [
    ['מה הוואו פקטור שלך- עד 5 וקח זמן לחשוב',5],
    ['שלושה מתחרים.',3],
    ['מה היתרונות של המתחרים שלך',3],
    ['מה החסרונות של המתחרים שלך',3],
    ['מה היתרונות שלך לעומתם- איפה אתה טוב יותר',3],
    ['מה הכי היית רוצה שידעו עלייך',3],
    ['האם לקהל ספציפי או יותר רחב',1]
]

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
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

answers = []


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    global answers
    answers = []
    if request.method == "POST":
        
        for q in questions:
            temp = []
            for i in range(q[1]):
                val = request.form.get(str(q[0])+str(i))
                if val != "":
                    temp.append(val)
                #print(val)
            answers.append(temp)
        print(answers)
        return render_template("paragraph.html")
    else:
        return render_template("index.html",questions = questions)




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
            #return apology("invalid username and/or password", 403)

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
        txt = request.form.get("txt")
        for i in range(len(answers)):
            temp = []
            for a in answers[i]:
                if txt.count(a) > 0:
                    temp.append([a,txt.count(a)])
                else:
                    print(a, 0)
                    temp.append([a,f'<span style="color: #ff0000">{txt.count(a)}</span>'])
            results.append([questions[i][0],temp])
        return render_template('results.html', results = results, txt=txt,questions = questions)
    else:
        return render_template("paragraph.html")


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