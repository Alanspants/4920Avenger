from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("HELLO")

Scheduler = BackgroundScheduler()
Scheduler.add_job(job,"interval", seconds=3, start_date=datetime(2019 ,11,3,17,13,00))
Scheduler.start()

while True:
    pass
