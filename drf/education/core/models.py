from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Extension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True,related_name='extension')
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    def __str__(self):
        return 'Сustom extensions'