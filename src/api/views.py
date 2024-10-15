from rest_framework import generics, permissions

from api.models import User
from api.serializers import UserRegisterModelSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer
    permission_classes = [permissions.AllowAny]
