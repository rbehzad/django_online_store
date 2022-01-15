from http.client import HTTPResponse
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models import User
from .serializers import *
from rest_framework import generics, status


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    # queryset = User.objects.all()
    model = User
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RetrieveUpdateUser(generics.RetrieveUpdateAPIView):
    authentication_classes = []
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    # authentication_classes = (TokenObtainPairView,)
    # permission_classes = [IsAuthenticated,]
    def get(self, request):
        user = self.request.user
        
        srz_data = ProfileSerializer(instance=user)
        return Response(srz_data.data, status=status.HTTP_200_OK)

    def put(self, reqeust):
        user = self.request.user
        
        srz_data = UpdateProfileSerializer(instance=user, data=self.request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserImageView(generics.ListAPIView):
#     queryset = UserImage.objects.all()
#     serializer_class = UserImageSerializer

#     def post(self, request, *args, **kwargs):
#         fil = request.data['file']
#         image = UserImage.objects.create(image=fil)
#         return HTTPResponse(json.dumps({'message': "Uploaded"}), status=200)