from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user_name",
        "bio_short",
        "agreement_accepted",
    )
    list_display_links = (
        "pk",
        "user_name",
    )

    def bio_short(self, obj: Profile) -> str:
        if len(obj.bio) > 48:
            return obj.bio[:48] + "..."
        return obj.bio

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Profile.objects.select_related("user")

    def user_name(self, obj: Profile) -> str:
        return obj.user.first_name or obj.user.username