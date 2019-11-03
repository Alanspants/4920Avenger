import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox827c2b1aa6494b76ba23f7de5ac7fa3b.mailgun.org/messages",
		auth=("api", "51a35f8e68a577cad7e6bbb93df3cb86-816b23ef-81e736b3"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox827c2b1aa6494b76ba23f7de5ac7fa3b.mailgun.org>",
			"to": "Avenger <haozhechen6@gmail.com>",
			"subject": "Hello Avenger",
			"text": "Congratulations Avenger, you just sent an email with Mailgun!  You are truly awesome!"})

send_simple_message()