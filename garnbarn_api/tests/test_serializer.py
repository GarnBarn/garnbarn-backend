from datetime import date
from django.test import TestCase
from garnbarn_api.serializer import AssignmentSerializer
from garnbarn_api.models import Assignment


class SerializerTests(TestCase):
    def setUp(self):
        self.assignment_attributes = {
            'id': 1,
            'tag': None,
            'assignment_name': 'test_with_serializer',
            'due_date': '2021-10-27T19:09:03+07:00',
            'timestamp': '2021-10-27T19:09:03+07:00',
            'detail': 'test_with_serializer'
        }
        self.serializer_data = {
            'id': 1,
            'tag': None,
            'assignment_name': 'test_with_serializer',
            'due_date': '2021-10-27T19:09:03+07:00',
            'timestamp': '2021-10-27T19:09:03+07:00',
            'detail': 'test_with_serializer'
        }

        self.assignment_object = Assignment.objects.create(
            assignment_name='test_with_serializer',
            due_date='2021-10-27T19:09:03+07:00',
            detail='test_with_serializer'
            )
        self.serializer = AssignmentSerializer(instance=self.assignment_object)

    def test_serializer_contain_expected_field(self):
        data = self.serializer.data
        self.assertCountEqual(set(data.keys()), set({
            'id',
            'tag',
            'assignment_name',
            'due_date',
            'timestamp',
            'detail'
        }))

    def test_field_content_expect_timestamp(self):
        data = self.serializer.data
        self.assertEqual(data['tag'], self.assignment_attributes['tag'])
        self.assertEqual(data['id'], self.assignment_attributes['id'])
        self.assertEqual(data['assignment_name'], self.assignment_attributes['assignment_name'])
        self.assertEqual(data['due_date'], self.assignment_attributes['due_date'])
        self.assertEqual(data['detail'], self.assignment_attributes['detail'])