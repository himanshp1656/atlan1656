from django.test import TestCase

# Create your tests here.
from geopy.geocoders import MapBox

def get_coordinates_from_address(address):
    # Initialize MapBox geocoder with your access token
    geolocator = MapBox(api_key='pk.eyJ1IjoiaGltYW5zaHAxNiIsImEiOiJjbTI2NHZqY2oweG1lMmlxd2lzMm1memNyIn0.-CSJEFoXoUPBrn54NI-zAw')
    
    # Use geocode method to get location
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None  # If the address is invalid or not found

# Example usage
address = "Noida"
coordinates = get_coordinates_from_address(address)
if coordinates:
    print(f"Coordinates for '{address}': {coordinates}")
else:
    print("Address not found.")
