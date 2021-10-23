from django.test import TestCase
from garnbarn_api.models import Assignment


class AssignmentModelTests(TestCase):
    def setUp(self):
        self.assignment = Assignment.objects.create(
            assignment_name="test_name",
            due_date=1635336554,
            detail="test_detail"
        )