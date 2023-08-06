from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .serializers import StudentsCreateSerializer,TeachersCreateSerializer
from django.contrib.auth.models import User


class StudentCreateAPIView(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = StudentsCreateSerializer

class TeacherCreateAPIView(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = TeachersCreateSerializer
