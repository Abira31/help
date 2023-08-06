from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class CreateStudentTests(APITestCase):
    def test_create(self):
        data = {
            "username": "Прокофийй",
            "password": "&2LFO2jZZx",
            "email": "turovvitali@yahoo.com",
            "first_name": "Прокофийй",
            "last_name": "Яковлев"
        }
        response = self.client.post(reverse('create_student-list'),data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


