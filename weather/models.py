from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

#Расширил базовую изер модель
class User(AbstractUser):
    status_choises = ( #добавил 2 статцса : обычный юзер и менеджер
        ('user', 'User'),
        ('manager', 'Manager'),
    )
    status = models.CharField(max_length=20,choices=status_choises, default='user')
    city = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        # Указываем новый related_name, чтобы избежать конфликта
        permissions = [
            ("can_add_city", "Может добавлять города"),
        ]

    def __str__(self):
        return self.username

#Модель хранит инфу о погоде
class Weather(models.Model):
    city = models.CharField(max_length=100, unique=True)
    temp = models.FloatField()
    description = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now=True) #Ласт обновление инфы о погоде

    def __str__(self):
        return f"{self.city}: {self.temperature}°C, {self.description}"
