
import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org/messages",
		auth=("api", "1b0576f57d49e0faa17b43365cd39117-f696beb4-a9a6bd6b"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox1a5c1ed6074a4b759c651994f7509e55.mailgun.org>",
			# "to": "Dolly Lu <dollylululu@gmail.com>",
            "to": "Dolly Lu <dollylululu@163.com>",

              "subject": "Hello Dolly Lu19",
			"text": "Congratulations Dolly Lu, you just sent an email with Mailgun!  You are truly awesome!"})
send_simple_message()