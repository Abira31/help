from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class CreateTeacherTests(APITestCase):
    def test_create(self):
        data = {
            "username": "Панкрат",
            "password": "XN9ONzaX*#",
            "email": "veselovaagafja@yahoo.com",
            "first_name": "Панкрат",
            "last_name": "Наумов"
        }
        response = self.client.post(reverse('create_teacher-list'),data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
