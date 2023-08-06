from djoser.serializers import (UserCreateSerializer as BaseUserCreate )
from django.contrib.auth.models import User
from .models import Extension
from api.models import Students,Teachers

class StudentsCreateSerializer(BaseUserCreate):
    class Meta(BaseUserCreate.Meta):
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    def save(self, **kwargs):
        user = User.objects.create_user(**self.validated_data)
        Extension.objects.create(user=user,is_student=True)
        Students.objects.create(student=user)
        return user


class TeachersCreateSerializer(BaseUserCreate):
    class Meta(BaseUserCreate.Meta):
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    def save(self, **kwargs):
        user = User.objects.create_user(**self.validated_data)
        Extension.objects.create(user=user, is_teacher=True)
        Teachers.objects.create(teacher=user)
        return user