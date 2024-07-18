from django.test import TestCase
from .models import SearchHistory

class SearchHistoryTestCase(TestCase):
    def setUp(self):
        SearchHistory.objects.create(city="Moscow")
        SearchHistory.objects.create(city="London")

    def test_search_history_count(self):
        moscow = SearchHistory.objects.get(city="Moscow")
        london = SearchHistory.objects.get(city="London")
        self.assertEqual(moscow.search_count, 1)
        self.assertEqual(london.search_count, 1)