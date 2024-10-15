from django.contrib import admin

from api.models import ReferralCode


class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "value", "is_active")


admin.site.register(ReferralCode, ReferralCodeAdmin)
