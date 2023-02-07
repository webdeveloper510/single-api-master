from django.db import models

# Create your models here.

class Setting(models.Model):
    reminder_hours = models.IntegerField(default=6)
    start_coins = models.IntegerField(default=60)

