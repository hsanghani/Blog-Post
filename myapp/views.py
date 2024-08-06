# from rest_framework import generics, status, permissions
# from rest_framework.response import Response
# from .models import Employees, Todo
# from .serializers import TodoSerializer, EmployeeSerializer
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.contrib.auth import authenticate
# from .tokens import create_jwt_pair_for_user

# class EmployeeListCreateView(generics.ListCreateAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         response = {"message": "Employee Created Successfully", "data": serializer.data}
#         return Response(response, status=status.HTTP_201_CREATED, headers=headers)

# class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employees.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'pk'

# class LoginView(generics.GenericAPIView):
#     serializer_class = EmployeeSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = authenticate(email=email, password=password)
#         if user is not None:
#             tokens = create_jwt_pair_for_user(user)
#             response = {"message": "Login Successful", "tokens": tokens}
#             return Response(data=response, status=status.HTTP_200_OK)
#         else:
#             return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

# class TodoListCreateView(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     lookup_field = 'pk'


from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Employees, Todo
from .serializers import TodoSerializer, EmployeeSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .tokens import create_jwt_pair_for_user
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import time


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  

    def list(self, request, *args, **kwargs):
        cache_key = 'employee_list'
        employees = cache.get(cache_key)

        if not employees:
            print("not employee list")
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            return Response(serializer.data)
        else:
            print("cache employee")
            return Response(employees)


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('employee_list')
        return response

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # response = {"message": "Employee Created Successfully", "data": serializer.data}
        # return Response(response, status=status.HTTP_201_CREATED, headers=headers)

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Employees.objects.all()
    # serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'pk'

    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('employee_list')
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('employee_list')
        return response

# class LoginView(generics.GenericAPIView):
#     serializer_class = EmployeeSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = []  

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         user = authenticate(email=email, password=password)
#         if user is not None:
#             tokens = create_jwt_pair_for_user(user)
#             response = {"message": "Login Successful", "tokens": tokens}
#             return Response(data=response, status=status.HTTP_200_OK)
#         else:
#             return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        cache_key = f"user_tokens_{email}"
        print("CACHE_TTL::>>",CACHE_TTL)
        cached_tokens = cache.get(cache_key)

        if cached_tokens:
            print("cached tokens ::>>",cached_tokens)
            response = {"message": "Login Successful", "tokens": cached_tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            cache.set(cache_key, tokens, timeout=CACHE_TTL)
            response = {"message": "Login Successful", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(generics.GenericAPIView):
#     serializer_class = EmployeeSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         cache_key = f"user_tokens_{email}"
#         cached_tokens = cache.get(cache_key)

#         if cached_tokens:
#             # Assuming the cached tokens include an expiration timestamp
#             token_expiration = cached_tokens.get("expires_at")
#             print(token_expiration)
#             print(time.time())
#             if token_expiration and token_expiration > time.time():
#                 # Token is valid
#                 response = {"message": "Login Successful", "tokens": cached_tokens}
#                 return Response(data=response, status=status.HTTP_200_OK)
#             else:
#                 # Token has expired, generate a new one
#                 print("email ::>",email)
#                 tokens = self._generate_and_cache_tokens(email,password)
#                 response = {"message": "Token expired, new token generated", "tokens": tokens}
#                 return Response(data=response, status=status.HTTP_200_OK)

#         # If no cached tokens, authenticate and generate new tokens
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             print("email :::::>>>>>",email)
#             tokens = self._generate_and_cache_tokens(email,password)
#             response = {"message": "Login Successful", "tokens": tokens}
#             return Response(data=response, status=status.HTTP_200_OK)
#         else:
#             return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

#     def _generate_and_cache_tokens(self, email,password):
#         # Create new tokens
#         user = authenticate(email=email,password=password)  # Assuming user is authenticated here
#         print("user check :::>>",user)
#         tokens = create_jwt_pair_for_user(user)
#         # Add expiration timestamp to tokens
#         tokens["expires_at"] = time.time() + CACHE_TTL
#         # Cache the tokens with TTL
#         cache.set(f"user_tokens_{email}", tokens, timeout=CACHE_TTL)
#         return tokens


# class TodoListCreateView(generics.ListCreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     lookup_field = 'pk'



class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        cache_key = 'todo_list'
        todos = cache.get(cache_key)

        if not todos:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            return Response(serializer.data)

        return Response(todos)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('todo_list')  # Invalidate cache when a new Todo is created
        return response

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('todo_list')  # Invalidate cache when a Todo is updated
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('todo_list')  # Invalidate cache when a Todo is deleted
        return response




































# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework import status
# from .models import Employees, Todo
# from .serializers import TodoSerializer, EmployeeSerializer
# from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from django.contrib.auth import authenticate
# from .tokens import create_jwt_pair_for_user
# from .permissions import AdminOrReadOnly

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def employees_list(request):
    # if request.method == 'GET':
    #     employees = Employees.objects.all()
    #     serializer = EmployeeSerializer(employees, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # if request.method == 'POST':
    #     serializer = EmployeeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {"message": "Employee Created Successfully", "data": serializer.data}
    #         return Response(data=response, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#     email = request.data.get("email")
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(email=email, password=password)
#     if user is not None:
#         tokens = create_jwt_pair_for_user(user)
#         response = {"message": "Login Successful", "tokens": tokens}
#         return Response(data=response, status=status.HTTP_200_OK)
#     else:
#         return Response(data={"message": "Invalid email or password"})




# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def employee_detail(request, employee_id):
    # try:
    #     employee = Employees.objects.get(pk=employee_id)
    # except Employees.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # if request.method == 'PUT':
    #     serializer = EmployeeSerializer(employee, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == "GET":
    #     serializer = EmployeeSerializer(employee)
    #     return Response(serializer.data, status=status.HTTP_302_FOUND)
    # elif request.method == 'DELETE':
    #     employee.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def todo_list(request):
#     if request.method == 'GET':
#         leave_requests = Todo.objects.all()
#         serializer = TodoSerializer(leave_requests, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'POST':
#         serializer = TodoSerializer(data=request.data)
#         if serializer.is_valid():
#             todo = serializer.save(user=request.user)  # Save the Todo with the user

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def todo_detail(request, todo_id):
#     try:
#         todo = Todo.objects.get(pk=todo_id)
#     except Todo.DoesNotExist:
#         return Response({"msg":"plz input valid id"},status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         serializer = TodoSerializer(todo, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "GET":
#         serializer = TodoSerializer(todo)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
#     elif request.method == 'DELETE':
#         todo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
