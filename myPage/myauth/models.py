from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


def avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "profile/{user}/avatar/{filename}".format(
        user=instance.user,
        filename=filename,
    )


class Profile(models.Model):
    class Meta:
        verbose_name = gettext_lazy("Profile")
        verbose_name_plural = gettext_lazy("Profiles")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)