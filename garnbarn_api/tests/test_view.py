from garnbarn_api.models import Tag, Assignment, CustomUser
from datetime import datetime, timedelta
from rest_framework.test import force_authenticate, APITestCase
from django.contrib.auth.models import User
import json
import math


def convert_to_json(data):
    """Convert data into json format"""
    data = json.loads(data)
    # data = json.dumps(data)
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
        self.tag = Tag.objects.create(name="test_tag")
        assignment = Assignment(
            assignment_name="assignment 1",
            tag=self.tag,
            timestamp=self.current_time,
            due_date=self.end_date,
            description="test"
        )
        assignment.save()

    def test_assignment_not_existed_assignment(self):
        """Raise 404 status code when assignment's object does not exist"""
        response = self.client.get("/api/v1/assignment/0/")
        self.assertEqual(404, response.status_code)

    def test_get(self):
        """Return detail of the assignment"""
        response = self.client.get("/api/v1/assignment/1/")
        converted_data = convert_to_json(response.content)
        timestamp_cache_from_request = converted_data["timestamp"]
        del converted_data["timestamp"]
        expected_result = json.dumps({
            "id": 1,
            "tag": {
                "id": 1,
                "name": "test_tag",
                "color": None
            },
            "name": "assignment 1",
            "dueDate": self.end_date_timestamp,
            "description": "test"
        })
        self.assertJSONEqual(expected_result, converted_data)
        self.assertAlmostEqual(timestamp_cache_from_request,
                               self.current_timestamp, delta=2)
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
            "dueDate": self.end_date_timestamp,
            "description": "assignment 2's detail"
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

    def test_patch(self):
        """Update assignment object"""
        data = json.dumps({
            "name": "renamed",
            "dueDate": self.end_date_timestamp + 10000
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
            "description": "test"
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


def create_assignment(name, due_date):
    return Assignment.objects.create(assignment_name=name, due_date=due_date)


class FromPresentTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(uid="1234")
        self.client.force_authenticate(user=self.user)

        yesterday = datetime.now() + timedelta(days=-1)
        today = datetime.today()
        tomorrow = datetime.now() + timedelta(days=1)

        self.assignment1 = create_assignment("assignment 1", tomorrow)
        self.assignment2 = create_assignment("assignment 2", yesterday)
        self.assignment3 = create_assignment("assignment 3", today)

    def test_not_frompresent(self):
        """Normal GET method"""
        response = self.client.get("/api/v1/assignment/")
        self.assertEqual(json.loads(response.content)["count"], 3)

    def test_frompresent_is_true(self):
        """Adding fromPresent=true"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        # fromPresent=true will exclude assignment with due date < today
        self.assertEqual(json.loads(response.content)["count"], 2)
        # response should only contain assignment 3 and 1
        self.assertIn(self.assignment1.get_json_data(),
                      json.loads(response.content)["results"])
        self.assertIn(self.assignment3.get_json_data(),
                      json.loads(response.content)["results"])

    def test_frompresent_order(self):
        """The assignment should be ordered by its due date"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        self.assertEqual(json.loads(response.content)[
                         "results"][0]["name"], "assignment 3")
        self.assertEqual(json.loads(response.content)[
                         "results"][1]["name"], "assignment 1")
