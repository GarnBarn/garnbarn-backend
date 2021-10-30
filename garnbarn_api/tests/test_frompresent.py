from django.http import response
from django.test import client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from garnbarn_api.models import Assignment

import json
from math import floor
from datetime import datetime, timedelta


def create_assignment(name, due_date):
    return Assignment.objects.create(assignment_name=name, due_date=due_date)


class FromPresentTest(APITestCase):
    def setUp(self):
        yesterday = datetime.now() + timedelta(days=-1)
        today = datetime.today()
        tomorrow = datetime.now() + timedelta(days=1)

        self.assignment1 = create_assignment("assignment 1", tomorrow)
        self.assignment2 = create_assignment("assignment 2", yesterday)
        self.assignment3 = create_assignment("assignment 3", today)

    def test_not_frompresent(self):
        """Normal GET method"""
        response = self.client.get("/api/v1/assignment/")
        expected = ("assignment 1", "assignment 2", "assignment 3")
        self.assertEqual(json.loads(response.content)["count"], 3)

    def test_frompresent_is_true(self):
        """Adding fromPresent=true"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        # fromPresent=true will exclude assignment with due date < today
        self.assertEqual(json.loads(response.content)["count"], 2)

    def test_frompresent_order(self):
        """The assignment should be ordered by its due date"""
        response = self.client.get("/api/v1/assignment/?fromPresent=true")
        self.assertEqual(json.loads(response.content)[
                         "results"][0]["name"], "assignment 3")
        self.assertEqual(json.loads(response.content)[
                         "results"][1]["name"], "assignment 1")
