from rest_framework import serializers
from .models import Task,User

'''Model serializer for Task model'''
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
'''Model serializer for User model'''
class Userserializer(serializers.ModelSerializer):
    # password2 field as confirm password field
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    # meta class to set fields and model
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True}
        }
    '''Custom method to validate password and password2'''
    def validate(self, attrs):
        # getting passwords to validate
        password = attrs.get('password')
        password2 = attrs.get('password2')
        # checking if password does not match with password2
        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match.....')
        return attrs
    
    '''Create method to create new user'''
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    
    
'''Model Serializer for login '''
class UserLoginserializer(serializers.ModelSerializer):
    # email field is added using basic validations of an email provided by serializers class
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email','password']
        
        
