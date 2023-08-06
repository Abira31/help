from rest_framework.permissions import BasePermission,SAFE_METHODS
from api.models import Teachers,Subject
class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user,'extension'):
            return bool(request.user.extension.is_teacher)
        return False

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_staff)

class IsStudentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'extension'):
            if bool(request.user.extension.is_student) and request.method in SAFE_METHODS:
                return True
            return False
        return False


