from datetime import date, datetime
from django.test import TestCase
from garnbarn_api.serializer import AssignmentSerializer
from garnbarn_api.models import Assignment


class SerializerTests(TestCase):
    """Create setup for each test case."""

    def setUp(self):
        due_date1 = datetime.fromtimestamp(1635361743)
        due_date2 = datetime.fromtimestamp(1603825743)
        self.assignment_attributes = {
            'id': 1,
            'tag': None,
            'assignment_name': 'test_with_serializer',
            'due_date': due_date1.timestamp(),
            'timestamp': '2021-10-27T19:09:03+07:00',
            'detail': 'test_with_serializer'
        }

        self.assignment_object = Assignment.objects.create(
            assignment_name='test_with_serializer',
            due_date=due_date1,
            detail='test_with_serializer'
        )

        self.assignment_object2 = Assignment.objects.create(
            assignment_name='test_with_serializer',
            due_date=due_date2,
            detail='test_with_serializer'
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
            'assignment_name',
            'due_date',
            'timestamp',
            'detail'
        }))

    def test_field_content_except_timestamp(self):
        """Test that serializer have all the content in side the header."""
        data = self.serializer.data
        self.assertEqual(data['tag'], self.assignment_attributes['tag'])
        self.assertEqual(data['id'], self.assignment_attributes['id'])
        self.assertEqual(data['assignment_name'],
                         self.assignment_attributes['assignment_name'])
        self.assertEqual(data['due_date'],
                         self.assignment_attributes['due_date'])
        self.assertEqual(data['detail'], self.assignment_attributes['detail'])

    def test_is_published_return_True(self):
        """Test is_pulbished.

        Return:
            If the serializer is published the is_published will return True.
        """
        data = self.serializer.data
        self.assertEqual(True, data.serializer.is_published())

    def test_is_published_return_False(self):
        """Test is_pulbished.

        Return:
            If the serializer is not published the is_published will return False.
        """
        data = self.serializer2.data
        self.assertEqual(False, data.serializer.is_published())
