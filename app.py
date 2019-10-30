from flask import Flask, render_template, session
from flask import request, redirect
from modles.money import Money
from modles.user import User
from modles.database import Database
from modles.all_alert import All_alert

app = Flask(__name__)
app.secret_key = "Alan "
Database.initialize()


@app.before_first_request
def initialize():
    Database.initialize()
    session["email"] = session.get("email")
    session["name"] = session.get("name")


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


@app.route("/new_alert", methods=["GET", "POST"])
def new_alert():
    if session['email']:
        moneydict, position = Money.search_data()
        if request.method == "POST":
            input_currency = request.form['input_currency']
            rate_exchange = request.form['rate_exchange']
            bank_buy = request.form['bank_buy']
            bank_sale = request.form['bank_sale']

            result = All_alert.create_alert(session['email'], input_currency, rate_exchange, [bank_buy, bank_sale])

            if result is True:
                message = "Successfully adding new notification"
                currency_msg = "Currency: {}".format(input_currency)
                exchange_msg = "Exchange Rate: {}".format("cash" if rate_exchange == "cash" else "sale")
                buy_msg = "Bank buy price: {}".format(bank_buy)
                sale_msg = "Bank sale price: {}".format(bank_sale)
                return render_template("new_alert.html", moneydict=moneydict, message=message, currency=currency_msg,
                                       exchange_msg=exchange_msg, buy_msg=buy_msg, sale_msg=sale_msg)
            else:
                message = "Adding new notification fail, you already has a same notification!"
                currency_msg = "Currency: {}".format(input_currency)
                exchange_msg = "Exchange Rate: {}".format("cash" if rate_exchange == "cash" else "sale")
                buy_msg = "Bank buy price: {}".format(bank_buy)
                sale_msg = "Bank sale price: {}".format(bank_sale)
                return render_template("new_alert.html", moneydict=moneydict, message=message,
                                       currency=currency_msg,
                                       exchange_msg=exchange_msg, buy_msg=buy_msg, sale_msg=sale_msg)
        else:
            return render_template("new_alert.html", moneydict=moneydict)
    else:
        return redirect("/login")


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

@app.route("/cash_alert")
def cash_alert():
    if session["email"]:
        cash_data = All_alert.find_user_alert(session["email"],"cash")
        return render_template("cash_alert.html", cash_data=cash_data)
    else:
        return redirect("/login")

@app.route("/sign_alert")
def sign_alert():
    if session["email"]:
        sign_data = All_alert.find_user_alert(session["email"],"sign")
        return render_template("sign_alert.html", sign_data=sign_data)
    else:
        return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True, port=4100)
