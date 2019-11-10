from flask import Flask, request, render_template, session, redirect
from backends.database import Database as db
from backends.email_send import get_reminder
from apscheduler.schedulers.background import BackgroundScheduler
from backends.currency import Source
from backends.user import User
from backends.reminder import Reminder
import datetime
app = Flask(__name__)
# app.config['SECRET_KEY']=os.urandom(24)
app.secret_key = "123123123"

@app.before_first_request
def setup():
    session["email"] = session.get("email")
    session["name"] = session.get("name")
    db.setup()
    # work = BackgroundScheduler(check_alert, "cron", day_of_week="0-4", hour="16", miniute="30")
    work = BackgroundScheduler()
    # work.add_job(check_alert, "interval", seconds=10)
    work.add_job(get_reminder, "interval", seconds=1000)
    # work.add_job(check_alert, "cron", day_of_week="0-4", hour="18",minute="1")
    work.start()

@app.route("/")
def home():
    currencylist, pos = Source.get_currency()
    return render_template('home.html', currencylist=currencylist)

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
                return render_template("create_reminder.html", currencylist=currencylist, curr_info=curr_info, buy_info=buy_info, sell_info=sell_info, info=info)
            else:
                curr_info = "Currency Type: {}".format(input_currency)
                buy_info = "Buy Rate: ${}".format(buy_rate)
                sell_info = "Sell Rate: ${}".format(sell_rate)
                info = "Wow! Reminder added successfully!"
                return render_template("create_reminder.html", currencylist=currencylist, curr_info=curr_info, buy_info=buy_info, sell_info=sell_info, info=info)
        else:
            return render_template("create_reminder.html", currencylist=currencylist)
    else:
        return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['nameIn']
        email = request.form['emailIn']
        password = request.form['passwordIn']
        result = User.new_user(name, email, password)
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


if __name__== "__main__":
  app.run()