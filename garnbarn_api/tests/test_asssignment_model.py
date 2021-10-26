from django.test import TestCase
from garnbarn_api.models import Assignment
import datetime


class AssignmentModelTests(TestCase):
    def setUp(self):
        """Create a setup for each test case."""
        self.end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.end_data_timestamp = self.end_date.timestamp()

        self.assignment = Assignment.objects.create(
            assignment_name="test_name",
            due_date=self.end_date,
            description="test_detail"
        )

    def test_get_assignment_name(self):
        """Test assignment return string name of the assignment."""
        self.assertEqual('test_name', str(self.assignment))

    def test_assignment_due_date(self):
        """Test assigment due date."""
        self.assertIsInstance(self.assignment.due_date, datetime.datetime)

    def test_assignment_detail(self):
        """Test assignment deatail."""
        self.assertEqual('test_detail', self.assignment.description)

    def test_assigmnet_timestamp(self):
        """Test the type of assignment timestamp."""
        self.assertIsInstance(self.assignment.timestamp, datetime.datetime)
