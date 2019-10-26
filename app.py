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
    return render_template("home.html", moneydict = moneydict)

@app.route("/register", methods=['GET','POST'])
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
            return render_template("register.html",message=message)
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True, port=4100)
