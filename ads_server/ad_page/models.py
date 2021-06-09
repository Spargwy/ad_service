from django.db import models
from pydantic import BaseModel


class Ad(models.Model):
    ad_text = models.TextField()
    ad_price = models.IntegerField()
    ad_hot_price = models.IntegerField()