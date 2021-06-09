import json

from django.http import HttpResponse

import psycopg2
from django.template import loader

con = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="localhost",
    database="ads")

cur = con.cursor()


def ads_list(request):
    req = "select * from ad"
    cur.execute(req)
    ads_from_db = cur.fetchall()
    ads_array = []
    for ad in ads_from_db:
        single_ad = {"description": ad[1],
                     "price": ad[2],
                     }
        if ad[3] is not None:
            single_ad["hot_price"] = ad[3]

        if ad[4] is True:
            single_ad["top"] = True
        ads_array.append(single_ad)
    ads_in_json = {"ads": ads_array}
    template = loader.get_template('ad_page/ads.html')
    context = ads_in_json

    return HttpResponse(template.render(context, request))
