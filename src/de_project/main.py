from apscheduler.schedulers.blocking import BlockingScheduler

from send_msg import send

sched = BlockingScheduler()


@sched.scheduled_job("cron", day_of_week="wed", hour=21, minute=2)
def scheduled_job():
    send()
    print("This job is run monday at 20:00")


sched.start()
