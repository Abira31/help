from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.
model = [Subject,Groups,Subjects,Marks]
for m in model:
    admin.site.register(m)

class StudentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(extension__is_student=True)
        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Students,StudentAdmin)

class TeachersAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(extension__is_teacher=True)
        return super(TeachersAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(Teachers,TeachersAdmin)