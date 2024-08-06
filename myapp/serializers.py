from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError as SValidationError
from rest_framework.validators import ValidationError
from .models import Employees, Todo
from django.utils.timezone import now
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

class EmployeeSerializer(ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Employees
        fields = ['id', 'first_name', 'last_name', 'password', 'phone', 'email', 'address', 'role', 'date_of_birth','gender','username']

    def validate(self, attrs):
        email_exists = Employees.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        employee = super().create(validated_data)
        employee.set_password(password)
        employee.save()
        return employee



class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'name', 'done', 'date_created', 'user']
        # fields = '__all__'
        read_only_fields = ['user']
