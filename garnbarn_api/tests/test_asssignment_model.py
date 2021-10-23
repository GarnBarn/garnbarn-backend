from django.test import TestCase
from garnbarn_api.models import Assignment


class AssignmentModelTests(TestCase):
    def setUp(self):
        self.assignment = Assignment(assignment_name='Test case')