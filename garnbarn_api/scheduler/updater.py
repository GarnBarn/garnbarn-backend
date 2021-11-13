from apscheduler.schedulers.background import BackgroundScheduler
from garnbarn_api.views import AssignmentViewset


def start():
    scheduler = BackgroundScheduler()
    assignment = AssignmentViewset()

    reminder_time = "reminder_time"  # change this to nerarest reminder_time
    # call notifiation method
    scheduler.add_job()
    reminder_time = "next reminder_time"  # change this to next reminder_time


def notify():
    pass
