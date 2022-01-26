from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from accounts.models import User, OTPRequest
from django.contrib.auth.password_validation import validate_password


class RequestOTPSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=50, allow_null=False)
    channel = serializers.ChoiceField(allow_null=False, choices=OTPRequest.OtpChannel.choices)
    # class Meta:
    #     model = OTPRequest
    #     fields = ('receiver', 'channel')


class RequestOTPResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ('request_id',)


class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null=False)
    password = serializers.CharField(max_length=4, allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)


class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)
    message = serializers.CharField(max_length=220)
    

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
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

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
        fields = ('id', 'email', 'first_name', 'last_name', 'image')


