from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']


class RegisterUserSerializer(serializers.ModelSerializer):
    # Password input; write_only ensures it won't be returned in API responses
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','email', 
                  'phone_number', 'role', 'password', 'confirm_password']

    def validate_username(self, username):
        """
        Normalize username by lowercasing, stripping spaces, 
        and removing inner spaces. Also check uniqueness.
        """
        username = username.lower().strip().replace(" ", "")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return username

    def validate_email(self, email):
        """Validate email format and uniqueness"""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email
    
    def validate_phone_number(self, phone_number):
        """
        Validate phone number format if provided
        Must match +254XXXXXXXXX format
        """
        if phone_number:
            # Basic phone number validation (adjust regex as needed)
            phone_template = re.compile(r'^\+254\d{9}')
            if not phone_template.match(phone_number):
                raise serializers.ValidationError("Enter a valid phone number. +254*********")
            if User.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("A user with this phone_number already exists.")
        return phone_number
    
    def validate(self, validated_data):
        """Validate password confirmation matches password"""
        if validated_data.get('password') != validated_data.get('confirm_password'):
            raise serializers.ValidationError("Password confirmation does not match.")
        return validated_data
    
    def create(self, validated_data):
        """
        Create user with encrypted password
        - Remove confirm_password
        - Set password securely using set_password()
        """
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    # Fields for login input
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate login credentials:
        - Authenticate the user
        - Check if account is active
        - Generate JWT refresh and access tokens
        - Return user object and tokens if successful
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid Credentials")
            
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            
            refresh = RefreshToken.for_user(user)
            
            data['user'] = user
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        
        raise serializers.ValidationError("Both username and password are required")