from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from PIL import ExifTags
from io import BytesIO
from django.core.files import File


class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    kakao_id = models.BigIntegerField(null=True, unique=True)
    naver_id = models.CharField(null=True, unique=True, max_length=100)
    profile_pic = models.ImageField(upload_to="profile/%Y%m%d/", null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
