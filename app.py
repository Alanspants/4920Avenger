from flask import Flask, render_template, session
from flask import request, redirect
from modles.money import Money
from modles.user import User
from modles.database import Database

app = Flask(__name__)
app.secret_key = "Alan "
Database.initialize()


@app.route("/")
def home():
    moneydict, position = Money.search_data()
    return render_template("home.html", moneydict=moneydict)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['InputName']
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        result = User.register_user(name, email, password)
        if result is True:
            session['email'] = email
            session['name'] = name
            # session['password'] = password
            return redirect("/")
        else:
            message = "Your email address has already been registed."
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        result = User.check_user(email, password)
        if result is True:
            print(True)
            session['email'] = email
            session['name'] = User.find_user_data(email)['name']
            # session['password'] = password
            return redirect("/")
        else:
            message = "Wrong email address or password"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session['email'] = None
    session['name'] = None
    return redirect("/")


@app.route("/change_email", methods=['GET', 'POST'])
def change_email():
    if session['email']:
        if request.method == "POST":
            new_email = request.form['InputNewEmail']
            password = request.form['InputPassword']
            result = User.check_user(session['email'], password)
            if result is True:
                User.update_user_email(session['email'], new_email)
                session['email'] = new_email
                message = "Your new email address {}".format(new_email)
                return render_template("change_email.html", message=message)
            else:
                message = "Wrong password"
                return render_template("change_email.html", message=message)
        else:
            return render_template("change_email.html")
    else:
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, port=4100)
