from django.contrib import admin
from .models import Campsite, Booking

# 管理画面に Campsite と Booking のテーブルを追加
admin.site.register(Campsite)
admin.site.register(Booking)