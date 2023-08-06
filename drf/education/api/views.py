from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models import Prefetch
from .serializers import (TeachersSerializers,
                          SubjectsSerializers,
                          GroupsSerializers,
                          StudentsSerializers,
                          StudentsDetailSerializers,
                          GroupDistributionSerializers,
                          SubjectSerializers,
                          TeacherDetailSerializers,
                          SubjectSaveSerializers,
                          MarksSaveSerializers,
                          MarksSerializers)

from .models import (Teachers,Subjects,
                     Groups,Subject,
                     Students,Marks)

from core.permissions import (IsTeacherOrReadOnly,
                              IsAdminUserOrReadOnly,
                              IsStudentOrReadOnly)

from core.pagination import (SubjectPagination,StudentPagination)
from core.filters import (StudentsFilter,MarksFilter)

class TeachersViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = TeachersSerializers
    queryset = Teachers.objects.all().select_related('teacher')
    def get_serializer_class(self):
        pk = self.kwargs.get('pk',None)
        if pk:
            return TeacherDetailSerializers
        return self.serializer_class


class SubjectsViewSet(ModelViewSet):
    serializer_class = SubjectsSerializers
    queryset = Subjects.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]


class GroupsViewSet(ModelViewSet):
    serializer_class = GroupsSerializers
    queryset = Groups.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object_student(self,pk):
        try:
            return Students.objects.get(pk=pk)
        except Students.DoesNotExist:
            raise ValidationError({"message_error": f"Student with this id = {pk}  does not exist"})
        except ValueError:
            raise ValidationError({"message_error": f"Student id must not be empty"})

    def get_object_group(self,pk):
        try:
            return Groups.objects.get(pk=pk)
        except Groups.DoesNotExist:
            raise ValidationError({"message_error": f"Group with this id = {pk}  does not exist"})
        except ValueError:
           raise ValidationError({"message_error": f"Group id must not be empty"})
    @action(detail=False, methods=['POST'],
            serializer_class=GroupDistributionSerializers)
    def group_to_a_student(self, request,pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    @action(detail=False,methods=['PUT'],
            serializer_class=GroupDistributionSerializers)
    def update_student_group(self,request):
        student = self.get_object_student(request.data.get('student_id'))
        group = self.get_object_group(request.data.get('group_id'))
        student.group = group
        student.save()
        return Response(status=status.HTTP_200_OK)

#
class SubjectViewSet(ModelViewSet):
    serializer_class = SubjectSerializers
    queryset = Subject.objects\
        .select_related('subject')\
        .prefetch_related('group')\
        .prefetch_related('teacher')
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = SubjectPagination

    def get_serializer_class(self):
        if self.action in ['list','create']:
            return SubjectSerializers
        elif self.action in ['retrieve','update','partial_update']:
            return SubjectSaveSerializers

    def create(self, request, *args, **kwargs):
        serializers = SubjectSaveSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = SubjectSaveSerializers(instance=instance,data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(status=status.HTTP_200_OK)

    def get_object(self):
        try:
            subject = Subject.objects.get(id=self.kwargs.get('pk'))
            return subject
        except Subject.DoesNotExist:
            raise ValidationError({"message_error": f"Subject with this id = {self.kwargs.get('pk')}  does not exist"})

class StudentsViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = StudentsSerializers
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StudentsFilter
    def get_queryset(self):
        if self.kwargs.get('group_pk',None):
            return Students.objects.filter(group=self.kwargs['group_pk'])\
                .select_related('student')\
                .select_related('group')
        return Students.objects.all()\
            .select_related('student')\
            .prefetch_related('group',
                            Prefetch('marks',queryset=Marks.objects.all()\
                                     .select_related('subject')
                                     )
                            )
class MarksViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MarksFilter
    def get_permissions(self):
        if hasattr(self.request.user, 'extension'):
            if self.request.user.extension.is_teacher:
                return [IsTeacherOrReadOnly()]
            student = Students.objects.get(student=self.request.user)
            if student.id == int(self.kwargs.get('student_pk')):
                return [IsStudentOrReadOnly()]
            return [IsTeacherOrReadOnly()]
        return [IsTeacherOrReadOnly()]
    def get_queryset(self):
        if self.request.user.extension.is_teacher:
            teacher = Teachers.objects.get(teacher=self.request.user.id)
            subject = [subject.subject for subject in Subject.objects.filter(teacher=teacher)]
            return Marks.objects.filter(student=self.kwargs.get('student_pk'),
                                       subject__in=subject) \
                .select_related('subject')
        if self.request.user.extension.is_student:
            return Marks.objects.filter(student=self.kwargs.get('student_pk')).select_related('subject')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MarksSerializers
        return MarksSaveSerializers

    def create(self, request, *args, **kwargs):
        serializers = MarksSaveSerializers(data=request.data,context={'student_pk': self.kwargs['student_pk'],
                                                                      'request':request})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = MarksSaveSerializers(instance=instance, data=request.data,context={'student_pk': self.kwargs['student_pk'],
                                                                                         'request':request})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)
