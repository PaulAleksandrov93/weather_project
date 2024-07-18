# import requests
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import SearchHistory
# from .serializers import SearchHistorySerializer

# from django.shortcuts import render
# from rest_framework import status  # Добавляем импорт для статусов ответа

# def index(request):
#     return render(request, 'index.html')

# @api_view(['GET'])
# def get_weather(request, city):
#     weather_api_url = f"https://api.open-meteo.com/v1/forecast?city={city}&...&daily=temperature_2m_max"
    
#     try:
#         response = requests.get(weather_api_url)
#         response.raise_for_status()  # Проверяем на ошибки HTTP
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         return Response({'error': f'Error fetching weather data: {e}'}, status=status.HTTP_400_BAD_REQUEST)

#     # Обновление или создание записи в истории поиска
#     try:
#         search_history = SearchHistory.objects.get(city=city)
#         search_history.search_count += 1
#     except SearchHistory.DoesNotExist:
#         search_history = SearchHistory(city=city, search_count=1)
    
#     search_history.save()

#     return Response(data)

# @api_view(['GET'])
# def search_history(request):
#     history = SearchHistory.objects.all()
#     serializer = SearchHistorySerializer(history, many=True)
#     return Response(serializer.data)

# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import pandas as pd
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import SearchHistory
# from .serializers import SearchHistorySerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)
# geolocator = Nominatim(user_agent="your_app_name")

# @api_view(['GET'])
# def get_weather(request, city):
#     try:
#         location = geolocator.geocode(city)
#         if not location:
#             return Response({"error": "Could not find coordinates for the city"}, status=status.HTTP_404_NOT_FOUND)
        
#         latitude = location.latitude
#         longitude = location.longitude

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = {"latitude": latitude, "longitude": longitude, "hourly": "temperature_2m"}

#         responses = openmeteo.weather_api(url, params=params)
#         if not responses:
#             return Response({"error": "No data available for the requested city"}, status=status.HTTP_404_NOT_FOUND)
        
#         response = responses[0]
#         hourly = response.Hourly()
#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

#         hourly_data = {
#             "date": pd.to_datetime(hourly.Time(), unit="s", utc=True) + pd.to_timedelta(pd.np.arange(hourly.Timesteps()), 'h'),
#             "temperature_2m": hourly_temperature_2m.tolist()
#         }

#         # Save search history
#         save_search_history(request.user, city)

#         return Response(hourly_data)

#     except GeocoderTimedOut:
#         return Response({"error": "Geocoding service timed out"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def search_history(request):
#     history = SearchHistory.objects.filter(user=request.user).order_by('-last_searched')
#     serializer = SearchHistorySerializer(history, many=True)
#     return Response(serializer.data)

# @csrf_exempt
# def index(request):
#     return render(request, 'index.html')

# # Save search history
# def save_search_history(user, city):
#     try:
#         search_history = SearchHistory.objects.get(user=user, city=city)
#         search_history.search_count += 1
#     except SearchHistory.DoesNotExist:
#         search_history = SearchHistory(user=user, city=city, search_count=1)
#     search_history.save()


# ============
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import pandas as pd
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import SearchHistory
# from .serializers import SearchHistorySerializer
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)
# geolocator = Nominatim(user_agent="your_app_name")

# @api_view(['GET'])
# def get_weather(request, city):
#     try:
#         location = geolocator.geocode(city)
#         if not location:
#             return Response({"error": "Could not find coordinates for the city"}, status=status.HTTP_404_NOT_FOUND)
        
#         latitude = location.latitude
#         longitude = location.longitude

#         url = "https://api.open-meteo.com/v1/forecast"
#         params = {"latitude": latitude, "longitude": longitude, "hourly": "temperature_2m"}

#         responses = openmeteo.weather_api(url, params=params)
#         if not responses:
#             return Response({"error": "No data available for the requested city"}, status=status.HTTP_404_NOT_FOUND)
        
#         response = responses[0]
#         hourly = response.Hourly()
#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

#         # Convert timestamps to UTC datetime objects
#         timestamps = hourly.Time()
#         datetimes = [pd.to_datetime(ts, unit="s", utc=True) for ts in timestamps]

#         hourly_data = {
#             "date": [dt.isoformat() for dt in datetimes],
#             "temperature_2m": hourly_temperature_2m.tolist()
#         }

#         # Save search history
#         save_search_history(request.user, city)

#         return Response(hourly_data)

#     except GeocoderTimedOut:
#         return Response({"error": "Geocoding service timed out"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def search_history(request):
#     history = SearchHistory.objects.filter(user=request.user).order_by('-last_searched')
#     serializer = SearchHistorySerializer(history, many=True)
#     return Response(serializer.data)

# @csrf_exempt
# def index(request):
#     return render(request, 'index.html')

# # Save search history
# def save_search_history(user, city):
#     try:
#         search_history = SearchHistory.objects.get(user=user, city=city)
#         search_history.search_count += 1
#     except SearchHistory.DoesNotExist:
#         search_history = SearchHistory(user=user, city=city, search_count=1)
#     search_history.save()




#====


from openmeteo_requests import Client
import requests_cache
from retry_requests import retry
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SearchHistory
from .serializers import SearchHistorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Инициализация клиента Open-Meteo API с кэшем и повторными попытками при ошибке
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = Client(session=retry_session)

# Инициализация геокодера для определения координат по названию города
geolocator = Nominatim(user_agent="weather")

@api_view(['GET'])
def get_weather(request, city):
    try:
        # Получаем координаты города с помощью геокодера
        location = geolocator.geocode(city)
        if not location:
            return Response({"error": "Could not find coordinates for the city"}, status=status.HTTP_404_NOT_FOUND)
        
        latitude = location.latitude
        longitude = location.longitude

        # Параметры для запроса погоды
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }

        # Получаем ответ от API Open-Meteo
        responses = openmeteo.weather_api(url, params=params)
        if not responses:
            return Response({"error": "No data available for the requested city"}, status=status.HTTP_404_NOT_FOUND)
        
        response = responses[0]

        # Обработка данных о погоде
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly_temperature_2m.tolist()
        }

        # Сохраняем историю поиска
        save_search_history(request.user, city)

        return Response(hourly_data)

    except GeocoderTimedOut:
        return Response({"error": "Geocoding service timed out"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_history(request):
    # Получаем историю поиска пользователя
    history = SearchHistory.objects.filter(user=request.user).order_by('-last_searched')
    serializer = SearchHistorySerializer(history, many=True)
    return Response(serializer.data)

@csrf_exempt
def index(request):
    return render(request, 'index.html')

# Функция для сохранения истории поиска
def save_search_history(user, city):
    try:
        search_history, created = SearchHistory.objects.get_or_create(user=user, city=city)
        if not created:
            search_history.search_count += 1
        search_history.save()
    except Exception as e:
        # Обработка ошибок, например, логирование или возврат ошибки HTTP
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)