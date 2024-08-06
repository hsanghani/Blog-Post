from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView, LoginView, TodoListCreateView, TodoDetailView

urlpatterns = [
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("todo/", TodoListCreateView.as_view(), name="todo-list-create"),
    path("todo/<int:pk>/", TodoDetailView.as_view(), name="todo-detail")
]