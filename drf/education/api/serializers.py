from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (Teachers,Subjects,
                     Groups,Subject,
                     Students,Marks)
from django.core.validators import MinValueValidator
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        read_only_fields = ['first_name','last_name','email']




class TeachersSerializers(serializers.ModelSerializer):
    teacher = UserSerializers()
    class Meta:
        model = Teachers
        fields = ['url','teacher']



class TeachersUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

#
class SubjectsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['name','url']
#
class GroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['name','url']

class SubjectSerializers(serializers.ModelSerializer):
    subject = SubjectsSerializers()
    group = GroupsSerializers(many=True)
    teacher = TeachersSerializers(many=True)
    class Meta:
        model = Subject
        fields = ['url','subject','group','teacher']

class SubjectSaveSerializers(serializers.Serializer):
    subject = serializers.IntegerField()
    group = serializers.ListField(
        child=serializers.IntegerField()
    )
    teacher = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_subject(self, attrs):
        try:
            Subjects.objects.get(id=attrs)
        except Subjects.DoesNotExist:
            raise serializers.ValidationError({"message_error":f"Subject with this id = {attrs}  does not exist"})
        return attrs
    def validate_group(self, attrs):
        err = []
        if len(attrs) == 0:
            raise serializers.ValidationError({"message_error": f"Groups with this ID {err} must not be empty"})
        for attr in attrs:
            try:
                Groups.objects.get(id=attr)
            except Groups.DoesNotExist:
                err.append(attr)
        if len(err) > 0:
            raise serializers.ValidationError({"message_error": f"Groups with this id in {list(set(err))} does not exist"})
        return attrs
    def validate_teacher(self, attrs):
        err = []
        if len(attrs) == 0:
            raise serializers.ValidationError({"message_error": f"Teachers with this ID {err} must not be empty"})
        for attr in attrs:
            try:
                Teachers.objects.get(id=attr)
            except Teachers.DoesNotExist:
                err.append(attr)
        if len(err) > 0:
            raise serializers.ValidationError({"message_error": f"Teachers with this id in {list(set(err))} does not exist"})
        return attrs
    def create(self, validated_data):
        subject = Subject.objects.create(
            subject = Subjects.objects.get(id=validated_data.get('subject'))
        )
        subject.group.add(*[Groups.objects.get(id=i) for i in validated_data.get('group')])
        subject.teacher.add(*[Teachers.objects.get(id=i) for i in validated_data.get('teacher')])
        return subject
    def update(self, instance, validated_data):
        instance.subject = Subjects.objects.get(id=validated_data.get('subject'))
        instance.group.clear()
        instance.group.add(*[Groups.objects.get(id=i) for i in validated_data.get('group')])
        instance.teacher.clear()
        instance.teacher.add(*[Teachers.objects.get(id=i) for i in validated_data.get('teacher')])
        return instance
class TeacherSubjectSerializers(serializers.ModelSerializer):
    subject = SubjectsSerializers()
    group = GroupsSerializers(many=True)
    class Meta:
        model = Subject
        fields = ['subject', 'group']
class TeacherDetailSerializers(serializers.ModelSerializer):
    teacher = UserSerializers()
    subject = TeacherSubjectSerializers(many=True)
    class Meta:
        model = Teachers
        fields = ['teacher','subject']

class StudentsSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="students-detail")
    student = UserSerializers()
    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Students
        fields = ['url','student','group']
#
class MarksSerializers(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name',read_only=True)
    mark = serializers.IntegerField(read_only=True)
    class Meta:
        model = Marks
        fields = ['id','subject','mark']

class MarksSaveSerializers(serializers.ModelSerializer):
    subject = serializers.IntegerField(source='subject.id')
    class Meta:
        model = Marks
        fields = ['subject', 'mark']

    def validate_subject(self, attrs):
        teacher = Teachers.objects.get(teacher=self.context.get('request').user)
        subjects = Subject.objects.filter(teacher=teacher)
        subject_list = []
        if subjects.count() > 0:
            subject_list = [sub.subject.name for sub in subjects]
        subject = Subjects.objects.get(id=attrs)
        if subject.name in subject_list:
            return attrs
        raise serializers.ValidationError({"message_error": f"No rights to change marks"})

    def create(self, validated_data):
        student = Students.objects.get(id=self.context['student_pk'])
        subject = Subjects.objects.get(id=self.validated_data.get('subject')['id'])
        mark = self.validated_data.get('mark')
        mark = Marks.objects.create(student=student,subject=subject,mark=mark)
        return mark
    def update(self, instance, validated_data):
        instance.subject = Subjects.objects.get(id=self.validated_data.get('subject')['id'])
        instance.mark = self.validated_data.get('mark')
        instance.save()
        return instance

class StudentsDetailSerializers(serializers.ModelSerializer):
    student = UserSerializers()
    marks = MarksSerializers(many=True)
    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Students
        fields = ['student','group','marks']

class GroupDistributionSerializers(serializers.Serializer):
    student_id = serializers.IntegerField(validators=[MinValueValidator(1)])
    group_id = serializers.IntegerField(validators=[MinValueValidator(1)])
    def save(self, **kwargs):
        student_id = self.validated_data['student_id']
        group_id = self.validated_data['group_id']
        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            raise serializers.ValidationError({"message_error":f"Student with this id = {student_id}  does not exist"})
        try:
            group = Groups.objects.get(id=group_id)
        except Groups.DoesNotExist:
            raise serializers.ValidationError({"message_error":f"Group with this id = {group_id}  does not exist"})

        student.group = group
        student.save()
        return student

