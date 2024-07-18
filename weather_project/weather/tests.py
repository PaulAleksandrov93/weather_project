from django.test import TestCase
from django.contrib.auth.models import User
from .models import SearchHistory

class SearchHistoryTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Создаем записи в SearchHistory, связывая их с пользователем
        SearchHistory.objects.create(user=self.user, city="Moscow")
        SearchHistory.objects.create(user=self.user, city="London")

        # Обновляем search_count для города Moscow
        moscow = SearchHistory.objects.get(city="Moscow")
        moscow.update_search_count()

    def test_search_history_count(self):
        moscow = SearchHistory.objects.get(city="Moscow")
        london = SearchHistory.objects.get(city="London")
        self.assertEqual(moscow.search_count, 1)
        self.assertEqual(london.search_count, 0)  # search_count для London должен остаться 0