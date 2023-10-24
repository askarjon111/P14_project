from django.urls import path

from apps.users.views import confirm_code, send_code, register


urlpatterns = [
    path('send-code/', send_code, name='send_code'),
    path('confirm-code/', confirm_code, name='confirm_code'),
    path('register/', register,name='register',)
]
