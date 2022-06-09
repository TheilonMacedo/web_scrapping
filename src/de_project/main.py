from apscheduler.schedulers.blocking import BlockingScheduler

from send_msg import send

sched = BlockingScheduler()


@sched.scheduled_job("interval", seconds=4)
def timed_job():
    print("This job is run every three minutes.")


# @sched.scheduled_job("cron", day_of_week="wed", hour=20, minute=43)
# def scheduled_job():
#     send()
#     print("This job is run monday at 20:00")


sched.start()
