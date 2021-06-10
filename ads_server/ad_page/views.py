from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import Ad


def ads_list(request):
    hot = Ad.objects.filter(
        created__gte=timezone.now() - timedelta(minutes=5),
        hot_price__isnull=False,
        is_published=True,
    ).first()
    ads = Ad.objects.filter(created__gte=timezone.now() - timedelta(hours=1), is_published=True).exclude(id=hot.id)
    return render(request, 'ad_page/ads.html', {'ads': ads, 'hot': hot})
