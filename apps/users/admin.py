from django.contrib import admin
from apps.users.models import ConfirmationCode, User


admin.site.register(ConfirmationCode)
admin.site.register(User)
# Register your models here.
