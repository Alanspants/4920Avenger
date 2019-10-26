from flask import Flask, render_template
from modles.money import Money

app = Flask(__name__)

@app.route("/")
def home():
    moneydict, position = Money.search_data()
    return render_template("home.html", moneydict = moneydict)

if __name__ == "__main__":
    app.run(debug=True, port=4100)
