from django.contrib.auth.backends import ModelBackend
from .models import Employees

class EmployeesBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            employee = Employees.objects.get(email=email)
            if employee.check_password(password):
                return employee
        except Employees.DoesNotExist:
            return None

