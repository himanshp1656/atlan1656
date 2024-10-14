# models.py
from django.db import models
from django.contrib.auth.models import User
from driver.models import Driver
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('on_the_way_to_pickup', 'On the Way to pickup'),
        ('in_progress_to_dropoff', 'In Progress to dropoff'),
        ('completed', 'Completed'),
    ]
    driver= models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    estimated_cost= models.FloatField()
    # accepted = models.BooleanField(default=False) 
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    scheduled_date = models.DateField()
    
    def __str__(self):
        return f"Booking by {self.customer.username} from {self.pickup_location} to {self.dropoff_location}"
