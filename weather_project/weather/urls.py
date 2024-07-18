from django.urls import path
from .views import index, get_weather, search_history

urlpatterns = [
    path('', index, name='index'),
    path('weather/<str:city>/', get_weather, name='get_weather'),
    path('history/', search_history, name='search_history'),
]