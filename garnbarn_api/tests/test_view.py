from django.http import response
from django.test import TestCase
from garnbarn_api.models import Tag, Assignment
from django.urls import reverse
from datetime import datetime, timedelta, timezone
import json


def convert_to_json(data):
    """Convert data into json format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data


class ViewTests(TestCase):
    def setUp(self):
        self.current_time = datetime.now()
        self.end_date = self.current_time + timedelta(days=1)

        tag = Tag(tag_name="test_tag")
        tag.save()

        assignment = Assignment(
            assignment_name="assignment 1",
            tag=tag,
            timestamp=self.current_time,
            due_date=self.end_date,
            detail="test"
        )
        assignment.save()

    def test_assignment_not_found(self):
        """Raise 404 status code when assignment's object does not exist"""
        response = self.client.get("/api/v1/assignment/0/")
        self.assertEqual(404, response.status_code)

    def test_get(self):
        """Return detail of the assignment"""
        response = self.client.get("/api/v1/assignment/1/")
        data = convert_to_json(response.content)
        res = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "tag_name": "test_tag"
            },
            "name": "assignment 1",
            "dueDate": int(self.end_date.timestamp()),
            "timestamp": int(self.current_time.timestamp()),
            "detail": "test"
        })
        self.assertJSONEqual(res, data)

    def test_post_with_invalid_data(self):
        data = {
            "detail": "no-name"
        }
        response = self.client.post("/api/v1/assignment/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "name": ["This field is required"]
        })
