from datetime import timedelta

from django.db import models
from django.utils import timezone


class Ad(models.Model):
    chat_id = models.IntegerField()
    text = models.TextField(null=True)
    price = models.IntegerField(null=True)
    hot_price = models.IntegerField(null=True)
    created = models.DateTimeField(null=True, auto_now=True)
    is_published = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.text if self.text else 'Empty ad'

    class Meta:
        ordering = ('-created',)
