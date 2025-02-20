from datetime import timedelta
import requests
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Weather
from .serializers import UserSerializer, WeatherSerializer
from drfGetWeatherAPI import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFTokenView(APIView):
    def get(self, request):
        return Response({"message": "CSRF token set"})


# Регистрация
class RegView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=request.data['password'],
                status=serializer.validated_data['status'],
                city=serializer.validated_data.get('city', None)
            )
            return Response({"message": "Пользователь зарегистрирован"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Вход
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)#проверяем данные на вход

        if user:
            login(request, user)
            return Response({"message": "Вход выполнен", "user": UserSerializer(user).data})
        return Response({"error": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

# Выход пользователя

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Вы вышли из системы"}, status=status.HTTP_200_OK)

# Запрос погоды
class WeatherView(APIView):
    permission_classes = [permissions.IsAuthenticated] #доступ только авторизированным юзерам

    def get(self, request):
        user = request.user # получаем нашего пользователя с модели

        if user.status == "manager":
            return Response({"error": "Менеджеры не могут запрашивать погоду"}, status=status.HTTP_403_FORBIDDEN)


        weather = Weather.objects.filter(city=user.city).first()

        if weather and (now() - weather.last_update < timedelta(minutes=10)):#проверяем последнее время обновление погоды и существует ли инфа об этом в городе в бд
            return Response(WeatherSerializer(weather).data)

        api_key = settings.weather_api_key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={user.city}&appid={api_key}&units=metric"
        response = requests.get(url)# Обращаемся к внешнему апи

        data = response.json()

        weather, created = Weather.objects.update_or_create(
            city=user.city, #Создаем или обновляем данные о городе
            defaults={#если обновляем то только эти поля
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "last_update": now()
            }
        )

        return Response(WeatherSerializer(weather).data)

# Добавление города (только для менеджеров)
class CreateOrUpdateCityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.status != "manager":
            return Response({"error": "Только менеджеры могут добавлять города"}, status=status.HTTP_403_FORBIDDEN)

        city_name = request.data.get("city")
        if not city_name:
            return Response({"error": "Название города обязательно"}, status=status.HTTP_400_BAD_REQUEST)

        api_key = settings.weather_api_key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Ошибка при запросе к API погоды"}, status=response.status_code)

        data = response.json()

        weather, created = Weather.objects.update_or_create(
            city=city_name,
            defaults={
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "last_update": now()
            }
        )

        return Response({"message": "Город добавлен", "data": WeatherSerializer(weather).data})
