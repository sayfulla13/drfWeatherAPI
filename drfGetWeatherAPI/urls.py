from django.urls import path
from weather.views import RegView, LoginView, LogoutView, WeatherView, CreateOrUpdateCityAPIView, GetCSRFTokenView

urlpatterns = [
    path('register/', RegView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('weather/', WeatherView.as_view()),
    path('addcity/', CreateOrUpdateCityAPIView.as_view()),
    path('getcsrf/', GetCSRFTokenView.as_view(), name='get_csrf_token'),
]
