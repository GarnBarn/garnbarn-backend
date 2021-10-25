from datetime import date, datetime, timedelta
from django.test import TestCase
from garnbarn_api.serializer import AssignmentSerializer
from garnbarn_api.models import Assignment


class SerializerTests(TestCase):
    """Create setup for each test case."""

    def setUp(self):
        self.end_date = datetime.now() + timedelta(days=1)
        self.end_date_timestamp = self.end_date.timestamp()

        self.assignment_attributes = {
            'id': 1,
            'tag': None,
            'name': 'test_with_serializer',
            'dueDate': self.end_date,
            'description': 'test_with_serializer'
        }

        self.assignment_object = Assignment.objects.create(
            assignment_name='test_with_serializer',
            due_date=self.end_date,
            description='test_with_serializer'
        )

        self.assignment_object2 = Assignment.objects.create(
            assignment_name='test_with_serializer',
            due_date=self.end_date,
            description='test_with_serializer'
        )

        self.serializer = AssignmentSerializer(instance=self.assignment_object)
        self.serializer2 = AssignmentSerializer(
            instance=self.assignment_object2)

    def test_serializer_contain_expected_field(self):
        """Test that serializer have all the header."""
        data = self.serializer.data
        self.assertCountEqual(set(data.keys()), set({
            'id',
            'tag',
            'name',
            'dueDate',
            'timestamp',
            'description'
        }))

    def test_field_content_except_timestamp(self):
        """Test that serializer have all the content in side the header."""
        data = self.serializer.data
        self.assertEqual(data['tag'], self.assignment_attributes['tag'])
        self.assertEqual(data['id'], self.assignment_attributes['id'])
        self.assertEqual(data['name'],
                         self.assignment_attributes['name'])
        self.assertEqual(data['dueDate'],
                         int(self.assignment_attributes['dueDate'].timestamp()))
        self.assertEqual(data['description'],
                         self.assignment_attributes['description'])
