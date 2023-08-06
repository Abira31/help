from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Extension

admin.site.register(Extension)
# Register your models here.
class Extension(admin.StackedInline):
    model = Extension
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (Extension,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)