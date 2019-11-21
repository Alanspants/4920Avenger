from flask import Flask, request, render_template, session, redirect, jsonify
from backends.database import Database as db
from backends.email_send import get_reminder
from apscheduler.schedulers.background import BackgroundScheduler
from backends.currency import Source
from backends.user import User
from backends.reminder import Reminder
from bs4 import BeautifulSoup
from backends.calculator import convert
from backends.watch_list import WatchList
from backends.game import Game
from backends.gamer import Gamer
import requests
import json
import sys
from backends.data import getData
from backends.rank import rank

soup = BeautifulSoup('calculator.html', 'html.parser')
import datetime

app = Flask(__name__)
# app.config['SECRET_KEY']=os.urandom(24)
app.secret_key = "123123123"

gamer = Gamer(None, None)


@app.before_first_request
def setup():
    session["email"] = session.get("email")
    session["name"] = session.get("name")
    session["password"] = session.get("password")
    db.setup()
    # work = BackgroundScheduler(check_alert, "cron", day_of_week="0-4", hour="16", miniute="30")
    work = BackgroundScheduler()
    # work.add_job(check_alert, "interval", seconds=10)
    work.add_job(get_reminder, "interval", seconds=10000000)
    # work.add_job(check_alert, "cron", day_of_week="0-4", hour="18",minute="1")
    work.start()


@app.route("/")
def home():
    currencylist, pos = Source.get_currency()
    watchlist = WatchList.get_watch_list(session['email'])
    codes = WatchList.collect_codes(watchlist)

    if request.method == 'POST':
        code = request.form['history']
        print(code)
        return render_template('search.html')

    return render_template('home.html', currencylist=currencylist, codes=codes)


@app.route("/reminders")
def reminders():
    if session['email']:
        find = Reminder.get_reminder_by_email(session["email"])
        return render_template("reminders.html", find=find)
    else:
        return redirect("/login")


@app.route("/update_reminder", methods=["POST"])
def update_reminder():
    if request.method == "POST":
        get_currency = request.form["currency"]
        sell = request.form["update_sell"]
        buy = request.form["update_buy"]
        Reminder.update_reminder(session["email"], get_currency, [sell, buy])
        return redirect("/reminders")


@app.route("/delete_reminder", methods=["POST"])
def delete_reminder():
    if request.method == "POST":
        get_currency = request.form["currency"]
        Reminder.delete_reminder(session["email"], get_currency)
        return redirect("/reminders")


# new_alert
@app.route("/create_reminder", methods=["GET", "POST"])
def create_reminder():
    if session['email']:
        currencylist, pos = Source.get_currency()
        if request.method == 'POST':
            input_currency = request.form['input_currency']
            buy_rate = request.form['buy_rate']
            sell_rate = request.form['sell_rate']

            result = Reminder.new_reminder(session['email'], input_currency, [sell_rate, buy_rate])
            if result is not True:
                info = "Oops! Reminder added unsuccessfully !"
                curr_info = "Currency Type : {}".format(input_currency)
                buy_info = "Buy Rate: ${}".format(buy_rate)
                sell_info = "Sell Rate: ${}".format(sell_rate)
                return render_template("create_reminder.html", currencylist=currencylist, curr_info=curr_info,
                                       buy_info=buy_info, sell_info=sell_info, info=info)
            else:
                curr_info = "Currency Type: {}".format(input_currency)
                buy_info = "Buy Rate: ${}".format(buy_rate)
                sell_info = "Sell Rate: ${}".format(sell_rate)
                info = "Wow! Reminder added successfully!"
                return render_template("create_reminder.html", currencylist=currencylist, curr_info=curr_info,
                                       buy_info=buy_info, sell_info=sell_info, info=info)
        else:
            return render_template("create_reminder.html", currencylist=currencylist)
    else:
        return redirect("/login")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        currencylist, pos = Source.get_currency()
        name = request.form['nameIn']
        email = request.form['emailIn']
        password = request.form['passwordIn']
        result = User.new_user(name, email, password)

        gamer = Gamer.new_gamer(name, email)

        if result is not True:
            notification = "Oops! This email may have been registered!"
            return render_template("register.html", notification=notification)
        else:
            session['email'] = email
            session['name'] = name
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailIn']
        password = request.form['passwordIn']
        result = User.validation(email, password)
        if result is not True:
            notification = "The email or password may be wrong"
            return render_template("login.html", notification=notification)
        else:
            session['email'] = email
            session['name'] = User.get_user_by_email(email)['name']
            return redirect("/")
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
            password = request.form['passwordIn']
            result = User.validation(session['email'], password)
            new_email = request.form['newEmail']
            if result is not True:
                notification = "Oops! The password or email address may be wrong!"
                return render_template("change_email.html", notification=notification)
            else:
                User.update_user_by_email(session['email'], new_email)
                session['email'] = new_email
                notification = "Your new email {} is reset".format(new_email)
                return render_template("change_email.html", notification=notification)
        else:
            return render_template("change_email.html")
    else:
        return redirect("/login")


@app.route("/calculator", methods=['GET', 'POST'])
def calculator():
    currencylist, pos = Source.get_currency()
    if request.method == 'POST':
        fromCurrency = request.form['from']
        toCurrency = request.form['to']
        fromAmount = request.form['fromAmount']
        # result = fromAmount * 2
        # result = convert(fromCurrency, toCurrency, fromAmount, currencylist, pos)
        # if(fromCurrency == "AUD"):
        #     result = convert(-1, toCurrency, fromAmount, currencylist, pos)
        # elif(toCurrency == "AUD"):
        #     result = convert(fromCurrency, -1, fromAmount, currencylist, pos)
        # else:
        #     result = convert(fromCurrency, toCurrency, fromAmount, currencylist, pos)

        result = convert(fromCurrency, toCurrency, fromAmount, currencylist, pos)
        result_temp = convert(fromCurrency, toCurrency, 1, currencylist, pos)
        return render_template("calculator.html", currencylist=currencylist, from_position=pos[fromCurrency],
                               to_position=pos[toCurrency], from_Amount=fromAmount, to_Amount=result, flag=1,
                               temp_to_Amount=result_temp)
    else:
        initial_result = convert("USD", "AUD", "1", currencylist, pos)
        return render_template("calculator.html", currencylist=currencylist, flag=0, initial_result=initial_result)


@app.route("/watchlist")
def watchlist():
    if session['email']:
        find = WatchList.get_watch_list(session['email'])
        return render_template("watchlist.html", find=find)
    else:
        return redirect("/login")


@app.route("/add_watchlist:<currency>/<code>/<sell_rate>/<buy_rate>")
def add_watchlist(currency, code, sell_rate, buy_rate):
    currencylist, pos = Source.get_currency()
    if session['email']:
        WatchList.new_watchList(session['email'], currency, code, sell_rate, buy_rate)
        watchlist = WatchList.get_watch_list(session['email'])
        codes = WatchList.collect_codes(watchlist)
        return render_template("home.html", codes=codes, currencylist=currencylist)
    else:
        return redirect("/login")


@app.route("/remove_watchlist:<code>")
def remove_watchlist(code):
    if session['email']:
        WatchList.delete_watchList(session['email'], code)
        find = WatchList.get_watch_list(session['email'])
        return render_template("watchlist.html", find=find)
    else:
        return redirect("/login")


@app.route("/change_preference:<code>")
def change_preference(code):
    currencylist, pos = Source.get_currency()
    if session['email']:
        WatchList.delete_watchList(session['email'], code)
        watchlist = WatchList.get_watch_list(session['email'])
        codes = WatchList.collect_codes(watchlist)
        return render_template("home.html", codes=codes, currencylist=currencylist)
    else:
        return redirect("/login")


@app.route("/history:<code>", methods=['POST', 'GET'])
def history(code):
    data(code)
    return render_template('history.html', code=code)


@app.route("/data/<code>", methods=['POST', 'GET'])
def data(code):
    data = getData(code)
    return data


@app.route("/search", methods=['POST', 'GET'])
def search():
    # currencylist, pos = Source.get_currency()
    if request.method == 'POST':
        name = request.form["search"]
        name = name[0:3]
        return history(name)


@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if session['email']:
        if request.method == 'POST':
            new = request.form['new_password']
            old = request.form['passwordIn']

            result = User.validation(session['email'], old)
            if result is not True:
                notification = "Oops! The password may be wrong! Please try agin!"
                return render_template("change_password.html", notification=notification)
            else:
                User.update_user_by_password(User.getPassword(session['email']), new)
                notification = "Your new password is reset"
                return render_template("change_password.html", notification=notification)
        else:
            return render_template("change_password.html")
    else:
        return redirect("/login")


@app.route("/profile")
def profile():
    # email = session["email"]
    # name = session["name"]
    return render_template('profile.html')


@app.route("/game", methods=['GET', 'POST'])
def game():
    print(session['name'])
    currencylist, pos = Source.get_currency()
    availableCurrency = Gamer.get_available_currency(session['name'])
    if request.method == 'POST':
        fromCurrency = request.form['from']
        toCurrency = request.form['to']
        fromAmount = request.form['fromAmount']
        result = convert(fromCurrency, toCurrency, fromAmount, currencylist, pos)
        result_temp = convert(fromCurrency, toCurrency, 1, currencylist, pos)
        Gamer.update_gameCurrency(session['name'], fromCurrency, toCurrency, fromAmount)
        availableCurrency = Gamer.get_available_currency(session['name'])
        message = Gamer.get_message(session['name'])
        amount = str(Gamer.update_amount(session['name']))

        # return render_template("game.html", currencylist=currencylist, from_position=pos[fromCurrency],
        #                        to_position=pos[toCurrency], from_Amount=fromAmount, to_Amount=result,
        #                        temp_to_Amount=result_temp, availableCurrency=availableCurrency,pos=pos)
        gamer_rank = rank()
        return render_template("game.html", currencylist=currencylist, availableCurrency=availableCurrency, pos=pos,
                               message=message, amount=amount, gamer_rank = gamer_rank)
    else:
        gamer_rank = rank()
        message = Gamer.get_message(session['name'])
        amount = str(Gamer.update_amount(session['name']))
        return render_template("game.html", currencylist=currencylist, pos=pos, availableCurrency=availableCurrency,
                               message=message, amount=amount, gamer_rank = gamer_rank)


if __name__ == "__main__":
    app.run(port=5000)
