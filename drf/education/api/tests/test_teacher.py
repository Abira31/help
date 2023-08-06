from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.create_fake_data import CreateFakeDataTeacher

class TeacherTests(APITestCase):
    def setUp(self):
        CreateFakeDataTeacher.create()
    def test_teacher_list(self):
        url = reverse('teachers-list')
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotEqual(0,len(response.json()))
    def test_teacher_detail(self):
        url = reverse('teachers-list')
        response_teacher_list = self.client.get(url, format='json')
        response_teacher = response_teacher_list.json()[0]
        response = self.client.get(response_teacher.get('url'))
        self.assertEqual(response.json().get('teacher'),response_teacher.get('teacher'))





