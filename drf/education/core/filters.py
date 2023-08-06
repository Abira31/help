from django_filters.rest_framework import FilterSet
from api.models import Students,Marks

class StudentsFilter(FilterSet):
    class Meta:
        model = Students
        fields = {
            'student__first_name':['exact'],
            'student__last_name': ['exact'],
            'group__name': ['exact']
        }

class MarksFilter(FilterSet):
    class Meta:
        model = Marks
        fields = {
            'subject__name': ['exact']
        }
