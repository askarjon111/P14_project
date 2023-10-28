
from django.http import JsonResponse



def sms_login():
    # r = requests.post(settings.SMS_BASE_URL + '/api/auth/login/',
    #                   {'email': settings.SMS_EMAIL, 'password': settings.SMS_SECRET_KEY}).json()
    # settings.SMS_TOKEN = r['data']['token']
    print('successful login')


def sms_refresh():
    # r = requests.patch(settings.SMS_BASE_URL + '/api/auth/refresh',
    #                    headers={'Authorization': f'Bearer {settings.SMS_TOKEN}'}).json()
    # settings.SMS_TOKEN = r['data']['token']
    print('refresh')


def sms_send(phone_number, text):
    try:
        phone_number = str(phone_number)
        phone_number.replace("+", "")
        if phone_number[0:3] == "998":
            sms_login()
            # result = requests.post(settings.SMS_BASE_URL + '/api/message/sms/send',
            #                        {'mobile_phone': phone_number, 'message': text},
            #                        headers={'Authorization': f'Bearer {settings.SMS_TOKEN}'}).json()
            print(phone_number, text)

            # return result
            return True
        else:
            raise ValueError("Telefon raqam noto'g'ri")
    except Exception as e:
        data = {
            "success": False,
            "message": f"{e}"
        }
        return JsonResponse(data)