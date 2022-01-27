import uuid
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.api.serializers import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.api.permissions import PhoneNumberConfirmationPermission
from drf_yasg.utils import swagger_auto_schema

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny, PhoneNumberConfirmationPermission)
    serializer_class = MyTokenObtainPairSerializer
    
    def permission_denied(self, request, message=None, code=None):
        message = 'Wrong email/password or your phone number is not confirmed!'
        return super().permission_denied(request, message, code)


class RegisterView(generics.CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RetrieveUpdateUser(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated,]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)


class OTP_get_request_id_view(APIView):
    @swagger_auto_schema(request_body=RequestOTPSerializer)
    def post(self, request): # take args in request url
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if not User.objects.filter(phone_number=data['receiver']).exists():
                phone_number = data['receiver']
                return Response(status=status.HTTP_404_NOT_FOUND, data=f'User with {phone_number} phone number not found')

            otp = OTPRequest.objects.generate(data) # create model
            return Response(data=RequestOTPResponseSerializer(otp).data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class OTP_validate_view(APIView):
    @swagger_auto_schema(request_body=VerifyOtpRequestSerializer)
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'], data['request_id'], data['password']):
                return Response(self._handle_login(data))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data='Wrong Password')

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, otp):
        query = User.objects.filter(phone_number=otp['receiver'])
        if query.exists():
            user = query.first()
            user.phone_number_confirmation = True
            user.save()
            refresh = RefreshToken.for_user(user)
            return ObtainTokenSerializer({
                'refresh': str(refresh),
                'token': str(refresh.access_token),
                'message': 'Successfully Login',
            }).data
