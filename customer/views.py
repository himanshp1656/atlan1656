# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Booking
from django.contrib.auth.decorators import login_required

# mapbox=pk.eyJ1IjoiaGltYW5zaHAxNiIsImEiOiJjbTI2NHZqY2oweG1lMmlxd2lzMm1memNyIn0.-CSJEFoXoUPBrn54NI-zAw

from geopy.geocoders import MapBox

from geopy.distance import geodesic
from django.db.models import Q
from driver.models import Driver

def customer_home(request):
    return render(request, 'customer/login.html')
from geopy.distance import geodesic

def get_nearest_driver(pickup_location):
    # Get all drivers that have both latitude and longitude values (i.e., drivers with valid locations)
    drivers = Driver.objects.exclude(latitude__isnull=True, longitude__isnull=True)

    nearby_drivers = []
    
    # Loop through each driver to check their lo    cation
    for driver in drivers:
        # Get the driver's current location from the driver model
        driver_location = (driver.latitude, driver.longitude)

        # Calculate the distance from the pickup location to the driver's location
        distance = geodesic(pickup_location, driver_location).km

        if distance <= 50:  # Only consider drivers within a 50 km radius
            nearby_drivers.append((driver, distance))
    
    if not nearby_drivers:
        return None  # No drivers within 50 km
    
    # Sort drivers by distance and return the list of nearby drivers
    nearby_drivers.sort(key=lambda x: x[1])
    return nearby_drivers  # Return the list of nearby drivers with distances


def get_coordinates_from_address(address):
    # Initialize MapBox geocoder with your access token
    geolocator = MapBox(api_key='pk.eyJ1IjoiaGltYW5zaHAxNiIsImEiOiJjbTI2NHZqY2oweG1lMmlxd2lzMm1memNyIn0.-CSJEFoXoUPBrn54NI-zAw')
    
    # Use geocode method to get location
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None  # If the address is invalid or not found
    

from django.core.mail import send_mail
from django.utils.html import format_html

def send_booking_request_to_drivers(drivers, booking):
    # You can implement this as a notification, email, or database entry.
    # For example, sending an email:
    subject = "New Booking Request"
    message = f"A new booking request has been made for a pickup at {booking.pickup_location}. " \
              f"Please log in to accept or decline the request."
    print(drivers)
    
    driver_emails = [driver.email for driver in drivers]
    email_from = 'himanshp1656autotyper@gmail.com'
    recipient_list = driver_emails
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
    )
    # Send email (this is a simple email sending example, you can enhance it)
from datetime import datetime
from django.utils import timezone

@login_required
def book_vehicle(request):
    if request.method == 'POST':
        pickup_location = request.POST.get('pickup_location')
        dropoff_location = request.POST.get('dropoff_location')
        vehicle_type = request.POST.get('vehicle_type')
        estimated_cost = request.POST.get('estimated_cost')
        pickup_coordinate= get_coordinates_from_address(pickup_location)
        dropoff_coordinate= get_coordinates_from_address(dropoff_location)
        scheduled_time = request.POST.get('scheduled_time')
        print(scheduled_time)
        if scheduled_time:
            scheduled_date = datetime.strptime(scheduled_time, '%Y-%m-%d')
        else:
            # If no scheduled time provided, use today's date
            scheduled_date = timezone.now().date()
        print('sss',scheduled_time)
        if not pickup_coordinate or not dropoff_coordinate:
            messages.error(request, 'Invalid address provided!')
            return redirect('/customer/book/')
        nearby_drivers = get_nearest_driver(pickup_coordinate)

        if nearby_drivers is None:
            messages.error(request, 'No drivers available within a 50 km radius.')
            return redirect('/customer/book/')
        

        # Save the booking details in the database
        booking = Booking.objects.create(
            customer=request.user,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            vehicle_type=vehicle_type,
            estimated_cost=estimated_cost,
            driver=None,
            scheduled_date=scheduled_date,
            status='pending'
        )
        nearby_drivers = [driver[0] for driver in nearby_drivers]
        send_booking_request_to_drivers(nearby_drivers, booking)
        messages.success(request, 'Your booking has been successfully submitted!')
        return redirect('/customer/book/')
    bookings = Booking.objects.filter(customer=request.user).order_by('-date_created')
    return render(request, 'customer/home.html', {'bookings': bookings})

from django.http import JsonResponse

# Customer fetches the driver's latest location
def fetch_driver_location(request,booking_id):

    try:
        booking = Booking.objects.get(id=booking_id)
        return JsonResponse({
            'latitude': booking.driver.latitude,
            'longitude': booking.driver.longitude
        })
    except Booking.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

# views.py
from django.shortcuts import render
from .models import Booking

@login_required
def customer_tracking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if booking.status != 'accepted':
        messages.error(request, "This booking is not active.")
        return redirect('/customer/home')

    return render(request, 'customer/tracking.html', {'booking_id': booking_id})



def calculate_distance(request):
    if request.method == 'GET':
        pickup_location = request.GET.get('pickup_location')
        dropoff_location = request.GET.get('dropoff_location')

        # Get coordinates for both locations
        pickup_coords = get_coordinates_from_address(pickup_location)
        dropoff_coords = get_coordinates_from_address(dropoff_location)
        print(pickup_coords)

        if pickup_coords and dropoff_coords:
            # Calculate the distance in kilometers
            distance_km = geodesic(pickup_coords, dropoff_coords).km
            return JsonResponse({'distance': distance_km})
        else:
            return JsonResponse({'error': 'Invalid address'}, status=400)