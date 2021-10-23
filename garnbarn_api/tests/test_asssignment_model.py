from django.test import TestCase
from garnbarn_api.models import Assignment
import datetime


class AssignmentModelTests(TestCase):
    def setUp(self):
        """Create a setup for each test case."""
        due_date1 = datetime.datetime.fromtimestamp(1635361743)
        self.assignment = Assignment.objects.create(
            assignment_name="test_name",
            due_date=due_date1,
            detail="test_detail"
        )

    def test_get_assignment_name(self):
        """Test assignment return string name of the assignment."""
        self.assertEqual('test_name', str(self.assignment))

    def test_assignment_due_date(self):
        """Test assigment due date."""
        self.assertEqual(datetime.datetime.fromtimestamp(1635361743), self.assignment.due_date)

    def test_assignment_detail(self):
        """Test assignment deatail."""
        self.assertEqual('test_detail', self.assignment.detail)

    def test_assigmnet_timestamp(self):
        """Test the type of assignment timestamp."""
        self.assertIsInstance(self.assignment.timestamp, datetime.datetime)