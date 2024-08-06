from django.urls import path
from .views import EmployeeListCreateView, EmployeeDetailView, LoginView, TodoListCreateView, TodoDetailView

urlpatterns = [
    path("employees/", EmployeeListCreateView.as_view(), name="employee-list-create"),
    path("employees/<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("todo/", TodoListCreateView.as_view(), name="todo-list-create"),
    path("todo/<int:pk>/", TodoDetailView.as_view(), name="todo-detail")
]


# from .views import employees_list, employee_detail, login, todo_list, todo_detail


# urlpatterns = [
#     path("employees/", employees_list),
#     path("employees/<int:employee_id>/", employee_detail),
#     path("auth/login/", login, name="get token"),
#     path("todo/", todo_list),
#     path("todo/<int:todo_id>/", todo_detail)
# ]
