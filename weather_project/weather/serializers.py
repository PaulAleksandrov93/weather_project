# from rest_framework import serializers
# from .models import SearchHistory

# class SearchHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SearchHistory
#         fields = ['city', 'search_count', 'last_searched']

from rest_framework import serializers
from .models import SearchHistory
from django.contrib.auth.models import User

class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SearchHistory
        fields = ['user', 'city', 'search_count', 'last_searched']