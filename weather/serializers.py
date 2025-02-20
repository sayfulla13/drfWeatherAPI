from rest_framework import serializers
from .models import User, Weather

#Сериализатор для пользователей
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'status', 'city']

#Сериализатор для данных о погоде
class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['city' ,'temp' ,'description' ,'last_update']