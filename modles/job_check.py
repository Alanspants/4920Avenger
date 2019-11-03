import requests

from modles.money import Money
from modles.database import Database


def check_alert():
    moneydict, position = Money.search_data()
    all_user = []
    data = Database.find_all(collection="users")
    for user in data:
        all_user.append(user["email"])
    for user in all_user:
        message = []
        user_all_alert = Database.find(collection="all_alert", query={"email": user})
        for user_alert in user_all_alert:
            if user_alert["rate_exchange"] == "cash":
                if moneydict[position[user_alert["currency"]]].cash_in != "-":
                    if float(user_alert["price"][0]) >= float(moneydict[position[user_alert["currency"]]].cash_in):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    elif moneydict[position[user_alert["currency"]]].cash_out != "-":
                        if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].cash_out):
                            if user_alert["currency"] not in message:
                                message.append(user_alert["currency"])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif moneydict[position[user_alert["currency"]]].cash_out != "-":
                    if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].cash_out):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            if user_alert["rate_exchange"] == "sign":
                if moneydict[position[user_alert["currency"]]].sign_in != "-":
                    if float(user_alert["price"][0]) >= float(moneydict[position[user_alert["currency"]]].sign_in):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    elif moneydict[position[user_alert["currency"]]].sign_out != "-":
                        if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].sign_out):
                            if user_alert["currency"] not in message:
                                message.append(user_alert["currency"])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif moneydict[position[user_alert["currency"]]].sign_out != "-":
                    if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].sign_out):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        print(user, ": ", message)
        requests.post(
            "https://api.mailgun.net/v3/sandbox827c2b1aa6494b76ba23f7de5ac7fa3b.mailgun.org/messages",
            auth=("api", "51a35f8e68a577cad7e6bbb93df3cb86-816b23ef-81e736b3"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox827c2b1aa6494b76ba23f7de5ac7fa3b.mailgun.org>",
                  "to": "Avenger <haozhechen6@gmail.com>",
                  #user
                  "subject": "Hello Avenger",
                  "text": "Current requirement satisifiy currency: {}".format(str(message).strip("[]"))
                  }
        )


# Database.initialize()
# check_alert()
