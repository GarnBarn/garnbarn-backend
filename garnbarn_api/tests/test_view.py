
from django.http import response
from django.test import TestCase
from django.test.utils import tag
from rest_framework import serializers
from rest_framework.test import APITestCase

from freezegun import freeze_time

from garnbarn_api.models import Tag, Assignment, CustomUser
from datetime import datetime, timedelta
from rest_framework.test import force_authenticate, APITestCase
from django.contrib.auth.models import User

import json
import math
from unittest.mock import patch


def convert_to_json(data):
    """Convert data into json format"""
    data = json.loads(data)
    return data


class ViewTests(APITestCase):
    def setUp(self):
        self.current_time = datetime.now()
        self.end_date = self.current_time + timedelta(days=1)
        # datetime.timestamp() will give float
        # so we have to change its format to int.
        self.current_timestamp = math.floor(
            self.current_time.timestamp() * 1000)
        self.end_date_timestamp = math.floor(self.end_date.timestamp() * 1000)

        self.user = CustomUser.objects.create(uid="1234")
        self.client.force_authenticate(user=self.user)

        self.user = CustomUser(uid="user_id",
                               name="user_name",
                               )
        self.user.save()

        self.tag = Tag.objects.create(name="test_tag", color='#4285F4')
        self.assignment = Assignment(
            assignment_name="assignment 1",
            author=self.user,
            tag=self.tag,
            timestamp=self.current_time,
            due_date=self.end_date,
            description="test"
        )
        self.assignment.save()

        self.tag2 = Tag.objects.create(name="test_tag2", color='#4285F4', author=self.user)

    def test_assignment_not_existed_assignment(self):
        """Raise 404 status code when assignment's object does not exist"""
        response = self.client.get("/api/v1/assignment/0/")
        self.assertEqual(404, response.status_code)

    def test_tag_not_existed(self):
        """Raise 404 status code when tag's object does not exist."""
        response = self.client.get('/api/v1/tag/0/')
        self.assertEqual(404, response.status_code)

    def test_get(self):
        """Return detail of the assignment"""
        response = self.client.get("/api/v1/assignment/1/")
        converted_data = convert_to_json(response.content)
        timestamp_cache_from_request = converted_data["timestamp"]
        del converted_data["timestamp"]
        expected_result = json.dumps({
            "id": 1,
            "author": "user_id",
            "tag": {
                "id": 1,
                "name": "test_tag",
                "author": None,
                "color": '#4285F4',
                "reminderTime": None,
            },
            "name": "assignment 1",
            "dueDate": self.end_date_timestamp,
            "description": "test",
            "reminderTime": None
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertAlmostEqual(timestamp_cache_from_request,
                               self.current_timestamp, delta=2)
        self.assertEqual(200, response.status_code)

    def test_post_without_name(self):
        """Create assignment object without a name"""

        data = {
            "author": self.user,
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

    def test_post_with_invalid_reminder_time(self):
        """Reminder time contain string"""
        data = {
            "name": "Bob",
            "reminderTime": [1, 2, "hello"]
        }
        response = self.client.post("/api/v1/assignment/", data)
        self.assertEqual(400, response.status_code)

    def test_post_with_empty_list_reminder_time(self):
        """Create assignment with reminder"""
        data = {
            "name": "Bob",
            "reminderTime": []
        }
        response = self.client.post("/api/v1/assignment/", data)
        response_in_json = json.loads(response.content)
        self.assertIsNone(response_in_json["reminderTime"])

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
            "dueDate": self.end_date_timestamp,
            "description": "assignment 2's detail",
            "reminderTime": [3600, 1800]
        }
        response = self.client.post(
            "/api/v1/assignment/", json.dumps(data), content_type="application/json")
        self.assertEqual(200, response.status_code)
        new_assignment = Assignment.objects.get(assignment_name="assignment 2")
        # For dueDate, Python used second based timestamp. So converting between milisec timestamp
        # Will lose 3 unit presistion. So delta=1000
        self.assertAlmostEqual(math.floor(new_assignment.due_date.timestamp()
                                          * 1000), data["dueDate"], delta=1000)
        # The creation time may not equal the current timestamp, The acceptable creation time is 2s or 2000 ms
        self.assertAlmostEqual(math.floor(new_assignment.timestamp.timestamp() * 1000),
                               self.current_timestamp, delta=2000)
        self.assertEqual(new_assignment.description, data["description"])
        data["reminderTime"].sort()
        self.assertEqual(data["reminderTime"],
                         new_assignment.reminder_time)

    def test_patch(self):
        """Update assignment object"""
        data = json.dumps({
            "name": "renamed",
            "dueDate": self.end_date_timestamp + 10000,
            "reminderTime": [100, 10, 25]
        })
        # rename assignment from "assignment 1" to "renamed"
        response = self.client.patch("/api/v1/assignment/1/", data,
                                     content_type="application/json"
                                     )
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({
            "id": 1,
            "author": "user_id",
            "tag": {
                "id": 1,
                "name": "test_tag",
                "author": None,
                "color": '#4285F4',
                "reminderTime": None
            },
            "name": "renamed",
            "description": "test",
            "reminderTime": [10, 25, 100]
        })
        timestamp_cache_from_request = converted_data["timestamp"]
        due_date_cache_from_request = converted_data["dueDate"]
        del converted_data["timestamp"]
        del converted_data["dueDate"]
        self.assertJSONEqual(expected_result, converted_data)
        self.assertAlmostEqual(timestamp_cache_from_request,
                               self.current_timestamp, delta=2)
        self.assertAlmostEqual(self.end_date_timestamp +
                               10000, due_date_cache_from_request, delta=1000)
        self.assertEqual(200, response.status_code)
        all_assignment_in_database = Assignment.objects.all()
        self.assertEqual(len(all_assignment_in_database), 1)
        focused_assignment = all_assignment_in_database[0]
        self.assertEqual(focused_assignment.assignment_name, "renamed")

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
        # Check if the assignment has been deleted from database, (The number of datas should be 0)
        assignments_in_database = Assignment.objects.all()
        self.assertEqual(len(assignments_in_database), 0)

    def test_get_tag(self):
        """Return detail of the tag."""
        response = self.client.get("/api/v1/tag/2/")
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({
            "id": 2,
            "name": "test_tag2",
            "author": 'user_id',
            "color": "#4285F4",
            "reminderTime": None,
            "subscriber": None
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)

    def test_post_tag_without_name(self):
        """Create tag object without a name."""

        data = {
            'author': self.user,
            'color': '#4285F4',
        }
        response = self.client.post("/api/v1/tag/", data)
        converted_data = convert_to_json(response.content)
        res = json.dumps({
            "message": {
                "name": ["This field is required."]
            }
        })
        self.assertJSONEqual(res, converted_data)
        self.assertEqual(400, response.status_code)

    def test_post_with_invalid_tag_reminder_time(self):
        """Reminder time contain string"""
        data = {
            "name": "test_tag",
            "reminderTime": [1, 2, "hello"]
        }
        response = self.client.post("/api/v1/tag/", data)
        self.assertEqual(400, response.status_code)

    def test_post_valid_tag(self):
        """Create tag object with no error."""
        data = {
            'name': "test_tag",
            'author': self.user,
            'color': '#4285F4',
            "reminderTime": [3600, 1800],
            'subscriber': self.user
        }
        response = self.client.post("/api/v1/tag/", data)
        self.assertEqual(200, response.status_code)

    def test_tag_patch(self):
        """Update tag object."""
        data = json.dumps({
            'name': "renamed",
            'color': '#4285F9',
        })
        response = self.client.patch("/api/v1/tag/1/", data,
                                    content_type="application/json"
                                    )
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({
            'id': 1,
            'name': "renamed",
            'author': None,
            'color': '#4285F9',
            'reminderTime': None
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)
        all_tag_in_database = Tag.objects.all()
        self.assertEqual(len(all_tag_in_database), 2)
        focused_tag = all_tag_in_database[0]
        self.assertEqual(focused_tag.name, 'renamed')

    def test_tag_delete(self):
        """Delete tag object."""
        response = self.client.delete("/api/v1/tag/1/")
        converted_data = convert_to_json(response.content)
        expected_result = json.dumps({})
        self.assertJSONEqual(expected_result, converted_data)
        self.assertEqual(200, response.status_code)
        all_tag_object = Tag.objects.all()
        self.assertEqual(len(all_tag_object), 1)
        response_after_deleted = self.client.get("/api/v1/tag/1/")
        self.assertEqual(404, response_after_deleted.status_code)
        tag_in_database = Tag.objects.all()
        self.assertEqual(len(tag_in_database), 1)


@freeze_time("2012-12-12T12:00:00+07:00")
class FromPresentTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = CustomUser.objects.create(uid="1234")
        self.client.force_authenticate(user=self.user)

        # Create assignment with specified due date
        yesterday = datetime.now() - timedelta(days=1)
        today_but_in_the_past = datetime.now() - timedelta(hours=3)
        today = datetime.now()
        tomorrow = datetime.now() + timedelta(days=1)
        self.assignment1 = self.create_assignment("assignment 1", tomorrow)
        self.assignment2 = self.create_assignment("assignment 2", yesterday)
        self.assignment3 = self.create_assignment(
            "assignment 3", today)
        self.assignment4 = self.create_assignment(
            "assignment 4", today_but_in_the_past)

    def create_assignment(self, name, due_date):
        return Assignment.objects.create(assignment_name=name, due_date=due_date)

    def test_not_frompresent(self):
        """Normal GET method"""
        response = self.client.get("/api/v1/assignment/")
        self.assertEqual(json.loads(response.content)["count"], 4)

    def test_frompresent_is_true(self):
        """Adding fromPresent=true"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        # fromPresent=true will exclude assignment with due date < today
        self.assertEqual(json.loads(response.content)["count"], 3)

    def test_frompresent_order(self):
        """The assignment should be ordered by its due date"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        response_in_json = json.loads(response.content)
        self.assertEqual(
            response_in_json["results"][0]["name"], "assignment 4")
        self.assertEqual(
            response_in_json["results"][1]["name"], "assignment 3")
        self.assertEqual(
            response_in_json["results"][2]["name"], "assignment 1")
