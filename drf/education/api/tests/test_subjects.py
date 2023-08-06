from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import User,Teachers,Subjects
from core.models import Extension
from core.create_fake_data import CreateFakeDataSubjects
class SubjectsTests(APITestCase):
    def setUp(self):
        CreateFakeDataSubjects.create()
        self.subject_data = {
            "name":"Физика"
        }
        user_teacher = {
            'username': 'Симон', 'password': '#3RkWrl99p',
            'first_name': 'Симон', 'last_name': 'Степанов',
            'email': 'nikolaevseliverst@rambler.ru'
        }
        user_admin = {
            'username':'Ипполит',
            'password':'A+u6RNkhsb',
            'email':'pzinoveva@rambler.ru'
        }
        self.user_teacher = User.objects.create_user(**user_teacher)
        Extension.objects.create(user=self.user_teacher, is_teacher=True)
        Teachers.objects.create(teacher=self.user_teacher)
        self.user_admin = User.objects.create_superuser(**user_admin)

    def test_subjects_list(self):
        response = self.client.get(reverse('subjects-list'),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotEqual(0,len(response.json()))

    def test_teacher_detail(self):
        response_subjects_list = self.client.get(reverse('subjects-list'), format='json')
        response_subject = response_subjects_list.json()[0]
        response = self.client.get(response_subject.get('url'))
        self.assertEqual(response.json(),response_subject)

    def test_teacher_invalid_post(self):
        response = self.client.post(reverse('subjects-list'),data=self.subject_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.user_teacher)
        response = self.client.post(reverse('subjects-list'), data=self.subject_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_valid_post(self):
        self.client.force_authenticate(self.user_admin)
        response = self.client.post(reverse('subjects-list'),self.subject_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_subjects_valid_put(self):
        self.client.force_authenticate(self.user_admin)
        subject = Subjects.objects.filter(name='Биология').first()
        data = {"name":"Физика"}
        response = self.client.put(reverse('subjects-detail',kwargs={"pk":subject.id}),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(data.get('name'),response.json().get('name'))

    def test_subjects_valid_delete(self):
        self.client.force_authenticate(self.user_admin)
        subject = Subjects.objects.first()
        response = self.client.delete(reverse('subjects-detail',kwargs={"pk":subject.id}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)





