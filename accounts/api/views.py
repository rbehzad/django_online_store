from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User
from .serializers import *
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authentication import TokenAuthentication


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    model = User
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# class ProfileView(ModelViewSet):
#     authentication_classes = (TokenAuthentication,)
#     # permission_classes = [IsAuthenticated,]
#     queryset = User.objects.all()
#     serializer_class = ProfileSerializer


class RetrieveUpdateUser(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    # authentication_classes = (TokenAuthentication,)
#     # permission_classes = [IsAuthenticated,]
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        srz_data = ProfileSerializer(instance=user, data=request.data)
        if srz_data.is_valid():
            return Response(srz_data.data, status=status.HTTP_200_OK)
        else:
            return Response(srz_data.errors, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        srz_data = UpdateProfileSerializer(instance=user, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)