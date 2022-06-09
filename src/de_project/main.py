from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

from send_msg import send

sched = BlockingScheduler()


@sched.scheduled_job(
    "cron", day_of_week="wed", hour=21, minute=33, timezone="America/Bahia"
)
def scheduled_job():
    send()
    print("This job is run monday at 20:00")


sched.start()
