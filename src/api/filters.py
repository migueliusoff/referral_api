import django_filters
from django_filters import filters

from api.models import ReferralCode


class ReferralCodeFilter(django_filters.FilterSet):
    email = filters.CharFilter(method="filter_email")

    def filter_email(self, queryset, name, value):
        filtered_qs = queryset.filter(user__email=value, is_active=True)
        if not filtered_qs.exists():
            return ReferralCode.objects.none()
        obj = filtered_qs.first()
        if obj.is_expired:
            return ReferralCode.objects.none()
        return filtered_qs

    class Meta:
        model = ReferralCode
        fields = []
