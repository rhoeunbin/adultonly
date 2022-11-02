from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    @property
    def full_name(self):
        return f'{self.last_name}{self.first_name}'
