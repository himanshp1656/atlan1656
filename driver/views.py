from geopy.distance import geodesic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Driver  # Import your models
from customer.models import Booking  # Import the Booking model



# gorpro=AlzaSyHRzJG3JUlm2KZ4Wr8utVNF9_IMr42qSkr


from django.shortcuts import render, get_object_or_404


from geopy.distance import geodesic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  Driver

from geopy.geocoders import MapBox

from geopy.distance import geodesic

def driver_home(request):
    return render(request, 'driver/home.html')

def get_coordinates_from_address(address):
    # Initialize MapBox geocoder with your access token
    geolocator = MapBox(api_key='pk.eyJ1IjoiaGltYW5zaHAxNiIsImEiOiJjbTI2NHZqY2oweG1lMmlxd2lzMm1memNyIn0.-CSJEFoXoUPBrn54NI-zAw')
    
    # Use geocode method to get location
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None 
    
@login_required
def driver_booking_requests(request):
    try:
        # Fetch the driver linked to the current user
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "You are not registered as a driver.")
        return redirect('/driver/home')

    # Ensure driver location is set
    if driver.latitude is None or driver.longitude is None:
        messages.error(request, "Your current location is not set.")
        return redirect('/driver/home')

    driver_coords = (driver.latitude, driver.longitude)
    print(driver_coords)
    print('lll',driver_coords)
    # Get all pending bookings, ordered by latest creation date
    all_bookings = Booking.objects.filter(status='pending')
    available_bookings = []
    print(all_bookings.count())
    # Filter bookings within 50 km
    for booking in all_bookings:
        print('jjj',booking.pickup_location)
        if isinstance(booking.pickup_location, str):
            try:
                booking_pickup_coords = get_coordinates_from_address(booking.pickup_location)
                print('jjj',booking_pickup_coords)
            except Exception as e:
                print(f"Error getting coordinates: {e}")
                continue  # Skip if there's an error in geocoding
        else:
            booking_pickup_coords = (booking.pickup_location.latitude, booking.pickup_location.longitude)

        # Calculate distance if coordinates are valid
        if booking_pickup_coords:
            distance = geodesic(driver_coords, booking_pickup_coords).km
            if distance <= 50:
                available_bookings.append(booking)

    status_bookings = Booking.objects.filter(driver=driver).order_by('-date_created')

    # Handle booking acceptance by driver
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id, status='pending')
            booking.driver = driver
            booking.status = 'accepted'
            booking.save()
            messages.success(request, 'You have accepted the booking successfully!')
            return redirect(f'/driver/tracking/{booking.id}')  # Redirect to tracking page
        except Booking.DoesNotExist:
            messages.error(request, 'This booking is no longer available.')
    print('jjj',available_bookings)
    return render(request, 'driver/home.html', {'bookings': available_bookings, 'status_bookings': status_bookings})

# views.py (inside the completion function)
def complete_delivery(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'completed'
        driver = booking.driver
        
        # Save driver's final location to database
        driver.latitude = request.POST.get('latitude')
        driver.longitude = request.POST.get('longitude')
        driver.save()
        
        booking.save()
        messages.success(request, 'Delivery completed!')
    return redirect('some_dashboard')



def driver_tracking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # You can pass additional context here if needed
    return render(request, 'driver/tracking.html', {'booking_id': booking.id})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Driver
import json

# Driver updates their location
@csrf_exempt
def update_driver_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        booking_id = data.get('booking_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        try:
            booking = Booking.objects.get(id=booking_id)
            booking.driver.latitude = latitude
            booking.driver.longitude = longitude
            booking.driver.save()
            return JsonResponse({'status': 'success'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def change_booking_status(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        booking = get_object_or_404(Booking, id=booking_id)

        # Update the booking status
        booking.status = new_status
        booking.save()

        messages.success(request, 'Booking status updated successfully!')
        return redirect('driver_bookings')  # Redirect to your bookings page

    messages.error(request, 'Invalid request method.')
    return redirect('driver_bookings')  # Redirect on error
