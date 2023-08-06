from abc import ABC,abstractmethod
from django.contrib.auth.models import User
from core.models import Extension
from api.models import (Subject,Groups,
                        Teachers,Students,
                        Subjects,Marks)
from core.fake_data import teachers,students,groups,subjects
import random

class CreateFakeDataABC(ABC):
    teachers = []
    students = []
    groups = []
    subjects = []
    teachers_group = []
    students_group = []
    @classmethod
    @abstractmethod
    def create(cls):
        pass

class CreateFakeDataTeacher(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for teacher in teachers:
            user = User.objects.create_user(**teacher)
            Extension.objects.create(user=user, is_teacher=True)
            cls.teachers_group.append(Teachers.objects.create(teacher=user))
            cls.teachers.append(user)
class CreateFakeDataStudent(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for student in students:
            user = User.objects.create_user(**student)
            Extension.objects.create(user=user, is_student=True)
            cls.students.append(user)
class CreateFakeDataGroup(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for group in groups:
            cls.groups.append(Groups.objects.create(**group))
class CreateFakeDataSubjects(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for subject in subjects:
            cls.subjects.append(Subjects.objects.create(**subject))
class CreateFakeDataStudents(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for student in cls.students:
            cls.students_group.append(Students.objects.create(student=student, group=random.choice(cls.groups)))
class CreateFakeDataSubject(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for _ in range(0,5):
            subject = random.choice(cls.subjects)
            groups = random.choices(cls.groups,k=random.randint(1,len(cls.groups)))
            teachers = random.choices(cls.teachers_group,k=random.randint(1,3))
            sub = Subject.objects.create(subject=subject)
            sub.group.add(*[group.id for group in groups])
            sub.teacher.add(*[teacher.id for teacher in teachers])
class CreateFakeDataMark(CreateFakeDataABC):
    @classmethod
    def create(cls):
        for _ in range(0, 100):
            student = random.choice(cls.students_group)
            subject = random.choice(cls.subjects)
            Marks.objects.create(student=student, subject=subject, mark=random.randint(2, 5))
class CreateFakeData(CreateFakeDataABC):
    @classmethod
    def create(cls):
        CreateFakeDataTeacher.create()
        CreateFakeDataStudent.create()
        CreateFakeDataGroup.create()
        CreateFakeDataSubjects.create()
        CreateFakeDataStudents.create()
        CreateFakeDataSubject.create()
        CreateFakeDataMark.create()


