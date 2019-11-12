from backends.currency import Source
from backends.database import Database
import requests

def get_reminder():
    sources = Database.get_all(document="users")
    emails = []
    for user in sources:
        emails.append(user["email"])
    print(emails)
    currencylist, poslist = Source.get_currency()
    for email in emails:
        reminders = Database.find(document="all_alert", new_record={"email": email})
        currencies = []
        for reminder in reminders:
            #print(reminder)
            #print(reminder["price"])
            # print(pos)
            # print(pos['A'])
            #print(float(currencylist[pos[reminder["currency"]]].buy_rate))
            if currencylist[poslist[reminder["currency"]]].sell_rate != None:
                if float(currencylist[poslist[reminder["currency"]]].sell_rate) >= float(reminder["price"][0]):
                    if reminder["currency"] not in currencies:
                        currencies.append(reminder["currency"])
                    else:
                        pass
                else:
                    pass
            elif currencylist[poslist[reminder["currency"]]].buy_rate != None:
                if float(currencylist[poslist[reminder["currency"]]].buy_rate) <= float(reminder["price"][1]):
                    if reminder["currency"] not in currencies:
                        currencies.append(reminder["currency"])
                    else:
                        pass
                else:
                    pass
            else:
                pass

            #             currencies.append(user_alert["currency"])
            #         else:
            #             pass
            #             else:
            #                 pass
            #         else:
            #             pass
            #     else:
            #         pass
            #         else:
            #             pass
            #     else:
            #         pass
            # else:
            #     pass
        print(currencies)
        print(str(currencies).strip("[]"))
        print(email, ":", currencies)
        if len(currencies):
            requests.post(
                "https://api.mailgun.net/v3/sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org/messages",
                auth=("api", "1b0576f57d49e0faa17b43365cd39117-f696beb4-a9a6bd6b"),
                data={"from": "Mailgun Sandbox <postmaster@sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org>",
                      "to": "Dolly Lu <dollylululu@gmail.com>",
                      # "to": user,
                      "subject": "Currency Reminder",
                      "text": "Dear user, your interested rate for {} has been reached!".format(str(currencies).strip("[]"))})

# Database.initialize()
# check_alert()