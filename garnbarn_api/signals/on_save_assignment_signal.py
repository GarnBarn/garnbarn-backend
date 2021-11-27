from django.db.models.signals import post_save
from django.dispatch import receiver

from garnbarn_api.models import Assignment, Tag
from garnbarn_api.services.scheduler import scheduler
from garnbarn_api.signals.publish_notification_signal import publish_notification_signal
from apscheduler.triggers.date import DateTrigger

from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Assignment)
def on_save_assignment(sender, instance: Assignment, created, **kwargs):
    """Add job schedule when Assigment.save() is called."""
    # Stop function if there is no due_date, because schedule time
    # is calculated by due_date - reminder_time.
    if not instance.due_date:
        return
    instance.refresh_from_db()
    schedule_time = adjust_schedule_date(instance)
    clear_jobs(instance)
    add_jobs(instance, schedule_time, publish_notification_signal)


@receiver(post_save, sender=Tag)
def on_save_tag(sender, instance: Tag, created, **kwargs):
    assignments = Assignment.objects.filter(tag=instance)
    if not assignments or not instance.reminder_time:
        return
    instance.refresh_from_db()
    for assignment in assignments:
        if not assignment.reminder_time:
            schedule = adjust_schedule_date(assignment)
            clear_jobs(assignment)
            add_jobs(assignment, schedule, publish_notification_signal)


def adjust_schedule_date(instance):
    """If assignment object did not provide any reminder time,
    tag's reminder time will be used.

    Args:
        instance (Assignment): Assignment object.
        schedule_date (list): List of reminder times.
    """
    # Default value in schedule date is 0 because we have to
    # add a job for on-time reminder.
    schedule_time = [0]
    if instance.reminder_time:
        schedule_time += instance.reminder_time
    elif not instance.reminder_time and instance.tag:
        if instance.tag.reminder_time:
            schedule_time += instance.tag.reminder_time
    return schedule_time


def add_jobs(instance, schedule_time, func):
    """Add job's scheduler if schedule date is not
    behind present time.

    Args:
        instance (Assignment): Assignment object.
        schedule_date (list): List of reminder times.
        func (Callback function): A function which will be done at scheduled time.
    """
    for index, item in enumerate(schedule_time):
        schedule = instance.due_date.timestamp() - item
        schedule = datetime.fromtimestamp(schedule)
        if schedule < datetime.now():
            logger.debug(
                f"The schedule date({schedule}) is behind current time. Job skipped")
            continue
        job = scheduler.add_job(func, trigger=DateTrigger(run_date=schedule), id=f"Notification - {instance.pk}_{index}",
                                max_instances=1, replace_existing=True, args=[instance])
        logger.info(
            f"Schedule for assignment with id:{instance.pk} has been set to trigger on ({job.next_run_time})")


def clear_jobs(instance):
    """Clear all scheduled jobs of current assignment.

    Args:
        instance (Assignment): Assignment object.
    """
    for i in range(4):
        job_id = f"Notification - {instance.pk}_{i}"
        if scheduler.get_job(job_id) is None:
            break
        scheduler.remove_job(job_id)
