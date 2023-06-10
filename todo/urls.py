from django.contrib import admin
from django.urls import path,include
from todoApp.views import TodoViewSet,UserRegisteration,UserLoginView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

''# Default router is used to define a router which automatically generates url routes''
# as per the registeration of router all the routes will be starting with 'api/todo' for TodoViewset view 
# List endpoint: GET 'api/todo/'
# Create endpoint POST 'api/todo'
# Detail endpoint GET 'api/todo/<pk>'
# Update endpoint PUT 'api/todo/<pk>'
# Delete endpoint DELETE 'api/todo/<pk>'
router = DefaultRouter()
router.register('api/todo',TodoViewSet)

'''url patterns include all the url routes''' 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api/todo/user/register/', UserRegisteration.as_view(), name='register'),
    path('api/todo/user/login/', UserLoginView.as_view(), name='login'),
]

# admin is to access admin area
# api/todo/user/register/ is to access UserRegisteration view
# api/todo/user/login/ is to access UserLogin view 
