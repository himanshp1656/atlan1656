from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.driver_booking_requests, name='driver_bookings'),
    path('home/', views.driver_home, name='driver_home'),

  path('tracking/<int:booking_id>/', views.driver_tracking, name='driver_tracking'),
    path('update-location/', views.update_driver_location, name='update_driver_location'),   
     path('bookings/change/<int:booking_id>/', views.change_booking_status, name='change_booking_status'),
]
