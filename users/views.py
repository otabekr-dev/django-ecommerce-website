import json
from django.views import View
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest, JsonResponse


User = get_user_model()

class RegisterView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        if not username:
            return JsonResponse({'error': 'Username kiriting'})
        if not first_name:
            return JsonResponse({'error': 'Ismingizni kiriting'})
        if not last_name:
            return JsonResponse({'error': 'Familiyangizni kiriting'})
        if not password:
            return JsonResponse({'error': 'Parol kiriting'})
        if len(password) < 8:
            return JsonResponse({'error': 'Parol 8 tadan kam bulmasligi kerak'})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return JsonResponse({'done': 'User yaratildi'})

class LoginView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'err':'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            return JsonResponse({'done':'Welcome!'})
        else:
            return JsonResponse({'err':'Username yoki parol xato'})    