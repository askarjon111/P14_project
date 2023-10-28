import random
import datetime
import pytz
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from apps.users.models import ConfirmationCode, User
from apps.users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.utils.sms import sms_send


@api_view(['get'])
@authentication_classes([])
@permission_classes([])
def send_code(request):
    sms_type = request.GET.get("request_type")
    phone_number = request.GET.get('phone_number')
    code = random.randint(1000, 9999)
    existing_users = User.objects.filter(phone_number=phone_number)
    sent_codes = ConfirmationCode.objects.filter(
        phone_number=phone_number, created_at__gte=timezone.now() - \
            datetime.timedelta(minutes=5)).count()

    if sent_codes < 3:
        if sms_type == "login" and existing_users.count() == 0:
            return Response({"message": "Bunday foydalanuvchi ro'yxatdan o'tmagan!"}, status=400)
        elif sms_type == "register" and existing_users.count() > 0:
            return Response({"message": "Bunday foydalanuvchi ro'yxatdan o'tgan!"}, status=400)
        else:
            text = "Sizning tasdiq kodingiz {}. Top Top".format(code)
            sms_response = sms_send(phone_number, text)
            if sms_response is not None:

                ConfirmationCode.objects.create(phone_number=phone_number, code=code, created_at=timezone.now())

                data = {
                    "success": True,
                    "message": "Code yuborildi!",
                    "status": 200
                }
            else:
                data = {
                    "success": False,
                    "message": "Code yuborilmadi!",
                    "status": 400
                }
    else:
        data = {
            "success": False,
            "message": "Urinishlar soni oshib ketdi, iltimos birozdan so'ng urinib ko'ring",
            "status": 400
        }


    return Response(data)


@api_view(['get'])
@authentication_classes([])
@permission_classes([])
def confirm_code(request):
    data = {"message": "Code Tasdiqlanmadi!", "status": 400}
    phone_number = request.GET.get('phone_number')
    code = request.GET.get('code')
    confirmation_code = ConfirmationCode.objects.filter(phone_number=phone_number, code=code).last()
    if confirmation_code and confirmation_code.on_time:
        confirmation_code.confirmed = True
        confirmation_code.save()
        data = {
            "message": "Code Tasdiqlandi!",
            "status": 200
        }
    return Response(data, status=data['status'])


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def register(request):
    try:
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_number = request.data.get("phone_number")
        confirmation_code = request.data.get("code")
        existing_users = User.objects.filter(phone_number=phone_number)
        if existing_users.count() > 0:
            return Response({"message": "Bunday foydalanuvchi ro'yxatdan o'tgan!"}, status=400)
        confirmation_codes = ConfirmationCode.objects.filter(phone_number=phone_number, code=confirmation_code)
        if confirmation_codes.count() > 0 and confirmation_codes.last().confirmed_code():
            new_user = User.objects.create(
                phone_number=phone_number, first_name=first_name, last_name=last_name)
            token = RefreshToken.for_user(new_user)
            tokens = {
                "refresh": str(token),
                "access": str(token.access_token)
            }
            data = {
                "success": True,
                "error": "",
                "message": "User created!",
                "data": {
                    "user": UserSerializer(new_user).data,
                    "tokens": tokens
                }
            }
        else:
            data = {
                "success": False,
                "error": "Telefon raqam yoki tasdiq kodi xato!",
                "message": "",
            }
    except Exception as er:
        data = {
            "success": False,
            "error": f"{er}",
            "message": "",
        }
    return Response(data)


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def login(request):
    try:
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        phone_number = request.data.get("phone_number")
        confirmation_code = request.data.get("code")
        existing_users = User.objects.filter(phone_number=phone_number)
        if existing_users.count() == 0:
                return Response({"message": "Bunday foydalanuvchi ro'yxatdan o'tmagan!"}, status=400)
        confirmation_codes = ConfirmationCode.objects.filter(phone_number=phone_number, code=confirmation_code)
        if confirmation_codes.count() > 0:
            new_user = User.objects.create(
                phone_number=phone_number, first_name=first_name, last_name=last_name)
            token = RefreshToken.for_user(new_user)
            tokens = {
                "refresh": str(token),
                "access": str(token.access_token)
            }
            data = {
                "success": True,
                "error": "",
                "message": "User created!",
                "data": {
                    "user": UserSerializer(new_user).data,
                    "tokens": tokens
                }
            }
        else:
            data = {
                "success": False,
                "error": "Telefon raqam yoki tasdiq kodi xato!",
                "message": "",
            }
    except Exception as er:
        data = {
            "success": False,
            "error": f"{er}",
            "message": "",
        }
    return Response(data)
