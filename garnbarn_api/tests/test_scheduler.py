from os import name
from apscheduler.job import Job
from django.test import TestCase
from django.utils import timezone
from garnbarn_api.models import Assignment, Tag
from garnbarn_api.services.scheduler import scheduler
from datetime import timedelta, datetime


def create_assignment(name, due_date=None, reminder=None, tag=None):
    """Create a assignment"""
    assignment = Assignment(assignment_name=name,
                            due_date=due_date,
                            reminder_time=reminder,
                            tag=tag
                            )
    return assignment


class TestScheduler(TestCase):
    def setUp(self):
        """Create tag and assignments"""
        self.due_date = timezone.now() + timedelta(days=10)
        hour = 3600  # seconds
        day = 86400  # seconds
        week = 604800  # seconds

        self.week_before_due_date = self.datetime_before_due_date("week")
        self.day_before_due_date = self.datetime_before_due_date("day")
        self.hour_before_due_date = self.datetime_before_due_date("hour")

        self.tag = Tag(name="Tag", reminder_time=[day])
        self.tag.save()

        self.assignment_1 = create_assignment(name="Assignment 1",
                                              due_date=self.due_date,
                                              reminder=[hour, week]
                                              )
        self.assignment_2 = create_assignment(name="Assignment 2",
                                              reminder=[hour, week]
                                              )
        self.assignment_3 = create_assignment(name="Assignment 3",
                                              due_date=self.due_date,
                                              tag=self.tag
                                              )

    def datetime_before_due_date(self, duration):
        """Get datetime before assignment's due date"""
        if duration == "week":
            return self.due_date - timedelta(days=7)
        elif duration == "day":
            return self.due_date - timedelta(days=1)
        elif duration == "hour":
            return self.due_date - timedelta(hours=1)

    def test_schedule_assignment_with_due_date_and_reminder_time(self):
        """Schedule assignment with specified due date and reminder time."""
        self.assignment_1.save()
        jobs = scheduler.get_jobs()
        self.assertEqual(3, len(jobs))
        self.assertEqual(self.week_before_due_date, jobs[0].next_run_time)
        self.assertEqual(self.hour_before_due_date, jobs[1].next_run_time)
        self.assertEqual(self.assignment_1.due_date, jobs[2].next_run_time)

    def test_schedule_assignment_with_no_due_date(self):
        """Schedule must not be added if due date is not specified."""
        self.assignment_2.save()
        self.assertEqual([], scheduler.get_jobs())

    def test_schedule_assignment_without_specifing_reminder_time(self):
        """If reminder time of assignment is not provided, will use reminder time from tag instead."""
        self.assignment_3.save()
        jobs = scheduler.get_jobs()
        self.assertEqual(2, len(jobs))
        self.assertEqual(self.day_before_due_date, jobs[0].next_run_time)
        self.assertEqual(self.assignment_3.due_date, jobs[1].next_run_time)

    def test_update_schedule(self):
        """Update assignment reminder time will update the job schedules."""
        self.assignment_1.save()
        jobs = scheduler.get_jobs()
        self.assertEqual(3, len(jobs))

        self.assignment_1.reminder_time = None
        self.assignment_1.save()
        jobs = scheduler.get_jobs()
        self.assertEqual(1, len(jobs))
        self.assertEqual(self.assignment_1.due_date, jobs[0].next_run_time)

    def test_schedule_time_is_behind_current_time(self):
        past_due_date = timezone.now() - timedelta(days=1)
        assignment = create_assignment(name="Old due date",
                                       due_date=past_due_date,
                                       tag=self.tag
                                       )
        assignment.save()
        jobs = scheduler.get_jobs()
        self.assertEqual(0, len(jobs))
