# # models.py
from django.db import models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# class Location(models.Model):
#     latitude = models.FloatField()  # Latitude coordinate
#     longitude = models.FloatField()  # Longitude coordinate
#     timestamp = models.DateTimeField(auto_now_add=True)
#     driver = models.ForeignKey('Driver', related_name='locations', on_delete=models.CASCADE)

#     def clean(self):
#         # Latitude range check
#         if not (-90 <= self.latitude <= 90):
#             raise ValidationError("Invalid latitude value. Must be between -90 and 90.")
        
#         # Longitude range check
#         if not (-180 <= self.longitude <= 180):
#             raise ValidationError("Invalid longitude value. Must be between -180 and 180.")

#     def __str__(self):
#         return f"Location({self.latitude}, {self.longitude}) at {self.timestamp}"

class Driver(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    license = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    


    def __str__(self):
        return self.name
