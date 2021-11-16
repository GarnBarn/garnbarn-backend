from django.db.models.signals import post_save
from django.dispatch import receiver

from garnbarn_api.models import Assignment
from garnbarn_api.services.scheduler import scheduler
from garnbarn_api.services.pubsub import pubsub
from apscheduler.triggers.date import DateTrigger

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Assignment)
def on_save_assignment(sender, instance, created, **kwargs):

    # Stop function if there is no due_date, because schedule time
    # is calculated by due_date - reminder_time.
    if not instance.due_date:
        return

    instance.refresh_from_db()
    # Default value in schedule date is 0 because we have to
    # add a job for on-time reminder.
    schedule_date = [0]
    if instance.reminder_time:
        schedule_date += instance.reminder_time
    elif not instance.reminder_time and instance.tag:
        if instance.tag.reminder_time:
            schedule_date += instance.tag.reminder_time

    for i in range(4):
        job_id = f"Notification - {instance.pk}_{i}"
        if scheduler.get_job(job_id) is None:
            break
        scheduler.remove_job(job_id)

    for index, item in enumerate(schedule_date):
        schedule = instance.due_date.timestamp() - item
        schedule = datetime.fromtimestamp(schedule)
        if schedule < datetime.now():
            logger.debug(
                f"The schedule date({schedule}) is behind current time. Job skipped")
            continue
        job = scheduler.add_job(pubsub, trigger=DateTrigger(run_date=schedule), id=f"Notification - {instance.pk}_{index}",
                                max_instances=1, replace_existing=True)
        logger.info(
            f"Schedule for assignment with id:{instance.pk} has been set to trigger on ({job.next_run_time})")
