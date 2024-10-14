# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_vehicle, name='book_vehicle'),
   path('fetch-location/<int:booking_id>/', views.fetch_driver_location, name='fetch_driver_location'),
     path('tracking/<int:booking_id>/', views.customer_tracking, name='customer_tracking'),
       path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
]
