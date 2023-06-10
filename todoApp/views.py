from django.shortcuts import render
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import TodoSerializer,Userserializer,UserLoginserializer
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

'''Helper function to generate JWT tokens for a user'''

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # refresh is a variable holding refresh token 
    # this function will return a dictionary of refresh and access token
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token)
    }

'''Model viewset to manage tasks '''
class TodoViewSet(viewsets.ModelViewSet):
    # queyset holding all Model objects of Task model
    queryset = Task.objects.all()
    # serializer class is the serializer we are using to validate and serialize data
    serializer_class = TodoSerializer
    # permission class is used to specify only authenticated user can access this api
    permission_classes = [IsAuthenticated]

    '''Cusotom method to mark task as completed'''
    @action(detail=True, methods=['POST'])
    def mark_as_completed(self, request, pk=None):
        # Accessing the requested task from all model objects
        todo = Task.objects.get(id=pk)
        # Setiting done True for the model object in todo variable 
        todo.done = True
        todo.save()
        # sending back the data to serializer to serialize data
        serializer = self.get_serializer(todo)
        return Response(serializer.data) 
    
    
    
'''API view for user registeration'''
class UserRegisteration(APIView):
    
    '''post method for user registeration'''
    @action(detail=True, methods=['POST'])
    def post(self,request):
        # sending data to serializer 
        serializer = Userserializer(data=request.data)
        # checking for validations if there will be any exception then raise the exception
        if serializer.is_valid(raise_exception=True):
            # saving user with requested data
            user =  serializer.save()
            # getting tokens from helper function
            token = get_tokens_for_user(user)
            # status 201 is sent as response as new user is created 
            return Response({'token':token,'msg':'Registeration ok'},status=status.HTTP_201_CREATED)
        # status 400(Bad Request) is sent if data is not valid 
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


'''API view for user login'''
    
class UserLoginView(APIView):
    
    
    '''post method for user login'''
    @action(detail=True, methods=['POST'])
    def post(self,request):
        # sending data to serializer
        serializer = UserLoginserializer(data = request.data)
        # checking for validations if there will be any exception then raise the exception
        if serializer.is_valid(raise_exception=True):
            # getting email and password to authenticate the user
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email,password=password)
            # checking if user exists or not
            if user is not None:
                # token will be generated if user exists and sending status 200(Ok)
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login ok'},status=status.HTTP_200_OK)
            else:
                # if user not exists then 404(Not Found) is sent 
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)