from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.create_fake_data import CreateFakeDataGroup
from api.models import User,Teachers,Groups,Students
from core.models import Extension

class GroupTests(APITestCase):
    def setUp(self):
        CreateFakeDataGroup.create()
        user_teacher = {
            'username': 'Михей', 'password': '+q!I0NDsk!',
            'first_name': 'Михей', 'last_name': 'Рогова',
            'email': 'kotovaalla@gmail.com'
        }
        user_student = {
            'username': 'Ираида', 'password': 'Qo6%UbK(g^',
            'first_name': 'Ираида', 'last_name': 'Журавлева',
            'email': 'anzhela_46@rambler.ru'
        }
        user_admin = {
            'username': 'Пантелеймон',
            'password': '6P8RxV1lg(',
            'email': 'pantelemon_1976@yandex.ru'
        }
        self.group_data = {
            "name": "магистратура"
        }
        self.user_teacher = User.objects.create_user(**user_teacher)
        Extension.objects.create(user=self.user_teacher, is_teacher=True)
        Teachers.objects.create(teacher=self.user_teacher)
        self.user_admin = User.objects.create_superuser(**user_admin)
        self.user_student = User.objects.create_user(**user_student)
        Extension.objects.create(user=self.user_student, is_student=True)
        self.student = Students.objects.create(student=self.user_student)


    def test_group_list(self):
        response = self.client.get(reverse('groups-list'),format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertNotEqual(0,len(response.json()))

    def test_group_detail(self):
        response_subjects_list = self.client.get(reverse('groups-list'), format='json')
        response_subject = response_subjects_list.json()[0]
        response = self.client.get(response_subject.get('url'))
        self.assertEqual(response.json(),response_subject)

    def test_group_invalid_post(self):
        response = self.client.post(reverse('groups-list'), data=self.group_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(self.user_teacher)
        response = self.client.post(reverse('groups-list'), data=self.group_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_valid_post(self):
        self.client.force_authenticate(self.user_admin)
        response = self.client.post(reverse('groups-list'),self.group_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_group_valid_put(self):
        self.client.force_authenticate(self.user_admin)
        group = Groups.objects.filter(name='3 курс').first()
        data = {"name":"3-про курс"}
        response = self.client.put(reverse('groups-detail',kwargs={"pk":group.id}),data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(data.get('name'),response.json().get('name'))

    def test_group_valid_delete(self):
        self.client.force_authenticate(self.user_admin)
        group = Groups.objects.first()
        response = self.client.delete(reverse('groups-detail',kwargs={"pk":group.id}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_group_set_student(self):
        self.client.force_authenticate(self.user_admin)
        self.assertIsNone(self.student.group)
        group = Groups.objects.first()
        data = {
            "student_id":self.student.id,
            "group_id":group.id
        }
        response = self.client.post(reverse('groups-group-to-a-student'),data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.student.refresh_from_db()
        self.assertIsNotNone(self.student.group)

    def test_group_update_student(self):
        self.client.force_authenticate(self.user_admin)
        group = Groups.objects.last()
        data = {
            "student_id":self.student.id,
            "group_id":group.id
        }
        response = self.client.put(reverse('groups-update-student-group'), data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)










