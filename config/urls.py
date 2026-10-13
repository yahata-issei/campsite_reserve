from django.contrib import admin
from django.urls import path
from reserve import views

urlpatterns = [
    path('admin/', admin.site.urls),          # 管理者画面
    path('', views.index, name='index'),      # 何も指定しないトップページ
    path('clicked/', views.clicked, name='clicked'), # 通信テスト用
]