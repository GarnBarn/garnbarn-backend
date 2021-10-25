from django.http import response
from django.test import TestCase
from garnbarn_api.models import Tag, Assignment
from django.urls import reverse
from datetime import datetime, timedelta, timezone
import json
from django.core.exceptions import ObjectDoesNotExist


def convert_to_json(data):
    """Convert data into json format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data


class ViewTests(TestCase):
    def setUp(self):
        self.current_time = datetime.now()
        self.end_date = self.current_time + timedelta(days=1)
        # datetime.timestamp() will give float
        # so we have to change its format to int.
        self.current_timestamp = int(self.current_time.timestamp())
        self.end_date_timestamp = int(self.end_date.timestamp())

        self.tag = Tag(tag_name="test_tag")
        self.tag.save()

        assignment = Assignment(
            assignment_name="assignment 1",
            tag=self.tag,
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
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "tag_name": "test_tag",
                "color": None
            },
            "name": "assignment 1",
            "dueDate": self.end_date_timestamp,
            "timestamp": self.current_timestamp,
            "detail": "test"
        })
        self.assertJSONEqual(res, converted_data)

    def test_post_without_name(self):
        """Create assignment object without a name"""
        data = {
            "detail": "no-name"
        }
        response = self.client.post("/api/v1/assignment/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "name": ["This field is required."]
        })
        self.assertJSONEqual(res, converted_data)

    def test_post_with_invalid_tag_id(self):
        """Create assignment object with non-exist tag's id"""
        data = {
            "name": "asssignment",
            "tag": 0
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

    def test_post_with_invalid_due_date(self):
        """Create assignment object with dueDate < now"""
        data = {
            "name": "assignment",
            "dueDate": self.current_time - timedelta(days=1),
            "detail": "dueDate is invalid"
        }
        response = self.client.post("/api/v1/assignment/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "message": "Invalid due date"
        })
        self.assertJSONEqual(res, converted_data)
        self.assertEqual(400, response.status_code)
        all_assignment_objects = Assignment.objects.all()
        self.assertEqual(len(all_assignment_objects), 1)

    def test_post_with_valid_data(self):
        """Create assignment object"""
        data = {
            "tag": 1,
            "name": "assignment 2",
            "dueDate": self.end_date,
            "timestamp": self.current_time,
            "detail": "assignment 2's detail"
        }
        response = self.client.post("/api/v1/assignment/", data)
        self.assertEqual(200, response.status_code)
        new_assignment = Assignment.objects.get(assignment_name="assignment 2")
        # TODO: Uncomment these line after edit the data in this testcase.
        # self.assertEqual(new_assignment.due_date.now(), data["dueDate"].now())
        # self.assertEqual(new_assignment.timestamp, data["timestamp"])
        self.assertEqual(new_assignment.detail, data["detail"])

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
        res = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "tag_name": "test_tag",
                "color": None
            },
            "name": "renamed",
            "dueDate": self.end_date_timestamp,
            "timestamp": self.current_timestamp,
            "detail": "test"
        })
        self.assertJSONEqual(res, converted_data)

    def test_patch_with_invalid_tag_name(self):
        """Update patch with not-exist tag name"""
        data = json.dumps({
            "tag_name": "not exist"
        })
        with self.assertRaises(Tag.DoesNotExist):
            response = self.client.patch("/api/v1/assignment/1/", data,
                                         content_type="application/json"
                                         )
            self.assertEqual(400, response.status_code)

    def test_delete(self):
        """Delete assignment object"""
        response = self.client.delete("/api/v1/assignment/1/")
        converted_data = convert_to_json(response.content)
        res = json.dumps({})
        self.assertJSONEqual(res, converted_data)
        self.assertEqual(200, response.status_code)
        # The Assignment in database should be empty now. (Since we remove the assignment 1)
        all_assignment_objects = Assignment.objects.all()
        self.assertEqual(len(all_assignment_objects), 0)

        # Check if the assignment object has been deleted
        # Status code sould be 404 (Not Found)
        response_after_deleted = self.client.get("/api/v1/assignment/1/")
        self.assertEqual(404, response_after_deleted.status_code)
