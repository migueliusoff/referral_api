from rest_framework import generics, mixins, permissions, viewsets

from api.models import ReferralCode, User
from api.serializers import (
    ReferralCodeCreateModelSerializer,
    UserRegisterModelSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


class ReferralCodeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ReferralCode.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return ReferralCodeCreateModelSerializer
