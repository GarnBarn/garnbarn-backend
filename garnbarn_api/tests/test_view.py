from django.test import TestCase
from garnbarn_api.models import Tag, Assignment
from django.urls import reverse
from django.http import request


class ViewTests(TestCase):
    def setUp(self):
        """Create assignment's object"""
        self.assignment = Assignment.objects.create(id=1,
                                                    assignment_name="test_name",
                                                    due_date=1635579090,
                                                    detail="This is a test"
                                                    )

    def test_create_assignment(self):
        pass
