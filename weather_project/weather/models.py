# models.py
from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    search_count = models.IntegerField(default=0)
    last_searched = models.DateTimeField(auto_now_add=True)

    def update_search_count(self):
        self.search_count += 1
        self.save()

    def __str__(self):
        return f"{self.city} - {self.user.username}"