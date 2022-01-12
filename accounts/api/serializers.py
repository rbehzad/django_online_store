from django.db import models
from django.db.models import fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ('email', 'password', 'password2', 'phone_number', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'seller',)


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')

