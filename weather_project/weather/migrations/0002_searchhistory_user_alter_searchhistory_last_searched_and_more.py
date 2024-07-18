# Generated by Django 5.0.7 on 2024-07-18 17:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='last_searched',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='search_count',
            field=models.IntegerField(default=0),
        ),
    ]
