from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reserve.urls')), # すべてのルートを reserve アプリの urls.py に委任
]