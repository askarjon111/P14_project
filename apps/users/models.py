import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.common.models import BaseModel, File
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Custom user model that supports using phone_number instead of username"""

    phone_number = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    car_model = models.CharField(max_length=255,blank=True, null=True)
    profile_picture = models.OneToOneField(File, null=True, blank=True, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


class ConfirmationCode(BaseModel):
    code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=13)
    user = models.ForeignKey(User, blank=True, null=True, related_name="confirmation_codes", on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)


    def confirmed_code(self):
        if self.confirmed and self.created_at > timezone.now() - datetime.timedelta(minutes=5):
            return True
        else:
            return False

    def on_time(self):
        if self.created_at > timezone.now() - datetime.timedelta(minutes=2):
            return True
        else:
            return False
