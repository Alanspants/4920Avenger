from flask import Flask, render_template, request, redirect, session
from modules.money import Money
from modules.user import  User
from modules.database import Database
from modules.All_alert import All_alert
app = Flask(__name__)
app.secret_key = "123123123"

@app.before_first_request
def initialize():
    Database.initialize()
    session["email"] = session.get("email")
    session["name"] = session.get("name")


@app.route("/")
def home():
    moneydict, position = Money.search_data()
    return render_template('home.html', moneydict=moneydict)

@app.route("/cash_alert")
def cash_alert():
    if session['email']:
        find = All_alert.find_user_alert(session["email"])
        return render_template("cash_alert.html", find=find)
    else:
        return redirect("/login")

@app.route("/update_alert", methods=["POST"])
def update_alert():
    if request.method == "POST":
        bank_buy = request.form["bank_buy"]
        bank_sell = request.form["bank_sell"]
        currency = request.form["currency"]
        All_alert.update_user_alert(session["email"], currency, [bank_buy, bank_sell])
        return redirect("/cash_alert")

@app.route("/delete_alert", methods=["POST"])
def delete_alert():
    if request.method == "POST":
        currency = request.form["currency"]
        All_alert.delete_user_alert(session["email"], currency)
        return redirect("/cash_alert")

@app.route("/new_alert", methods=["GET", "POST"])
def new_alert():
    if session['email']:
        moneydict, position = Money.search_data()
        if request.method == 'POST':
            input_currency = request.form['input_currency']
            buy_rate = request.form['buy_rate']
            sell_rate = request.form['sell_rate']

            result = All_alert.create_alert(session['email'], input_currency, [buy_rate, sell_rate])
            if result is True:
                message = "Wow! Reminder added successfully!"
                currency_msg = "Currency Type: {}".format(input_currency)
                buy_msg = "Buy Rate: ${}".format(buy_rate)
                sell_msg = "Sell Rate: ${}".format(sell_rate)
                return render_template("new_alert.html", moneydict=moneydict, message=message, currency_msg=currency_msg, buy_msg=buy_msg, sell_msg=sell_msg)
            else:
                message = "Oops! Reminder added unsuccessfully !"
                currency_msg = "Currency Type : {}".format(input_currency)
                buy_msg = "Buy Rate: ${}".format(buy_rate)
                sell_msg = "Sell Rate: ${}".format(sell_rate)
                return render_template("new_alert.html", moneydict=moneydict, message=message,
                                       currency_msg=currency_msg, buy_msg=buy_msg, sell_msg=sell_msg)
        else:
            return render_template("new_alert.html", moneydict=moneydict)
    else:
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['nameIn']
        email = request.form['emailIn']
        password = request.form['passwordIn']
        result = User.register_user(name, email, password)
        if result is True:
            session['email'] = email
            session['name'] = name
            return redirect("/")
        else:
            message = "Oops! This email may have been registered!"
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailIn']
        password = request.form['passwordIn']
        result = User.check_user(email, password)
        if result is True:
            session['email'] = email
            session['name'] = User.find_user_data(email)['name']
            return redirect("/")
        else:
            message = "The email or password may be wrong"
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session['name'] = None
    session['email'] = None
    return redirect("/")



@app.route("/change_email", methods=['GET', 'POST'])
def change_email():
    if session['email']:
        if request.method == 'POST':
            new_email = request.form['newEmail']
            password = request.form['passwordIn']
            result = User.check_user(session['email'], password)
            if result is True:
                User.update_user_email(session['email'], new_email)
                session['email'] = new_email
                message = "Your new email {} is reset".format(new_email)
                return render_template("change_email.html", message=message)
            else:
                message = "Oops! The password or email address may be wrong!"
                return render_template("change_email.html", message=message)
        else:
            return render_template("change_email.html")
    else:
        return redirect("/login")


if __name__== "__main__":
  app.run()