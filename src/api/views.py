from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import ReferralCodeFilter
from api.models import ReferralCode, User
from api.serializers import (
    ReferralCodeCreateModelSerializer,
    ReferralCodeListModelSerializer,
    UserModelSerializer,
    UserRegisterModelSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer


class ReferralCodeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = ReferralCode.objects.all().select_related("user")
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


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    @action(detail=True, methods=["get"])
    def referrals(self, request, *args, **kwargs):
        return Response(UserModelSerializer(self.get_object().referrals.all(), many=True).data)
