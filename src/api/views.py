from rest_framework import generics, mixins, permissions, viewsets

from api.filters import ReferralCodeFilter
from api.models import ReferralCode, User
from api.serializers import (
    ReferralCodeCreateModelSerializer,
    ReferralCodeListModelSerializer,
    UserRegisterModelSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


class ReferralCodeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = ReferralCode.objects.filter().select_related("user")
    filterset_class = ReferralCodeFilter

    def get_permissions(self):
        if self.action == "list":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return ReferralCodeCreateModelSerializer

        if self.action == "list":
            return ReferralCodeListModelSerializer
