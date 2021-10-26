from django.test import TestCase
from garnbarn_api.models import Tag, Assignment
from datetime import datetime, timedelta
import json
import math


def convert_to_json(data):
    """Convert data into json format"""
    data = json.loads(data)
    # data = json.dumps(data)
    return data


class ViewTests(TestCase):
    def setUp(self):
        self.current_time = datetime.now()
        self.end_date = self.current_time + timedelta(days=1)
        # datetime.timestamp() will give float
        # so we have to change its format to int.
        self.current_timestamp = round(
            self.current_time.timestamp() * 1000)
        self.end_date_timestamp = round(self.end_date.timestamp() * 1000)

        self.tag = Tag(name="test_tag")
        self.tag.save()

        assignment = Assignment(
            assignment_name="assignment 1",
            tag=self.tag,
            timestamp=self.current_time,
            due_date=self.end_date,
            description="test"
        )
        assignment.save()

    def test_assignment_not_found(self):
        """Raise 404 status code when assignment's object does not exist"""

        response = self.client.get("/api/v1/assignment/0/")
        self.assertEqual(404, response.status_code)

    def test_get(self):
        """Return detail of the assignment"""

        response = self.client.get("/api/v1/assignment/1/")
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "name": "test_tag",
                "color": None
            },
            "name": "assignment 1",
            "dueDate": self.end_date_timestamp,
            "timestamp": self.current_timestamp,
            "description": "test"
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)

    def test_post_without_name(self):
        """Create assignment object without a name"""

        data = {
            "description": "no-name"
        }
        response = self.client.post("/api/v1/assignment/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "message": {
                "name": ["This field is required."]
            }
        })
        self.assertJSONEqual(res, converted_data)
        self.assertEqual(400, response.status_code)

    def test_post_with_invalid_tag_id(self):
        """Create assignment object with non-exist tag's id"""
        data = {
            "name": "asssignment",
            "tagId": 0
        }
        response = self.client.post("/api/v1/assignment/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "message": "Tag's ID not found"
        })
        self.assertJSONEqual(res, converted_data)
        self.assertEqual(400, response.status_code)
        all_assignment_objects = Assignment.objects.all()
        self.assertEqual(len(all_assignment_objects), 1)

    def test_post_with_valid_data(self):
        """Create assignment object"""
        data = {
            "tagId": 1,
            "name": "assignment 2",
            "timestamp": self.current_time,
            "dueDate": self.end_date_timestamp,
            "description": "assignment 2's detail"
        }
        response = self.client.post(
            "/api/v1/assignment/", data, content_type="application/json")
        self.assertEqual(200, response.status_code)

        new_assignment = Assignment.objects.get(assignment_name="assignment 2")
        self.assertEqual(new_assignment.due_date.timestamp(), data["dueDate"])
        self.assertEqual(int(new_assignment.timestamp.timestamp()),
                         int(data["timestamp"].timestamp()))
        self.assertEqual(new_assignment.description, data["description"])

    def test_patch(self):
        """Update assignment object"""
        data = json.dumps({
            "name": "renamed"
        })
        # rename assignment from "assignment 1" to "renamed"
        response = self.client.patch("/api/v1/assignment/1/", data,
                                     content_type="application/json"
                                     )
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "name": "test_tag",
                "color": None
            },
            "name": "renamed",
            "dueDate": self.end_date_timestamp,
            "timestamp": self.current_timestamp,
            "description": "test"
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)
        all_assignment_in_database = Assignment.objects.all()
        self.assertEqual(len(all_assignment_in_database), 1)
        focused_assignment = all_assignment_in_database[0]
        self.assertEqual(focused_assignment.name, "renamed")

    def test_delete(self):
        """Delete assignment object"""
        response = self.client.delete("/api/v1/assignment/1/")
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({})
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)
        # The Assignment in database should be empty now. (Since we remove the assignment 1)
        all_assignment_objects = Assignment.objects.all()
        self.assertEqual(len(all_assignment_objects), 0)
        # Check if the assignment object has been deleted
        # Status code should be 404 (Not Found)
        response_after_deleted = self.client.get("/api/v1/assignment/1/")
        self.assertEqual(404, response_after_deleted.status_code)
