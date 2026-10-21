from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reserve/create/', views.create_booking, name='create_booking'), # hx-post="/reserve/create/" を受け取る
]