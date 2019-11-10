from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


def round():
    print("dolly")

if __name__ == '__main__':
    while True:
        work = BackgroundScheduler()
        #work.add_job(round, "interval",seconds=1)
        # work.add_job(round, "interval", start_date=datetime(2019,11,8,17,17,0), seconds=1)
        # work.add_job(round, "cron", month="3-4, 6-7", day_of_week="1-2", hour="10", minute="8", second="10, 15")
        work.add_job(round, "date", run_date=datetime(2019, 11, 8, 17, 21, 20))
        work.start()
