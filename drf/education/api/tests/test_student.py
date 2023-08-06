from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.create_fake_data import (CreateFakeDataGroup,
                                   CreateFakeDataStudent,
                                   CreateFakeDataStudents,
                                   CreateFakeDataMark,
                                   CreateFakeDataSubjects)

from api.models import (Marks,
                        Students,
                        Subject,
                        User,
                        Teachers,
                        Subjects,
                        Groups)

from core.models import Extension

class StudentTest(APITestCase):
    # Не каждый учитель может поставить студенту  отценку.
    # Если учитель ведет предмет у студента то он может поставить ему отценку
    # и ее поменять если данный учитель преподает данный предмет
    #Студенты могут видеть только свои отценки
    def setUp(self):
        CreateFakeDataSubjects.create()
        CreateFakeDataGroup.create()
        CreateFakeDataStudent.create()
        CreateFakeDataStudents.create()
        CreateFakeDataMark.create()

        teacher_data = {
            'username': 'Геннадий7',
            'password': '@lG)9MfmGo7',
            'first_name': 'Геннадий7',
            'last_name': 'Лазарева7',
            'email': 'apollon_2016@rambler.ru7'
        }

        self.teacher = User.objects.create_user(**teacher_data)
        Extension.objects.create(user=self.teacher, is_teacher=True)
        self.teacher_group = Teachers.objects.create(teacher=self.teacher)




    def test_set_invalid_marks(self):
        sub_first = Subjects.objects.first()
        sub = Subjects.objects.create(name='ИЗО')
        group = Groups.objects.create(name='Живопись')
        subject = Subject.objects.create(subject=sub)
        subject.group.add(group)
        subject.teacher.add(self.teacher_group)
        data = {
            "subject": sub_first.id,
            "mark": 5
        }
        student = Students.objects.first()

        self.client.force_authenticate(self.teacher)
        response = self.client.post(reverse('student-mark-list',
                                            kwargs={"student_pk":student.id}),
                                    data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        err = {'subject': {'message_error': 'No rights to change marks'}}
        self.assertEqual(response.json(),err)


