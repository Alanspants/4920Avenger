from backends.money import Money
from backends.database import Database
import requests

def check_alert():
    moneydict, position = Money.search_data()


    all_user = []
    data = Database.find_all(collection="users")
    for user in data:
        all_user.append(user["email"])
    print(all_user)
    for user in all_user:
        message = []
        user_all_alert = Database.find(collection="all_alert", query={"email":user})
        for user_alert in user_all_alert:
            #print(user_alert)
            #print(user_alert["price"])
            # print(position)

            # print(position['A'])
            #print(float(moneydict[position[user_alert["currency"]]].buy_rate))
            if moneydict[position[user_alert["currency"]]].sell_rate != None:
                if float(user_alert["price"][0]) >= float(moneydict[position[user_alert["currency"]]].sell_rate):
                    if user_alert["currency"] not in message:
                        message.append(user_alert["currency"])
                    else:
                        pass
                elif moneydict[position[user_alert["currency"]]].buy_rate != "-":
                    if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].buy_rate):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            elif moneydict[position[user_alert["currency"]]].buy_rate != None:
                if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].buy_rate):
                    if user_alert["currency"] not in message:
                        message.append(user_alert["currency"])
                    else:
                        pass
                else:
                    pass
            else:
                pass

            # if moneydict[position[user_alert["currency"]]].buy_rate:
            #     if float(user_alert["price"][0]) >= float(moneydict[position[user_alert["currency"]]].buy_rate):
            #         if user_alert["currency"] not in message:
            #             message.append(user_alert["currency"])
            #         else:
            #             pass
            #     elif moneydict[position[user_alert["currency"]]].sell_rate != "-":
            #         if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].sell_rate):
            #             if user_alert["currency"] not in message:
            #                 message.append(user_alert["currency"])
            #             else:
            #                 pass
            #         else:
            #             pass
            #     else:
            #         pass
            # elif moneydict[position[user_alert["currency"]]].sell_rate:
            #     if float(user_alert["price"][0]) <= float(moneydict[position[user_alert["currency"]]].sell_rate):
            #         if user_alert["currency"] not in message:
            #             message.append(user_alert["currency"])
            #         else:
            #             pass
            #     else:
            #         pass
            # else:
            #     pass
    print(message)
    print(str(message).strip("[]"))
    print(user, ":", message)
    requests.post(
        "https://api.mailgun.net/v3/sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org/messages",
        auth=("api", "1b0576f57d49e0faa17b43365cd39117-f696beb4-a9a6bd6b"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org>",
              "to": "Dolly Lu <dollylululu@gmail.com>",
              # "to": user,
              "subject": "Currency Reminder",
              "text": "Dear user, your interested rate for {} has been reached!".format(str(message).strip("[]"))})

# Database.initialize()
# check_alert()